"""
Passli Live PASS/FAIL Desktop Automation Dashboard
==================================================
Compact, professional dark-themed Tkinter GUI for real-time monitoring
of Selenium WebDriver test execution. Built for live university presentations.
"""

import os
import sys
import queue
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from . import test_config
from .test_runner import TestSuiteRunner, NORMAL_TESTS, DEMO_TESTS


class PassliLiveDashboard:
    """Live Tkinter Dashboard coordinating threaded test runs and UI updates."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Passli — Selenium Test Automation Dashboard")
        self.root.geometry("820x640")
        self.root.minsize(680, 520)

        # Stay on top by default so recording captures both browser & dashboard
        self.always_on_top = True
        self.root.attributes("-topmost", self.always_on_top)

        # Thread-safe event queue and test runner
        self.queue = queue.Queue()
        self.runner = TestSuiteRunner(update_queue=self.queue)
        self.worker_thread = None

        # State tracking
        self.test_items = {}  # test_id -> tree item id
        self.current_suite = "normal"
        self.is_running = False

        # Theme Colors (Passli Dark Aesthetic)
        self.c_bg_main = "#0b1120"
        self.c_bg_card = "#0f172a"
        self.c_bg_header = "#1e293b"
        self.c_border = "#334155"
        self.c_text_main = "#f8fafc"
        self.c_text_muted = "#94a3b8"
        self.c_green = "#10b981"
        self.c_red = "#ef4444"
        self.c_yellow = "#f59e0b"
        self.c_blue = "#38bdf8"
        self.c_gray = "#64748b"

        self.root.configure(bg=self.c_bg_main)
        self._init_styles()
        self._build_ui()

        # Start periodic queue polling
        self.root.after(80, self._process_queue)

    def _init_styles(self):
        """Configure ttk styles for dark modern look."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview styling
        self.style.configure(
            "Custom.Treeview",
            background=self.c_bg_card,
            foreground=self.c_text_main,
            fieldbackground=self.c_bg_card,
            rowheight=26,
            font=("Segoe UI", 9),
            borderwidth=0,
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background=self.c_bg_header,
            foreground="#e2e8f0",
            font=("Segoe UI", 9, "bold"),
            borderwidth=1,
            relief="flat",
        )
        self.style.map("Custom.Treeview", background=[("selected", "#1e3a8a")])
        self.style.map("Custom.Treeview.Heading", background=[("active", "#334155")])

        # Progress bar styling
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.c_bg_header,
            background=self.c_green,
            thickness=10,
        )

    def _build_ui(self):
        """Build UI layout containing header, metrics cards, treeview, and controls."""
        main_container = tk.Frame(self.root, bg=self.c_bg_main, padx=14, pady=12)
        main_container.pack(fill=tk.BOTH, expand=True)

        # ----------------- Top Header -----------------
        header_frame = tk.Frame(main_container, bg=self.c_bg_main)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        title_box = tk.Frame(header_frame, bg=self.c_bg_main)
        title_box.pack(side=tk.LEFT)

        app_title = tk.Label(
            title_box,
            text="PASSLI TEST AUTOMATION DASHBOARD",
            font=("Segoe UI", 13, "bold"),
            fg=self.c_text_main,
            bg=self.c_bg_main,
        )
        app_title.pack(anchor="w")

        self.target_url_label = tk.Label(
            title_box,
            text=f"Target: {test_config.BASE_URL}  |  Engine: Selenium 4 Chrome",
            font=("Segoe UI", 8),
            fg=self.c_text_muted,
            bg=self.c_bg_main,
        )
        self.target_url_label.pack(anchor="w")

        # Top Right Status & Pin
        status_box = tk.Frame(header_frame, bg=self.c_bg_main)
        status_box.pack(side=tk.RIGHT)

        self.pin_btn = tk.Button(
            status_box,
            text="📌 On Top: ON",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg="#94a3b8",
            activebackground="#334155",
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            padx=6,
            pady=2,
            command=self._toggle_pin,
        )
        self.pin_btn.pack(side=tk.RIGHT, padx=(8, 0))

        self.status_badge = tk.Label(
            status_box,
            text="IDLE",
            font=("Segoe UI", 9, "bold"),
            fg="#94a3b8",
            bg="#1e293b",
            padx=10,
            pady=3,
            relief="flat",
        )
        self.status_badge.pack(side=tk.RIGHT)

        # ----------------- Metric Stat Cards -----------------
        metrics_frame = tk.Frame(main_container, bg=self.c_bg_main)
        metrics_frame.pack(fill=tk.X, pady=(0, 10))

        self.total_card = self._create_card(metrics_frame, "TOTAL TESTS", "0", self.c_blue)
        self.passed_card = self._create_card(metrics_frame, "PASSED", "0", self.c_green)
        self.failed_card = self._create_card(metrics_frame, "FAILED", "0", self.c_red)
        self.skipped_card = self._create_card(metrics_frame, "SKIPPED", "0", self.c_yellow)
        self.duration_card = self._create_card(metrics_frame, "DURATION", "0.0s", "#cbd5e1")

        # ----------------- Progress Bar -----------------
        self.prog_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            main_container,
            variable=self.prog_var,
            maximum=100.0,
            style="Custom.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        # ----------------- Live Test Matrix Treeview -----------------
        tree_frame = tk.Frame(main_container, bg=self.c_bg_card, bd=1, relief="solid")
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ("id", "name", "category", "status", "duration", "details")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse",
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Test Case Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("status", text="Status")
        self.tree.heading("duration", text="Time")
        self.tree.heading("details", text="Result / Failure Details")

        self.tree.column("id", width=75, anchor="center")
        self.tree.column("name", width=210, anchor="w")
        self.tree.column("category", width=95, anchor="center")
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("duration", width=65, anchor="center")
        self.tree.column("details", width=250, anchor="w")

        # Custom tag color coding
        self.tree.tag_configure("PASS", foreground=self.c_green)
        self.tree.tag_configure("FAIL", foreground=self.c_red)
        self.tree.tag_configure("RUNNING", foreground=self.c_yellow)
        self.tree.tag_configure("WAITING", foreground=self.c_gray)
        self.tree.tag_configure("SKIP", foreground=self.c_gray)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Double-click item shows popup detail
        self.tree.bind("<Double-1>", self._on_tree_double_click)

        # ----------------- Action Buttons Toolbar -----------------
        btn_frame = tk.Frame(main_container, bg=self.c_bg_main)
        btn_frame.pack(fill=tk.X)

        self.btn_normal = tk.Button(
            btn_frame,
            text="▶ Run Normal Suite (11)",
            font=("Segoe UI", 9, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self._start_suite("normal"),
        )
        self.btn_normal.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_demo = tk.Button(
            btn_frame,
            text="⚠ Run Intentional Failures (3)",
            font=("Segoe UI", 9, "bold"),
            bg="#b45309",
            fg="#ffffff",
            activebackground="#92400e",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self._start_suite("demo"),
        )
        self.btn_demo.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_all = tk.Button(
            btn_frame,
            text="⚡ Run All (14)",
            font=("Segoe UI", 9, "bold"),
            bg="#475569",
            fg="#ffffff",
            activebackground="#334155",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self._start_suite("all"),
        )
        self.btn_all.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_stop = tk.Button(
            btn_frame,
            text="⏹ Stop",
            font=("Segoe UI", 9, "bold"),
            bg="#be123c",
            fg="#ffffff",
            activebackground="#9f1239",
            activeforeground="#ffffff",
            bd=0,
            padx=10,
            pady=6,
            state=tk.DISABLED,
            cursor="hand2",
            command=self._stop_suite,
        )
        self.btn_stop.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_clear = tk.Button(
            btn_frame,
            text="🗑 Clear",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#cbd5e1",
            activebackground="#334155",
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self._clear_results,
        )
        self.btn_clear.pack(side=tk.LEFT, padx=(0, 6))

        # Right side utility buttons
        self.btn_report = tk.Button(
            btn_frame,
            text="🌐 Open HTML Report",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg=self.c_blue,
            activebackground="#334155",
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            padx=8,
            pady=5,
            cursor="hand2",
            command=self._open_html_report,
        )
        self.btn_report.pack(side=tk.RIGHT, padx=(6, 0))

        self.btn_screens = tk.Button(
            btn_frame,
            text="📸 Screenshots",
            font=("Segoe UI", 8),
            bg="#1e293b",
            fg="#94a3b8",
            activebackground="#334155",
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            padx=8,
            pady=5,
            cursor="hand2",
            command=self._open_screenshots_dir,
        )
        self.btn_screens.pack(side=tk.RIGHT)

        # Populate initial test catalog in Treeview
        self._populate_initial_tree("normal")

    def _create_card(self, parent, label_text, default_val, text_color):
        """Helper to create dark metric stat cards."""
        card = tk.Frame(parent, bg=self.c_bg_card, bd=1, relief="solid", padx=10, pady=8)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)

        lbl = tk.Label(card, text=label_text, font=("Segoe UI", 7, "bold"), fg=self.c_text_muted, bg=self.c_bg_card)
        lbl.pack(anchor="w")

        val = tk.Label(card, text=default_val, font=("Segoe UI", 14, "bold"), fg=text_color, bg=self.c_bg_card)
        val.pack(anchor="w")
        return val

    def _toggle_pin(self):
        """Toggle always-on-top window property."""
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        self.pin_btn.config(
            text="📌 On Top: ON" if self.always_on_top else "📌 On Top: OFF",
            fg="#38bdf8" if self.always_on_top else "#94a3b8",
        )

    def _populate_initial_tree(self, suite_type: str):
        """Populate Treeview rows with initial WAITING states."""
        self.tree.delete(*self.tree.get_children())
        self.test_items.clear()

        if suite_type == "normal":
            tests = NORMAL_TESTS
        elif suite_type == "demo":
            tests = DEMO_TESTS
        else:
            tests = NORMAL_TESTS + DEMO_TESTS

        for t in tests:
            t_id = t["id"]
            item_id = self.tree.insert(
                "",
                tk.END,
                values=(t_id, t["name"], t["category"], "WAITING", "—", t["description"]),
                tags=("WAITING",),
            )
            self.test_items[t_id] = item_id

        self.total_card.config(text=str(len(tests)))
        self.passed_card.config(text="0")
        self.failed_card.config(text="0")
        self.skipped_card.config(text="0")
        self.duration_card.config(text="0.0s")
        self.prog_var.set(0.0)

    def _start_suite(self, suite_type: str):
        """Launch background worker thread to run selected test suite."""
        if self.is_running:
            return

        self.is_running = True
        self.current_suite = suite_type
        self._populate_initial_tree(suite_type)

        # Update button states
        self.btn_normal.config(state=tk.DISABLED)
        self.btn_demo.config(state=tk.DISABLED)
        self.btn_all.config(state=tk.DISABLED)
        self.btn_clear.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        self.status_badge.config(text="RUNNING", bg="#854d0e", fg="#fef08a")

        # Spawn background thread
        self.worker_thread = threading.Thread(
            target=self.runner.run_suite,
            kwargs={"suite_type": suite_type, "headless": test_config.HEADLESS},
            daemon=True,
        )
        self.worker_thread.start()

    def _stop_suite(self):
        """Signal the test runner to halt after current test."""
        if self.is_running:
            self.runner.request_stop()
            self.status_badge.config(text="STOPPING...", bg="#991b1b", fg="#fecaca")
            self.btn_stop.config(state=tk.DISABLED)

    def _clear_results(self):
        """Reset dashboard tree and counters."""
        if self.is_running:
            return
        self._populate_initial_tree(self.current_suite)
        self.status_badge.config(text="IDLE", bg="#1e293b", fg="#94a3b8")

    def _open_html_report(self):
        """Open the generated HTML report in default browser."""
        report_path = test_config.REPORTS_DIR / "report.html"
        if report_path.exists():
            webbrowser.open(report_path.as_uri())
        else:
            messagebox.showinfo("Report Not Found", "Run tests first to generate an HTML execution report.")

    def _open_screenshots_dir(self):
        """Open screenshots directory in Windows Explorer."""
        if sys.platform == "win32":
            os.startfile(str(test_config.SCREENSHOTS_DIR))
        else:
            webbrowser.open(test_config.SCREENSHOTS_DIR.as_uri())

    def _on_tree_double_click(self, event):
        """Show detailed message dialog when double clicking a test row."""
        selected_item = self.tree.focus()
        if not selected_item:
            return
        vals = self.tree.item(selected_item, "values")
        if vals:
            msg = f"Test ID: {vals[0]}\nName: {vals[1]}\nCategory: {vals[2]}\nStatus: {vals[3]}\nDuration: {vals[4]}\n\nDetails:\n{vals[5]}"
            messagebox.showinfo(f"Test Details — {vals[0]}", msg)

    def _process_queue(self):
        """Check for updates from test runner worker thread (thread-safe)."""
        try:
            while True:
                event = self.queue.get_nowait()
                ev_type = event.get("type")
                data = event.get("data", {})

                if ev_type == "TEST_RUNNING":
                    t_id = data["test_id"]
                    if t_id in self.test_items:
                        item_id = self.test_items[t_id]
                        cur = list(self.tree.item(item_id, "values"))
                        cur[3] = "RUNNING"
                        cur[4] = "..."
                        self.tree.item(item_id, values=cur, tags=("RUNNING",))
                        self.tree.see(item_id)

                elif ev_type == "TEST_COMPLETED":
                    res = data["test"]
                    t_id = res["test_id"]
                    status = res["status"]
                    duration_str = f"{res['duration']}s"
                    detail = res.get("message", "")

                    if t_id in self.test_items:
                        item_id = self.test_items[t_id]
                        cur = list(self.tree.item(item_id, "values"))
                        cur[3] = status
                        cur[4] = duration_str
                        cur[5] = detail
                        tag = "FAIL" if status == "FAIL" else "PASS"
                        self.tree.item(item_id, values=cur, tags=(tag,))

                    # Update metric cards
                    self.passed_card.config(text=str(data["passed"]))
                    self.failed_card.config(text=str(data["failed"]))
                    self.skipped_card.config(text=str(data["skipped"]))

                    pct = (data["completed_count"] / max(data["total"], 1)) * 100.0
                    self.prog_var.set(pct)

                elif ev_type == "TEST_SKIPPED":
                    res = data
                    t_id = res["test_id"]
                    if t_id in self.test_items:
                        item_id = self.test_items[t_id]
                        cur = list(self.tree.item(item_id, "values"))
                        cur[3] = "SKIP"
                        cur[4] = "0.0s"
                        cur[5] = res["message"]
                        self.tree.item(item_id, values=cur, tags=("SKIP",))

                elif ev_type == "SUITE_COMPLETED":
                    self.is_running = False
                    self.btn_normal.config(state=tk.NORMAL)
                    self.btn_demo.config(state=tk.NORMAL)
                    self.btn_all.config(state=tk.NORMAL)
                    self.btn_clear.config(state=tk.NORMAL)
                    self.btn_stop.config(state=tk.DISABLED)

                    failed = data.get("failed", 0)
                    suite_t = data.get("suite_type", "")
                    dur = data.get("total_duration_seconds", 0.0)
                    self.duration_card.config(text=f"{dur}s")

                    if failed == 0:
                        self.status_badge.config(text="COMPLETED (ALL PASS)", bg="#065f46", fg="#a7f3d0")
                    elif suite_t == "demo":
                        self.status_badge.config(text="DEMO COMPLETED", bg="#854d0e", fg="#fef08a")
                    else:
                        self.status_badge.config(text=f"COMPLETED ({failed} FAIL)", bg="#991b1b", fg="#fecaca")

                elif ev_type == "SUITE_ERROR":
                    self.is_running = False
                    self.btn_normal.config(state=tk.NORMAL)
                    self.btn_demo.config(state=tk.NORMAL)
                    self.btn_all.config(state=tk.NORMAL)
                    self.btn_clear.config(state=tk.NORMAL)
                    self.btn_stop.config(state=tk.DISABLED)
                    self.status_badge.config(text="ERROR", bg="#991b1b", fg="#ffffff")
                    messagebox.showerror("Execution Error", data.get("error", "Unknown error"))

        except queue.Empty:
            pass
        finally:
            self.root.after(80, self._process_queue)


def launch_dashboard():
    """Application entry point to open Tkinter dashboard."""
    root = tk.Tk()
    app = PassliLiveDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    launch_dashboard()
