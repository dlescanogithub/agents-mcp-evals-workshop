"""Optional live adapter. Off unless the environment explicitly enables it.

The request body is a generic JSON envelope. It is not a client for any vendor SDK.
"""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from typing import cast

from workshop.config import Settings
from workshop.models import ModelTurn

Transport = Callable[[str, Mapping[str, object], str], Mapping[str, object]]


class LiveProviderDisabled(RuntimeError):
    """The live adapter refused to start. This is the default."""


def build_live_request(url: str, body: Mapping[str, object], api_key: str) -> tuple[str, bytes, dict[str, str]]:
    payload = json.dumps(dict(body)).encode("utf-8")
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }
    return url, payload, headers


def redact(text: str, secret: str) -> str:
    if secret and secret in text:
        return text.replace(secret, "[redacted]")
    return text


def urllib_transport(url: str, body: Mapping[str, object], api_key: str) -> Mapping[str, object]:
    target, payload, headers = build_live_request(url, body, api_key)
    request = urllib.request.Request(target, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        raw = cast(object, json.loads(response.read().decode("utf-8")))
    if not isinstance(raw, dict):
        raise RuntimeError("live provider returned a non-object")
    return {str(key): value for key, value in raw.items()}


def _turn_from_payload(payload: Mapping[str, object]) -> ModelTurn:
    text = payload.get("text", "")
    if not isinstance(text, str) or text == "":
        raise RuntimeError("live provider payload needs a text field")
    return ModelTurn(kind="final", text=text)


class LiveProvider:
    def __init__(self, settings: Settings, transport: Transport | None = None) -> None:
        if not settings.enable_live:
            raise LiveProviderDisabled(
                "Live provider is off. Set WORKSHOP_ENABLE_LIVE_PROVIDER=1 to enable it. "
                "CI must not set that flag."
            )
        if settings.provider != "live":
            raise LiveProviderDisabled("Set WORKSHOP_PROVIDER=live together with the enable flag.")
        if not settings.live_base_url or not settings.live_api_key:
            raise LiveProviderDisabled("Live provider needs WORKSHOP_LIVE_BASE_URL and WORKSHOP_LIVE_API_KEY.")
        self._url = settings.live_base_url
        self._api_key = settings.live_api_key
        self._transport = urllib_transport if transport is None else transport

    def complete(self, messages: Sequence[Mapping[str, str]]) -> ModelTurn:
        body: dict[str, object] = {
            "messages": [{"role": item["role"], "content": item["content"]} for item in messages]
        }
        payload = self._transport(self._url, body, self._api_key)
        return _turn_from_payload(payload)
