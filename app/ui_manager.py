"""
==========================================
MOS Practice V15
UI Manager
==========================================
"""

import os
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from app.constants import UI, Status


class UIManager:

    def __init__(self, app):
        self.app = app

    def setup(self):
        # Bắt đầu tạo giao diện luôn, không gọi update_display ở đây
        top_bar = tk.Frame(self.app.root, bg=self.app.MOS_COLOR, height=self.app.ui_config.TOP_BAR_HEIGHT)
        top_bar.pack(fill="x", side="top")
        
        # BRANDING
        brand_frame = tk.Frame(top_bar, bg=self.app.MOS_COLOR)
        brand_frame.pack(side="left", padx=self.app.ui_config.DEFAULT_PADDING)
        try:
            logo_path = os.path.join(
                self.app.get_base_path(),
                "assets",
                "logo.png"
            )
            if os.path.exists(logo_path):
                self.app.logo_img = tk.PhotoImage(file=logo_path)
                tk.Label(brand_frame, image=self.app.logo_img, bg=self.app.MOS_COLOR).pack(side="left")
        except Exception:
            pass
        tk.Label(brand_frame, text=UI.BRAND_NAME, bg=self.app.MOS_COLOR, fg="white", font=self.app.ui_config.BRAND_FONT).pack(side="left", padx=self.app.ui_config.SMALL_PADDING)

        # CONTROLS
        left = tk.Frame(top_bar, bg=self.app.MOS_COLOR)
        left.pack(side="left", padx=self.app.ui_config.DEFAULT_PADDING)
        
        self.app.lbl_timer = tk.Label(left, text=UI.TIMER_DEFAULT, bg=self.app.theme.DARK, fg="white", font=self.app.ui_config.TIMER_FONT, padx=self.app.ui_config.DEFAULT_PADDING)
        self.app.lbl_timer.pack(side="left", padx=self.app.ui_config.SMALL_PADDING)
        self.create_btn(left, UI.BTN_POSITION, self.app.toggle_position, "#041b38", padx=8).pack(side="left", padx=self.app.ui_config.SMALL_PADDING)
        
        self.app.btn_select = tk.Menubutton(left, text=UI.BTN_SELECT_PROJECT, bg=self.app.theme.DARK, fg="white", font=self.app.ui_config.BUTTON_FONT, padx=8, pady=5, cursor="hand2")
        self.app.menu_proj = Menu(self.app.btn_select, tearoff=0)
        for i, p in enumerate(self.app.projects_data):
            self.app.menu_proj.add_command(label=p["name"], command=lambda idx=i: self.app.project.jump_to_project(idx))
        self.app.btn_select["menu"] = self.app.menu_proj
        self.app.btn_select.pack(side="left", padx=self.app.ui_config.SMALL_PADDING)

        # Title (Canh giữa)
        self.app.title_cont = tk.Frame(top_bar, bg=self.app.MOS_COLOR)
        self.app.title_cont.pack(side="left", expand=True)
        self.app.lbl_title_prefix = tk.Label(self.app.title_cont, bg=self.app.MOS_COLOR, fg="#A0AEC0", font=self.app.ui_config.TITLE_SMALL_FONT)
        self.app.lbl_title_prefix.pack(side="left")
        self.app.lbl_title_name = tk.Label(self.app.title_cont, bg=self.app.MOS_COLOR, fg="#FFFFFF", font=self.app.ui_config.TITLE_FONT)
        self.app.lbl_title_name.pack(side="left")

        # Right Group
        right = tk.Frame(top_bar, bg=self.app.MOS_COLOR)
        right.pack(side="right", padx=self.app.ui_config.DEFAULT_PADDING)
        self.create_btn(right, UI.BTN_RESTART, self.app.project.restart_project, "#4A5568").pack(side="left", padx=self.app.ui_config.SMALL_PADDING)
        self.create_btn(right, UI.BTN_SUBMIT, self.app.project.submit_project, "#059669").pack(side="left", padx=self.app.ui_config.SMALL_PADDING)
        self.create_btn(right, UI.BTN_CLOSE, self.app.close_application, "#C53030").pack(side="left", padx=self.app.ui_config.SMALL_PADDING)

        progress_container = tk.Frame(
            self.app.root,
            bg=self.app.theme.BACKGROUND
        )

        progress_container.pack(
            fill="x",
            padx=self.app.ui_config.LARGE_PADDING,
            pady=(5, 0)
        )

        self.app.lbl_progress = tk.Label(
            progress_container,
            text=UI.PROGRESS_DEFAULT,
            bg=self.app.theme.BACKGROUND,
            fg=self.app.theme.TEXT,
            font=self.app.ui_config.STATS_FONT
        )

        self.app.lbl_progress.pack(
            anchor="w",
            pady=(0, 2)
        )

        self.app.progress_bar = ttk.Progressbar(
            progress_container,
            orient="horizontal",
            mode="determinate",
            length=self.app.ui_config.PROGRESS_BAR_LENGTH
        )

        self.app.progress_bar.pack(
            fill="x"
        )

        dashboard = tk.Frame(
            self.app.root,
            bg=self.app.theme.BACKGROUND
        )

        dashboard.pack(
            fill="x",
            padx=self.app.ui_config.LARGE_PADDING,
            pady=(5, 5)
        )


        stats_frame = tk.Frame(
            dashboard,
            bg=self.app.theme.BACKGROUND
        )

        stats_frame.pack()

        self.app.lbl_completed = tk.Label(
            stats_frame,
            bg=self.app.theme.BACKGROUND,
            fg=self.app.theme.SUCCESS,
            font=self.app.ui_config.STATS_FONT
        )

        self.app.lbl_completed.pack(
            side="left",
            padx=self.app.ui_config.DEFAULT_PADDING
        )

        self.app.lbl_review = tk.Label(
            stats_frame,
            bg=self.app.theme.BACKGROUND,
            fg=self.app.theme.WARNING,
            font=self.app.ui_config.STATS_FONT
        )

        self.app.lbl_review.pack(
            side="left",
            padx=self.app.ui_config.DEFAULT_PADDING
        )

        self.app.lbl_remaining = tk.Label(
            stats_frame,
            bg=self.app.theme.BACKGROUND,
            fg=self.app.theme.TEXT,
            font=self.app.ui_config.STATS_FONT
        )

        self.app.lbl_remaining.pack(
            side="left",
            padx=self.app.ui_config.DEFAULT_PADDING
        )

        self.app.lbl_time = tk.Label(
            stats_frame,
            bg=self.app.theme.BACKGROUND,
            fg=self.app.theme.PRIMARY,
            font=self.app.ui_config.STATS_FONT
        )

        self.app.lbl_time.pack(
            side="left",
            padx=self.app.ui_config.DEFAULT_PADDING
        )
        

        
        self.app.task_bar = tk.Frame(self.app.root, bg=self.app.theme.BACKGROUND, height=self.app.ui_config.TASK_BAR_HEIGHT)
        self.app.task_bar.pack(fill="x")
        self.app.task_frame = tk.Frame(self.app.task_bar, bg=self.app.theme.BACKGROUND)
        self.app.task_frame.pack(pady=self.app.ui_config.SMALL_PADDING)
        
        # Khung văn bản (padx=self.app.ui_config.CONTENT_PADDING)
        self.app.instruction_container = tk.Frame(self.app.root, bg=self.app.theme.CARD, bd=1, relief="solid")
        self.app.instruction_container.pack(fill="x", padx=self.app.ui_config.CONTENT_PADDING, pady=self.app.ui_config.MEDIUM_PADDING) 
        
        self.app.lbl_inst = tk.Label(
            self.app.instruction_container,
            bg=self.app.theme.CARD,
            fg=self.app.theme.SECONDARY_TEXT,
            font=self.app.ui_config.TEXT_FONT,
            wraplength=self.app.ui_config.WRAP_LENGTH,
            justify="center",
            padx=self.app.ui_config.DEFAULT_PADDING,
            pady=self.app.ui_config.DEFAULT_PADDING)
        self.app.lbl_inst.pack(fill="both", expand=True)
        
        # Footer
        footer = tk.Frame(self.app.root, bg=self.app.theme.CARD, height=self.app.ui_config.FOOTER_HEIGHT)
        footer.pack(fill="x", side="bottom")
        btn_c = tk.Frame(footer, bg=self.app.theme.CARD)
        btn_c.pack(pady=5)
        self.create_btn(btn_c, UI.BTN_COMPLETE, lambda: self.app.project.mark_task(Status.COMPLETED), "#E2E8F0", "#4A5568", font=self.app.ui_config.SMALL_BUTTON_FONT, padx=12, pady=3).pack(side="left", padx=self.app.ui_config.DEFAULT_PADDING)
        self.create_btn(btn_c, UI.BTN_REVIEW, lambda: self.app.project.mark_task(Status.REVIEW), "#E2E8F0", "#4A5568", font=self.app.ui_config.SMALL_BUTTON_FONT, padx=12, pady=3).pack(side="left", padx=self.app.ui_config.DEFAULT_PADDING)
        
        # Cập nhật hiển thị sau khi đã khởi tạo toàn bộ giao diện
        # self.app.update_display()
        
    def create_btn(
        self,
        parent,
        text,
        cmd,
        bg,
        fg="white",
        font=None,
        padx=12,
        pady=5
    ):

        if font is None:
            font = self.app.ui_config.BUTTON_FONT
        
        return tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            font=font,
            bd=0,
            padx=padx,
            pady=pady,
            cursor="hand2"
        )
    
