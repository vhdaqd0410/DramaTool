from __future__ import annotations

from pathlib import Path
from typing import List

from core.analyzer import RenameItem


def render_preview(items: List[RenameItem]) -> str:
    if not items:
        return "没有检测到可处理的集数文件。请确认文件名包含第X集、01、EP01、S01E02 等常见格式。"
    lines = [f"共发现 {len(items)} 个可处理文件："]
    for item in items:
        lines.append(f"- {item.source.name} -> {item.target.name}")
    return "\n".join(lines)
