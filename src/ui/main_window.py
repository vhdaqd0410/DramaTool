from __future__ import annotations

import os
import shutil
import subprocess
import threading
import tkinter as tk
import winsound
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


from core.analyzer import build_rename_plan
from core.preview import render_preview
from core.task import run_rename_task
from utils.fileutil import parse_dropped_path


def next_pause_state(paused: bool) -> tuple[bool, str]:
    return (not paused, "继续" if not paused else "暂停")


def build_progress_text(processed: int, total: int) -> str:
    if total <= 0:
        return "已完成 0/0 个文件"
    percent = round(processed / total * 100, 1)
    return f"已完成 {processed}/{total} 个文件 ({percent:.1f}%)"


class MainWindow:
    def __init__(self, root: tk.Tk | None = None) -> None:
        self.root = root or tk.Tk()
        self.root.title("DramaTool")
        self.root.geometry("760x620")
        self.root.minsize(680, 520)
        self._enable_drag_drop()

        self.status_var = tk.StringVar(value="准备就绪，可选择剧集目录开始处理。")
        self.path_var = tk.StringVar(value="")
        self.output_dir_var = tk.StringVar(value="")
        self.is_renaming = False
        self.paused = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.rename_pairs: list[tuple[Path, Path]] = []
        self.total_files = 0
        self.success_count = 0
        self.error_count = 0
        self.processed_count = 0
        self.cancel_requested = False
        self.last_output_dir: Path | None = None
        self.rename_thread: threading.Thread | None = None

        title_label = ttk.Label(self.root, text="DramaTool", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=(16, 8))

        ttk.Label(self.root, text="当前目录：").pack(anchor="w", padx=24)
        ttk.Entry(self.root, textvariable=self.path_var, state="readonly").pack(fill="x", padx=24, pady=(4, 2))

        ttk.Label(self.root, text="输出目录：").pack(anchor="w", padx=24, pady=(8, 2))
        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill="x", padx=24, pady=(0, 8))
        ttk.Entry(output_frame, textvariable=self.output_dir_var).pack(side=tk.LEFT, fill="x", expand=True)
        ttk.Button(output_frame, text="选择输出目录", command=self.choose_output_directory).pack(side=tk.LEFT, padx=(8, 0))

        info_label = ttk.Label(self.root, textvariable=self.status_var, wraplength=650)
        info_label.pack(pady=(0, 10))

        self.preview_text = tk.Text(self.root, height=8, wrap="word")
        self.preview_text.pack(fill="both", expand=True, padx=24, pady=(0, 6))
        self.preview_text.insert(tk.END, "请先选择目录，然后点击“扫描”或“执行重命名”。")

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress = ttk.Progressbar(self.root, mode="determinate", variable=self.progress_var, maximum=100)
        self.progress.pack(fill="x", padx=24, pady=(0, 6))

        self.log_text = tk.Text(self.root, height=4, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=24, pady=(0, 6))
        self.log_text.insert(tk.END, "日志：\n")

        self.summary_var = tk.StringVar(value="等待扫描...")
        ttk.Label(self.root, textvariable=self.summary_var, wraplength=500).pack(anchor="w", padx=24, pady=(0, 4))

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=(6, 12))

        self.select_button = ttk.Button(button_frame, text="选择目录", command=self.choose_directory)
        self.select_button.pack(side=tk.LEFT, padx=8)
        self.scan_button = ttk.Button(button_frame, text="扫描", command=self.scan_directory)
        self.scan_button.pack(side=tk.LEFT, padx=8)
        self.run_button = ttk.Button(button_frame, text="执行重命名", command=self.execute_rename)
        self.run_button.pack(side=tk.LEFT, padx=8)
        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.toggle_pause, state="disabled")
        self.pause_button.pack(side=tk.LEFT, padx=8)
        self.cancel_button = ttk.Button(button_frame, text="取消任务", command=self.cancel_rename, state="disabled")
        self.cancel_button.pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="保存日志", command=self.save_log).pack(side=tk.LEFT, padx=8)
        ttk.Button(button_frame, text="退出", command=self.root.destroy).pack(side=tk.LEFT, padx=8)

    def _enable_drag_drop(self) -> None:
        try:
            self.root.drop_target_register("DND_Files")
            self.root.dnd_bind("<<Drop>>", self._handle_drop)
        except (AttributeError, tk.TclError):
            return

    def choose_directory(self) -> None:
        path = filedialog.askdirectory(title="选择剧集目录")
        if path:
            folder = Path(path)
            self.path_var.set(str(folder))
            self.scan_directory()

    def choose_output_directory(self) -> None:
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_dir_var.set(path)

    def _handle_drop(self, event: tk.Event) -> None:
        dropped_path = parse_dropped_path(event.data)
        if dropped_path is None:
            messagebox.showwarning("提示", "请拖入一个存在的文件夹或文件。")
            return

        if dropped_path.is_file():
            dropped_path = dropped_path.parent

        self.path_var.set(str(dropped_path))
        self.status_var.set(f"已通过拖拽读取目录：{dropped_path}")

        answer = messagebox.askyesno("拖拽处理", "是否直接开始重命名？\n\n选择“是”会直接执行重命名，选择“否”只进行扫描预览。")
        if answer:
            self.execute_rename()
        else:
            self.scan_directory()

    def scan_directory(self) -> None:
        folder = Path(self.path_var.get())
        if not folder.exists():
            messagebox.showwarning("提示", "请先选择目录。")
            return

        output_dir = Path(self.output_dir_var.get()).expanduser() if self.output_dir_var.get() else None
        items = build_rename_plan(folder, output_dir=output_dir, mode="split_merge")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, render_preview(items))
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, f"日志：\n扫描完成，发现 {len(items)} 个可处理文件。")
        self.log_text.see(tk.END)
        self.progress_var.set(0.0)
        self.summary_var.set(f"扫描结果：{len(items)} 个可处理文件")
        if items:
            self.status_var.set(f"已扫描目录：{folder}，共检测到 {len(items)} 个可处理文件。")
        else:
            self.status_var.set(f"已扫描目录：{folder}，但没有匹配到可处理的集数文件。")

    def execute_rename(self) -> None:
        if self.is_renaming:
            return

        folder = Path(self.path_var.get())
        if not folder.exists():
            messagebox.showwarning("提示", "请先选择目录。")
            return

        output_dir = Path(self.output_dir_var.get()).expanduser() if self.output_dir_var.get() else None
        items = build_rename_plan(folder, output_dir=output_dir, mode="split_merge")
        if not items:
            messagebox.showinfo("提示", "当前目录没有可执行的重命名项。")
            return

        conflicts = [item.target for item in items if item.target.exists() and item.target != item.source]
        if conflicts:
            conflict_names = "\n".join(str(item) for item in conflicts)
            messagebox.showwarning("提示", f"存在目标冲突，无法继续执行：\n{conflict_names}")
            return

        self.rename_pairs = [(item.source, item.target) for item in items if item.source != item.target]
        target_dir = output_dir or folder.with_name(f"{folder.name}_renamed")
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "日志：\n")
        self.log_text.insert(tk.END, f"输出目录：{target_dir}\n")
        self.progress_var.set(0.0)
        self.total_files = len(self.rename_pairs)
        self.success_count = 0
        self.error_count = 0
        self.processed_count = 0
        self.is_renaming = True
        self.paused = False
        self.cancel_requested = False
        self.pause_event.set()
        self.last_output_dir = target_dir
        self.log_text.insert(tk.END, f"准备处理 {self.total_files} 个文件。\n")
        self.summary_var.set(f"准备处理：{self.total_files} 个文件")
        self.pause_button.configure(text="暂停", state="normal")
        self.cancel_button.configure(state="normal")
        self.set_busy(True)
        self.rename_thread = threading.Thread(target=self._run_rename_worker, daemon=True)
        self.rename_thread.start()

    def _run_rename_worker(self) -> None:
        def on_progress(index: int, source: Path, target: Path, success: bool, error: Exception | None) -> None:
            if success:
                self.success_count += 1
            else:
                self.error_count += 1
            self.root.after(0, self._update_progress, index, source, target, success, error)

        def on_complete(cancelled: bool) -> None:
            self.root.after(0, self._finish_rename, cancelled)

        run_rename_task(
            pairs=self.rename_pairs,
            should_cancel=lambda: self.cancel_requested or not self.is_renaming,
            should_pause=lambda: not self.pause_event.is_set() and not self.cancel_requested and self.is_renaming,
            on_progress=on_progress,
            on_complete=on_complete,
        )

    def _update_progress(self, index: int, source: Path, target: Path, success: bool, error: Exception | None) -> None:
        total = self.total_files
        self.processed_count = index
        version = source.parent.name
        source_display = f"{version}/{source.name}"
        split_tag = " ← 拆集" if "-" in source.stem else ""
        if success:
            self.log_text.insert(tk.END, f"  [{index}/{total}] {source_display} -> {target.name}{split_tag}\n")
        else:
            self.log_text.insert(tk.END, f"  [{index}/{total}] 失败: {source_display} -> {target.name} ({error})\n")
        self.log_text.see(tk.END)
        percent = int(index / total * 100) if total else 100
        self.progress_var.set(percent)
        self.status_var.set(f"正在处理 {index}/{total} 个文件... {build_progress_text(index, total)}")
        self.summary_var.set(f"进度：{build_progress_text(index, total)}")

    def _finish_rename(self, cancelled: bool = False) -> None:
        self.is_renaming = False
        self.paused = False
        self.pause_event.set()
        self.pause_button.configure(text="暂停", state="disabled")
        self.cancel_button.configure(state="disabled")
        self.preview_text.delete("1.0", tk.END)
        if cancelled:
            self.preview_text.insert(tk.END, "任务已取消。")
            self.status_var.set(f"已取消，{build_progress_text(self.processed_count, self.total_files)}")
            self.log_text.insert(tk.END, f"已取消：已处理 {self.processed_count}/{self.total_files} 个文件。\n")
            self.summary_var.set(f"已取消：已处理 {self.processed_count}/{self.total_files} 个文件")
        else:
            self.preview_text.insert(tk.END, "重命名完成。")
            self.progress_var.set(100.0)
            self.status_var.set(f"重命名完成。{build_progress_text(self.processed_count, self.total_files)}")
            self.log_text.insert(tk.END, f"完成：成功 {self.success_count}，失败 {self.error_count}。\n")
            self.summary_var.set(f"完成：成功 {self.success_count}，失败 {self.error_count}")
            self._copy_screenshots_folder()
            self._open_output_directory()
            self._show_completion_dialog()
        self.set_busy(False)

    def toggle_pause(self) -> None:
        if not self.is_renaming:
            return

        self.paused, button_text = next_pause_state(self.paused)
        if self.paused:
            self.pause_event.clear()
            self.status_var.set(f"已暂停，{build_progress_text(self.processed_count, self.total_files)}")
            self.summary_var.set(f"暂停中：{build_progress_text(self.processed_count, self.total_files)}")
        else:
            self.pause_event.set()
            self.status_var.set(f"已继续处理，{build_progress_text(self.processed_count, self.total_files)}")
            self.summary_var.set(f"继续处理：{build_progress_text(self.processed_count, self.total_files)}")
        self.pause_button.configure(text=button_text)

    def cancel_rename(self) -> None:
        if not self.is_renaming:
            return
        self.cancel_requested = True
        self.pause_event.set()
        self.status_var.set(f"正在取消当前任务，{build_progress_text(self.processed_count, self.total_files)}")
        self.summary_var.set(f"取消中：{build_progress_text(self.processed_count, self.total_files)}")
        self.cancel_button.configure(state="disabled")

    def _open_output_directory(self) -> None:
        if not self.last_output_dir:
            return
        output_dir = self.last_output_dir
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        if hasattr(os, "startfile"):
            os.startfile(str(output_dir))
            return

        try:
            if os.name == "posix":
                subprocess.Popen(["open", str(output_dir)])
            else:
                subprocess.Popen(["xdg-open", str(output_dir)])
        except OSError:
            pass

    def _play_completion_sound(self) -> None:
        if self.error_count > 0:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        else:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def _copy_screenshots_folder(self) -> None:
        source_dir = Path(self.path_var.get()) / "4.工程截图"
        if not source_dir.is_dir():
            return
        target_dir = self.last_output_dir / "4.工程截图"
        try:
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
            self.log_text.insert(tk.END, "已复制「4.工程截图」文件夹。\n")
            self.log_text.see(tk.END)
        except OSError as exc:
            self.log_text.insert(tk.END, f"复制「4.工程截图」失败：{exc}\n")
            self.log_text.see(tk.END)

    def _show_completion_dialog(self) -> None:
        self._play_completion_sound()
        if self.success_count == 0 and self.error_count == 0:
            messagebox.showinfo("处理完成", "处理已完成。")
            return

        should_save = messagebox.askyesno(
            "处理完成",
            f"处理已完成。\n成功 {self.success_count} 个，失败 {self.error_count} 个。\n\n是否保存本次日志？",
        )
        if should_save:
            self.save_log()

    def save_log(self) -> None:
        log_path = filedialog.asksaveasfilename(
            title="保存日志",
            defaultextension=".log",
            filetypes=[("日志文件", "*.log"), ("文本文件", "*.txt"), ("所有文件", "*.*")],
        )
        if not log_path:
            return
        content = self.log_text.get("1.0", tk.END)
        Path(log_path).write_text(content, encoding="utf-8")
        messagebox.showinfo("提示", f"日志已保存到：{log_path}")

    def set_busy(self, busy: bool) -> None:
        for button in (self.select_button, self.scan_button, self.run_button):
            button.state(["disabled"] if busy else ["!disabled"])
        self.pause_button.state(["!disabled"] if busy else ["disabled"])
        self.cancel_button.state(["!disabled"] if busy else ["disabled"])

    def run(self) -> None:
        self.root.mainloop()
