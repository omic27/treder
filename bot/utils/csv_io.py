from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]


def append_csv_row(path: Path, row: dict[str, str], fieldnames: Iterable[str]) -> None:
    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(fieldnames))
        writer.writerow(row)
