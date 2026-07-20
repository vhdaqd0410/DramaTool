from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class RenameItem:
    source: Path
    target: Path
    episode: int


def infer_episode_number(name: str) -> int | None:
    normalized = name.replace("\\", "/")

    season_episode_match = re.search(r"S(\d+)E(\d+)", normalized, re.IGNORECASE)
    if season_episode_match:
        return int(season_episode_match.group(2))

    patterns = [
        r"第\s*(\d{1,3})\s*集",
        r"(?:^|[^A-Za-z])EP(?:ISODE)?\s*(\d{1,3})(?![A-Za-z])",
        r"(?:^|[^A-Za-z])E(\d{1,3})(?![A-Za-z])",
        r"(?:^|[._\s-])(\d{1,3})(?:$|[._\s-])",
        r"(\d{1,3})集",
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if value <= 999:
                return value
    return None


def build_target_path(source: Path, episode: int, output_dir: Path) -> Path:
    suffix = source.suffix
    new_stem = f"{episode:02d}"
    return output_dir / f"{new_stem}{suffix}"


def build_rename_plan(folder: Path, output_dir: Path | None = None) -> List[RenameItem]:
    items: List[RenameItem] = []
    version_dirs = [p for p in sorted(folder.iterdir()) if p.is_dir()]
    if not version_dirs:
        version_dirs = [folder]

    resolved_output_dir = output_dir or folder.with_name(f"{folder.name}_renamed")
    resolved_output_dir.mkdir(parents=True, exist_ok=True)

    for version_dir in version_dirs:
        version_output_dir = resolved_output_dir / version_dir.name
        version_output_dir.mkdir(parents=True, exist_ok=True)

        version_items: List[RenameItem] = []
        for path in sorted(version_dir.rglob("*")):
            if not path.is_file():
                continue
            if infer_episode_number(path.name) is None:
                continue
            version_items.append(RenameItem(source=path, target=path, episode=0))

        for index, item in enumerate(version_items, start=1):
            relative_path = item.source.relative_to(folder)
            target_dir = resolved_output_dir / relative_path.parent
            target_dir.mkdir(parents=True, exist_ok=True)
            item.target = build_target_path(item.source, index, target_dir)
            item.episode = index
            items.append(item)

    return items
