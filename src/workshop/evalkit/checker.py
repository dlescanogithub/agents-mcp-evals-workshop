"""Deterministic checker. It looks for a phrase. It is not a model judge.

The pass/fail marks next to the samples are reference labels written by the author.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceItem:
    text: str
    phrase: str
    reference_pass: bool


REFERENCE_ITEMS: tuple[ReferenceItem, ...] = (
    ReferenceItem("CD-240 is in bin B-1.", "bin B-1", True),
    ReferenceItem("The gasket kit is located in B-1.", "bin B-1", True),
    ReferenceItem("CD-240 is in bin B-1 and the recount matches the card.", "bin B-1", True),
    ReferenceItem("I could not find that SKU.", "bin B-1", False),
    ReferenceItem("bin B-1 holds the gasket kit.", "bin B-1", True),
    ReferenceItem("Stock was changed.", "bin B-1", False),
)


def deterministic_checker(text: str, phrase: str) -> bool:
    """True when the phrase occurs in the text. No model is called."""

    return phrase in text


@dataclass(frozen=True)
class CheckerReferenceReport:
    items: int
    agreements: int
    disagreements: int

    @property
    def ratio(self) -> float:
        if self.items == 0:
            return 0.0
        return self.agreements / self.items


def compare_checker_to_reference(
    items: tuple[ReferenceItem, ...] = REFERENCE_ITEMS,
) -> CheckerReferenceReport:
    """Compare the deterministic checker with reference labels written by the author."""

    agreements = 0
    for item in items:
        if deterministic_checker(item.text, item.phrase) == item.reference_pass:
            agreements += 1
    return CheckerReferenceReport(
        items=len(items),
        agreements=agreements,
        disagreements=len(items) - agreements,
    )
