"""Typed tools, a human gate, and the synthetic depot handlers."""

from workshop.tools.auth import Decision, authorize_tool
from workshop.tools.execute import execute
from workshop.tools.specs import (
    CATALOG,
    INVENTORY_ADJUST,
    INVENTORY_LOOKUP,
    NOTES_SEARCH,
    ToolSpec,
)

__all__ = [
    "CATALOG",
    "INVENTORY_ADJUST",
    "INVENTORY_LOOKUP",
    "NOTES_SEARCH",
    "Decision",
    "ToolSpec",
    "authorize_tool",
    "execute",
]
