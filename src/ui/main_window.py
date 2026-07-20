from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core.analyzer import build_rename_plan
from core.merger import rename_files
from core.preview import render_preview


class MainWindow:
    def __init__(self, root: tk.Tk | None = None) -> None:
        self.root = root or tk.Tk()
        self.root.title("DramaTool")
        self.root.geometry("560x340")
        self.root.minsize(520, 300)

        self.status_var = tk.StringVar(value="准备就绪，可选择剧集目录开始处理。")
        self.path_var = tk.StringVar(value="")

        title_label = ttk.Label(self.root, text="DramaTool", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=(20, 8))

        ttk.Label(self.root, text="当前目录：").pack(anchor="w", padx=24)
        ttk.Entry(self.root, textvariable=self.path_var, state="readonly").pack(fill="x", padx=24, pady=(4, 8))

        info_label = ttk.Label(self.root, textvariable=self.status_var, wraplength=500)
        info_label.pack(pady=(0, 12))

        self.preview_text = tk.Text(self.root, height=10, wrap="word")
        self.preview_text.pack(fill="both", expand=True, padx=24, pady=(0, 8))
        self.preview_text.insert(tk.END, "请先选择目录，然后点击“扫描”或“执行重命名”。")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="选择目录", command=self.choose_directory).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="扫描", command=self.scan_directory).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="执行重命名", command=self.execute_rename).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="退出", command=self.root.destroy).pack(side=tk.LEFT, padx=8)

    def choose_directory(self) -> None:
        path = filedialog.askdirectory(title="选择剧集目录")
        if path:
            folder = Path(path)
            self.path_var.set(str(folder))
            self.scan_directory()

    def scan_directory(self) -> None:
        folder = Path(self.path_var.get())
        if not folder.exists():
            messagebox.showwarning("提示", "请先选择目录。")
            return

        items = build_rename_plan(folder)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, render_preview(items))
        if items:
            self.status_var.set(f"已扫描目录：{folder}，共检测到 {len(items)} 个可处理文件。")
        else:
            self.status_var.set(f"已扫描目录：{folder}，但没有匹配到可处理的集数文件。")

    def execute_rename(self) -> None:
        folder = Path(self.path_var.get())
        if not folder.exists():
            messagebox.showwarning("提示", "请先选择目录。")
            return

        items = build_rename_plan(folder)
        if not items:
            messagebox.showinfo("提示", "当前目录没有可执行的重命名项。")
            return

        conflicts = [item.target for item in items if item.target.exists() and item.target != item.source]
        if conflicts:
            conflict_names = "\n".join(str(item) for item in conflicts)
            messagebox.showwarning("提示", f"存在目标冲突，无法继续执行：\n{conflict_names}")
            return

        rename_pairs = [(item.source, item.target) for item in items if item.source != item.target]
        rename_files(rename_pairs)

        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, "重命名完成。")
        self.status_var.set(f"已完成 {len(items)} 个文件的处理。")

    def run(self) -> None:
        self.root.mainloop()
