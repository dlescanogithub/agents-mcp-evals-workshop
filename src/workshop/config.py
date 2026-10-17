"""Environment-only settings. This module does not read files."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass


class ConfigError(ValueError):
    """Raised when an environment value cannot be used."""


@dataclass(frozen=True)
class Settings:
    provider: str
    enable_live: bool
    live_base_url: str
    live_api_key: str
    budget_usd: float
    max_steps: int
    max_attempts: int
    backoff_cap_s: float
    base_delay_s: float
    log_level: str

    def public_dict(self) -> dict[str, object]:
        """Settings safe to log. The live key is never included."""

        return {
            "provider": self.provider,
            "enable_live": self.enable_live,
            "live_base_url": self.live_base_url,
            "live_api_key_set": bool(self.live_api_key),
            "budget_usd": self.budget_usd,
            "max_steps": self.max_steps,
            "max_attempts": self.max_attempts,
            "backoff_cap_s": self.backoff_cap_s,
            "log_level": self.log_level,
        }


def _flag(raw: str | None, default: str = "0") -> bool:
    value = (default if raw is None else raw).strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off", ""}:
        return False
    raise ConfigError(f"expected a boolean flag, got {raw!r}")


def _positive_int(raw: str | None, default: int, *, name: str) -> int:
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer") from exc
    if value < 1:
        raise ConfigError(f"{name} must be >= 1")
    return value


def _non_negative_float(raw: str | None, default: float, *, name: str) -> float:
    if raw is None or raw.strip() == "":
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be a number") from exc
    if value < 0:
        raise ConfigError(f"{name} must be >= 0")
    return value


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    source = os.environ if env is None else env
    provider = source.get("WORKSHOP_PROVIDER", "fake").strip() or "fake"
    if provider not in {"fake", "live"}:
        raise ConfigError("WORKSHOP_PROVIDER must be fake or live")
    enable_live = _flag(source.get("WORKSHOP_ENABLE_LIVE_PROVIDER"))
    if provider == "live" and not enable_live:
        raise ConfigError("WORKSHOP_PROVIDER=live also requires WORKSHOP_ENABLE_LIVE_PROVIDER=1")
    return Settings(
        provider=provider,
        enable_live=enable_live,
        live_base_url=source.get("WORKSHOP_LIVE_BASE_URL", "").strip(),
        live_api_key=source.get("WORKSHOP_LIVE_API_KEY", "").strip(),
        budget_usd=_non_negative_float(source.get("WORKSHOP_BUDGET_USD"), 0.01, name="WORKSHOP_BUDGET_USD"),
        max_steps=_positive_int(source.get("WORKSHOP_MAX_STEPS"), 6, name="WORKSHOP_MAX_STEPS"),
        max_attempts=_positive_int(source.get("WORKSHOP_MAX_ATTEMPTS"), 3, name="WORKSHOP_MAX_ATTEMPTS"),
        backoff_cap_s=_non_negative_float(
            source.get("WORKSHOP_BACKOFF_CAP_S"), 0.05, name="WORKSHOP_BACKOFF_CAP_S"
        ),
        base_delay_s=0.01,
        log_level=source.get("WORKSHOP_LOG_LEVEL", "INFO").strip() or "INFO",
    )
