"""Optional LLM judge. Off unless LIVE_MODE=1 and the endpoint settings are set.

The eval gate does not call this. Tests pass a fake HTTP transport.
"""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import cast

from workshop.providers.live import redact

Transport = Callable[[str, Mapping[str, str], Mapping[str, object]], Mapping[str, object]]


@dataclass(frozen=True)
class LiveJudgeSettings:
    base_url: str
    model: str
    api_key: str
    max_spend_usd: float
    input_usd_per_token: float
    output_usd_per_token: float
    price_date: str


@dataclass(frozen=True)
class JudgeCall:
    label: str | None
    spent_usd: float
    price_date: str
    skipped: str


def _non_negative(raw: str) -> float | None:
    try:
        value = float(raw)
    except ValueError:
        return None
    if value < 0:
        return None
    return value


def load_live_judge_settings(env: Mapping[str, str]) -> LiveJudgeSettings | None:
    """Return settings only when every required variable is present. Otherwise None."""

    if env.get("LIVE_MODE", "").strip() != "1":
        return None
    base_url = env.get("LLM_BASE_URL", "").strip()
    model = env.get("LLM_MODEL", "").strip()
    api_key = env.get("LLM_API_KEY", "").strip()
    price_date = env.get("LLM_PRICE_DATE", "").strip()
    max_raw = env.get("MAX_LIVE_SPEND_USD", "").strip()
    input_raw = env.get("LLM_INPUT_USD_PER_TOKEN", "").strip()
    output_raw = env.get("LLM_OUTPUT_USD_PER_TOKEN", "").strip()
    if not all((base_url, model, api_key, price_date, max_raw, input_raw, output_raw)):
        return None
    max_spend = _non_negative(max_raw)
    input_price = _non_negative(input_raw)
    output_price = _non_negative(output_raw)
    if max_spend is None or input_price is None or output_price is None:
        return None
    return LiveJudgeSettings(
        base_url=base_url,
        model=model,
        api_key=api_key,
        max_spend_usd=max_spend,
        input_usd_per_token=input_price,
        output_usd_per_token=output_price,
        price_date=price_date,
    )


def chat_completions_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/chat/completions"


def token_cost(settings: LiveJudgeSettings, input_tokens: int, output_tokens: int) -> float:
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts must be >= 0")
    return (input_tokens * settings.input_usd_per_token) + (output_tokens * settings.output_usd_per_token)


def _label_from_text(content: str) -> str | None:
    word = content.strip().casefold()
    if word == "pass":
        return "pass"
    if word == "fail":
        return "fail"
    return None


def _usage(payload: Mapping[str, object]) -> tuple[int, int] | None:
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        return None
    prompt = usage.get("prompt_tokens")
    completion = usage.get("completion_tokens")
    if isinstance(prompt, bool) or isinstance(completion, bool):
        return None
    if not isinstance(prompt, int) or not isinstance(completion, int):
        return None
    return prompt, completion


def _message_text(payload: Mapping[str, object]) -> str | None:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    if not isinstance(content, str):
        return None
    return content


def run_llm_judge(
    text: str,
    phrase: str,
    settings: LiveJudgeSettings,
    transport: Transport,
) -> JudgeCall:
    """Call the transport once. A zero cap does not call it. Over-cap spend is discarded."""

    if settings.max_spend_usd == 0:
        return JudgeCall(label=None, spent_usd=0.0, price_date=settings.price_date, skipped="spend_cap")
    body: dict[str, object] = {
        "model": settings.model,
        "messages": [
            {
                "role": "user",
                "content": ("Reply with pass or fail only.\nPhrase: " + phrase + "\nText: " + text),
            }
        ],
    }
    headers = {
        "authorization": "Bearer " + settings.api_key,
        "content-type": "application/json",
    }
    payload = transport(chat_completions_url(settings.base_url), headers, body)
    usage = _usage(payload)
    content = _message_text(payload)
    if usage is None or content is None:
        return JudgeCall(label=None, spent_usd=0.0, price_date=settings.price_date, skipped="unparsed")
    spent = token_cost(settings, usage[0], usage[1])
    if spent - settings.max_spend_usd > 1e-12:
        return JudgeCall(label=None, spent_usd=spent, price_date=settings.price_date, skipped="spend_cap")
    label = _label_from_text(content)
    if label is None:
        return JudgeCall(label=None, spent_usd=spent, price_date=settings.price_date, skipped="unparsed")
    return JudgeCall(label=label, spent_usd=spent, price_date=settings.price_date, skipped="")


def urllib_transport(
    url: str,
    headers: Mapping[str, str],
    payload: Mapping[str, object],
) -> Mapping[str, object]:
    data = json.dumps(dict(payload)).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=dict(headers), method="POST")
    with urllib.request.urlopen(request, timeout=10) as response:
        raw = cast(object, json.loads(response.read().decode("utf-8")))
    if not isinstance(raw, dict):
        raise RuntimeError("llm judge returned a non-object")
    return {str(key): value for key, value in raw.items()}


def public_settings(settings: LiveJudgeSettings) -> dict[str, object]:
    """Fields safe to print. The key is never included."""

    return {
        "base_url": settings.base_url,
        "model": settings.model,
        "api_key_set": bool(settings.api_key),
        "max_spend_usd": settings.max_spend_usd,
        "input_usd_per_token": settings.input_usd_per_token,
        "output_usd_per_token": settings.output_usd_per_token,
        "price_date": settings.price_date,
        "redacted": redact("Bearer " + settings.api_key, settings.api_key),
    }
