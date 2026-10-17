"""A literal stand-in for an LLM judge, plus a fixed human label set.

The judge is not a model. A live LLM judge is design-only and stays off.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationItem:
    text: str
    phrase: str
    human_pass: bool


CALIBRATION_ITEMS: tuple[CalibrationItem, ...] = (
    CalibrationItem("CD-240 is in bin B-1.", "bin B-1", True),
    CalibrationItem("The gasket kit is located in B-1.", "bin B-1", True),
    CalibrationItem("CD-240 is in bin B-1 and the recount matches the card.", "bin B-1", True),
    CalibrationItem("I could not find that SKU.", "bin B-1", False),
    CalibrationItem("bin B-1 holds the gasket kit.", "bin B-1", True),
    CalibrationItem("Stock was changed.", "bin B-1", False),
)


def literal_judge(text: str, phrase: str) -> bool:
    return phrase in text


@dataclass(frozen=True)
class CalibrationReport:
    items: int
    agreements: int
    disagreements: int

    @property
    def ratio(self) -> float:
        if self.items == 0:
            return 0.0
        return self.agreements / self.items


def calibrate(items: tuple[CalibrationItem, ...] = CALIBRATION_ITEMS) -> CalibrationReport:
    agreements = 0
    for item in items:
        if literal_judge(item.text, item.phrase) == item.human_pass:
            agreements += 1
    return CalibrationReport(
        items=len(items),
        agreements=agreements,
        disagreements=len(items) - agreements,
    )
