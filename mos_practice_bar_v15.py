import tkinter as tk
from tkinter import messagebox
import time, threading, os, sys
from app.question_manager import QuestionManager
from app.word_manager import WordManager
from app.window_manager import WindowManager
from app.timer_manager import TimerManager
from app.ui_manager import UIManager
from app.project_manager import ProjectManager
from app.session_manager import SessionManager
from app.progress_manager import ProgressManager
from app.report_manager import ReportManager
from app.theme_manager import ThemeManager
from app.ui_config import UIConfig
from app.constants import Status, UI
from app.logger_manager import LoggerManager
from app.constants import Message
from app.exception_manager import ExceptionManager
from app.version_manager import VersionManager


try:
    import win32gui, win32con, win32com.client, pygetwindow as gw
except ImportError:
    pass


class MOSPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.app = self
        self.root.title("MOS Practice Bar")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.theme = ThemeManager()
        self.ui_config = UIConfig()

        self.logger = LoggerManager(
            self.get_base_path()
        )

        self.version = VersionManager()

       
        info = self.version.check_update()

        print(info)

        self.exception = ExceptionManager(
            self.logger
        )

        self.logger.info("Application Started")
        
        
        # Window           
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.app_height = self.ui_config.APP_HEIGHT
        self.position_mode = "bottom"
        self.MOS_COLOR = self.theme.MOS_BLUE
        
        # Manager
        self.word_manager = WordManager(
            self.logger
        )

        self.word_manager.update.start_background_update()
        
        self.window_manager = WindowManager(self.root)
        self.ui = UIManager(self)
        
        self.session = SessionManager(
            self.logger
        )
        
        self.project = ProjectManager(self)
        self.question_manager = QuestionManager()
        self.progress = ProgressManager(self)
        self.report = ReportManager(self)
        self.version = VersionManager()

        # DATA
        self.projects_data = self.question_manager.load()

        session = self.session.load()
        
        self.task_statuses = {} 

        self.current_project_idx = 0
        self.current_task_idx = 0

        session = self.session.load()

        if session:

            self.current_project_idx = session.get(
                "project",
                0
            )

            self.current_task_idx = session.get(
                "task",
                0
            )

            self.position_mode = session.get(
                "position",
                "bottom"
            )

        # Ui
        self.window_manager.update_geometry()
        self.root.configure(bg="#F8FAFC")
        self.ui.setup()

        # Timer
        self.timer = TimerManager(
            self.root,
            self.lbl_timer
        )
        self.start_timer()

        self.update_display()

        if self.version.is_new_version():

            messagebox.showinfo(
                "Update Available",
                (
                    "Có phiên bản mới.\n\n"
                    f"Current: {self.version.current_version()}\n"
                    f"Latest : {self.version.cloud_version()}"
                )
            )

               #Open Project đầu tiên
        self.open_word_file_for_project(0)

                

    def get_base_path(self):
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))
         
    def close_word_without_saving(self, keyword=None):
        self.word_manager.close_without_saving(keyword)

    def close_application(self):

        self.logger.info(
            "Application Closed"
        )

        self.session.save(
            {
                "project": self.current_project_idx,
                "task": self.current_task_idx,
                "position": self.position_mode
            }
        )
        
        self.close_word_without_saving()
        self.root.destroy()
        sys.exit()

         
    # --- LOGIC ---
    def update_display(self):
        
        self.update_dashboard()

                        
        for w in self.task_frame.winfo_children(): w.destroy()
        tasks = self.projects_data[self.current_project_idx]["tasks"]
        self.lbl_title_prefix.config(text=f"Project {self.current_project_idx + 1} of {len(self.projects_data)}: ")
        self.lbl_title_name.config(
            text=(
                f"{self.projects_data[self.current_project_idx]['name']} "            
            )
        )
        
        # Nút Prev
        self.ui.create_btn(
            self.task_frame,
            "◀ Prev",
            self.prev_task,
            "#4A5568",
            font=self.ui_config.STATS_FONT,
            padx=10,
            pady=3
        ).pack(side="left", padx=10)
        
        for i in range(len(tasks)):
            status = self.task_statuses.get((self.current_project_idx, i))
            icon = " ✔" if status == "completed" else (" ⚐" if status == "review" else "")
            if status == "completed": bg = "#48BB78"
            elif status == "review": bg = "#ED8936"
            else: bg = "#3182CE" if i == self.current_task_idx else "#E2E8F0"
            fg = "white" if bg != "#E2E8F0" else "#4A5568"
            tk.Button(self.task_frame, text=f"{i+1}{icon}", bg=bg, fg=fg, bd=0, padx=10, pady=3, 
                      command=lambda idx=i: self.select_task(idx)).pack(side="left", padx=3)
        
        # Nút Next
        self.ui.create_btn(
            self.task_frame,
            "Next Task ▶",
            self.next_task,
            "#059669",
            font=self.ui_config.STATS_FONT,
            padx=10,
            pady=3
        ).pack(side="left", padx=10)
        
        self.lbl_inst.config(text=tasks[self.current_task_idx])
    
    def toggle_position(self):

        project_name = self.projects_data[
            self.current_project_idx
        ]["name"]

        self.window_manager.toggle_position(project_name)

    def select_task(self, idx):
        self.project.select_task(idx)
        
    def next_task(self):
        self.project.next_task()
        
    def prev_task(self):
        self.project.prev_task()
              
    
    def load_questions(self):
        return self.question_manager.load()

    
    def open_word_file_for_project(self, idx):
        
        try:

            project_name = self.projects_data[idx]["name"]

            self.logger.info(
                f"Open Project: {project_name}"
            )

            self.word_manager.open_project(
                project_name,
                self.window_manager
            )
            
        except Exception as e:

            self.exception.handle(e)
        
    
    def start_timer(self):
        self.timer.start()

    def update_dashboard(self):

        progress = self.progress.get_progress()

        percent = 0

        if progress["total"] > 0:
            percent = (
                progress["completed"] /
                progress["total"]
            ) * 100

        self.progress_bar["value"] = percent

        self.lbl_progress.config(
            text=f"Progress: {percent:.0f}%"
        )

        minutes = self.timer.elapsed_seconds // 60
        seconds = self.timer.elapsed_seconds % 60

        completed_percent = 0

        if progress["total"] > 0:

            completed_percent = (
                progress["completed"]
                * 100
                / progress["total"]
            )


        self.lbl_completed.config(
            text=f"Completed: {progress['completed']} ({completed_percent:.0f}%)"
        )

        self.lbl_review.config(
            text=f"Review: {progress['review']}"
        )

        self.lbl_remaining.config(
            text=f"Remaining: {progress['remaining']}"
        )
        
        self.lbl_time.config(
            text=f"Time: {minutes:02d}:{seconds:02d}"
        )

    
if __name__ == "__main__":
    root = tk.Tk()
    app = MOSPracticeApp(root)
    root.mainloop()
