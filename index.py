"""A small, self-contained desktop clock.

Run with:
    python index.py
"""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import ttk


class ClockApp(tk.Tk):
    """Interactive digital clock with common display preferences."""

    BACKGROUNDS = {
        "Dark": ("#111827", "#f9fafb", "#9ca3af", "#1f2937"),
        "Light": ("#f3f4f6", "#111827", "#4b5563", "#ffffff"),
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("Digital Clock")
        self.geometry("560x300")
        self.minsize(480, 260)
        self.configure(bg=self.BACKGROUNDS["Dark"][0])

        self.is_24_hour = tk.BooleanVar(value=True)
        self.show_seconds = tk.BooleanVar(value=True)
        self.theme = tk.StringVar(value="Dark")
        self.time_text = tk.StringVar()
        self.date_text = tk.StringVar()

        self._build_ui()
        self._apply_theme()
        self._update_clock()

    def _build_ui(self) -> None:
        self.content = tk.Frame(self, bd=0, highlightthickness=0)
        self.content.pack(expand=True, fill="both", padx=28, pady=24)

        self.time_label = tk.Label(
            self.content,
            textvariable=self.time_text,
            font=("Segoe UI", 54, "bold"),
        )
        self.time_label.pack(pady=(20, 0))

        self.date_label = tk.Label(
            self.content,
            textvariable=self.date_text,
            font=("Segoe UI", 16),
        )
        self.date_label.pack(pady=(0, 22))

        self.controls = tk.Frame(self.content)
        self.controls.pack(fill="x")

        self.format_check = ttk.Checkbutton(
            self.controls,
            text="24-hour",
            variable=self.is_24_hour,
            command=self._update_clock,
        )
        self.format_check.pack(side="left", padx=(8, 12))

        self.seconds_check = ttk.Checkbutton(
            self.controls,
            text="Show seconds",
            variable=self.show_seconds,
            command=self._update_clock,
        )
        self.seconds_check.pack(side="left", padx=12)

        self.theme_box = ttk.Combobox(
            self.controls,
            textvariable=self.theme,
            values=tuple(self.BACKGROUNDS),
            state="readonly",
            width=9,
        )
        self.theme_box.pack(side="right", padx=8)
        self.theme_box.bind("<<ComboboxSelected>>", self._on_theme_changed)

        ttk.Label(self.controls, text="Theme").pack(side="right")

    def _update_clock(self) -> None:
        now = datetime.now()
        if self.is_24_hour.get():
            time_format = "%H:%M:%S" if self.show_seconds.get() else "%H:%M"
        else:
            time_format = "%I:%M:%S %p" if self.show_seconds.get() else "%I:%M %p"

        self.time_text.set(now.strftime(time_format))
        self.date_text.set(
            f"{now.strftime('%A, %B')} {now.day}, {now.strftime('%Y')}"
        )

        self.after(200, self._update_clock)

    def _on_theme_changed(self, _event: tk.Event[tk.Misc]) -> None:
        self._apply_theme()

    def _apply_theme(self) -> None:
        background, foreground, secondary, panel = self.BACKGROUNDS[self.theme.get()]
        self.configure(bg=background)
        self.content.configure(bg=background)
        self.controls.configure(bg=panel)
        self.time_label.configure(bg=background, fg=foreground)
        self.date_label.configure(bg=background, fg=secondary)


if __name__ == "__main__":
    ClockApp().mainloop()