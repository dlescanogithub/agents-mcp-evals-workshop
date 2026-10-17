"""JSON logs on stderr so an MCP stdio server can keep stdout for protocol frames."""

from __future__ import annotations

import json
import logging
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import TextIO


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "ts": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        fields = getattr(record, "fields", None)
        if isinstance(fields, Mapping):
            payload["fields"] = {str(key): value for key, value in fields.items()}
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, sort_keys=True)


def configure(level: str = "INFO", stream: TextIO | None = None) -> logging.Logger:
    logger = logging.getLogger("workshop")
    logger.handlers.clear()
    logger.propagate = False
    handler = logging.StreamHandler(stream if stream is not None else sys.stderr)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(level.upper())
    return logger


def log_event(logger: logging.Logger, message: str, **fields: object) -> None:
    logger.info(message, extra={"fields": fields})
