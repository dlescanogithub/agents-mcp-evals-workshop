"""Module 8 exercise. Compare checker and LLM-judge labels with the reference.

This module is optional. It is not part of the planned 2 x 3 h sessions.
The LLM judge stays off unless you configure it yourself, outside CI.
"""

from __future__ import annotations

from collections.abc import Sequence


def compare_against_reference(
    rows: Sequence[tuple[bool, bool | None, bool]],
) -> dict[str, int]:
    """Count agreements with the reference label.

    Each row is (checker, llm_judge, reference). ``llm_judge`` is None when
    that row has no model label; leave those rows out of the LLM counts.
    Return checker_compared, checker_agreements, llm_compared, llm_agreements.
    """

    raise NotImplementedError("module 8: compare checker, LLM judge, and reference labels")
