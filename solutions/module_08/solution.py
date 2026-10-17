"""Module 8 answer. Count checker and LLM-judge labels against the reference."""

from __future__ import annotations

from collections.abc import Sequence


def compare_against_reference(
    rows: Sequence[tuple[bool, bool | None, bool]],
) -> dict[str, int]:
    checker_compared = 0
    checker_agreements = 0
    llm_compared = 0
    llm_agreements = 0
    for checker, llm_label, reference in rows:
        checker_compared += 1
        if checker == reference:
            checker_agreements += 1
        if llm_label is None:
            continue
        llm_compared += 1
        if llm_label == reference:
            llm_agreements += 1
    return {
        "checker_compared": checker_compared,
        "checker_agreements": checker_agreements,
        "llm_compared": llm_compared,
        "llm_agreements": llm_agreements,
    }
