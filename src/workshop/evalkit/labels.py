"""CSV of labels. The template shipped with the repo has a header and no rows."""

from __future__ import annotations

import csv
from pathlib import Path

HEADER = ("item_id", "text", "checker", "llm_judge", "reference_label", "human_label")


def _flag(raw: str) -> bool | None:
    value = raw.strip().casefold()
    if value == "":
        return None
    if value in {"pass", "true", "yes", "1"}:
        return True
    if value in {"fail", "false", "no", "0"}:
        return False
    raise ValueError(f"unrecognised label {raw!r}")


def summarize_label_csv(path: Path) -> dict[str, int]:
    """Count filled human labels against the reference column.

    Blank human labels are not agreements and not disagreements.
    """

    compared = 0
    agreements = 0
    data_rows = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or tuple(reader.fieldnames) != HEADER:
            raise ValueError("label csv header does not match the template")
        for row in reader:
            data_rows += 1
            human = _flag(row.get("human_label", "") or "")
            reference = _flag(row.get("reference_label", "") or "")
            if human is None or reference is None:
                continue
            compared += 1
            if human == reference:
                agreements += 1
    return {
        "data_rows": data_rows,
        "human_compared": compared,
        "human_agreements": agreements,
    }
