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


def read_csv_fieldnames(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        row = next(reader, [])
        return [item.strip() for item in row if item.strip()]


def write_csv(path: Path, fieldnames: Iterable[str], rows: list[dict[str, str]]) -> None:
    names = list(fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=names)
        writer.writeheader()
        for row in rows:
            normalized = {name: row.get(name, "") for name in names}
            writer.writerow(normalized)


def ensure_csv_header(path: Path, fieldnames: Iterable[str]) -> list[str]:
    expected = list(fieldnames)
    current = read_csv_fieldnames(path)

    if not current:
        write_csv(path, expected, [])
        return expected

    if current == expected:
        return current

    current_set = set(current)
    combined = list(current)
    for name in expected:
        if name not in current_set:
            combined.append(name)

    rows = read_csv_rows(path)
    write_csv(path, combined, rows)
    return combined


def append_csv_row(path: Path, row: dict[str, str], fieldnames: Iterable[str]) -> None:
    names = ensure_csv_header(path, fieldnames)
    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=names)
        normalized = {name: row.get(name, "") for name in names}
        writer.writerow(normalized)
