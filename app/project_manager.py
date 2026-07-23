"""
==========================================
MOS Practice V15
Project Manager
==========================================
"""

from app.constants import Message
from app.dialog_manager import DialogManager

class ProjectManager:

    def __init__(self, app):
        self.app = app

    def select_task(self, idx):
        self.app.current_task_idx = idx
        self.app.update_display()

    def next_task(self):
        if self.app.current_task_idx < len(
            self.app.projects_data[self.app.current_project_idx]["tasks"]
        ) - 1:
            self.select_task(self.app.current_task_idx + 1)

    def prev_task(self):
        if self.app.current_task_idx > 0:
            self.select_task(self.app.current_task_idx - 1)

    def mark_task(self, status):
        key = (
            self.app.current_project_idx,
            self.app.current_task_idx
        )

        self.app.task_statuses[key] = status

        self.app.update_display()

    def jump_to_project(self, idx):

        self.app.logger.info(
            f"Jump To Project: {idx + 1}"
        )

        self.app.close_word_without_saving(
            self.app.projects_data[
                self.app.current_project_idx
            ]["name"]
        )

        self.app.current_project_idx = idx
        self.app.current_task_idx = 0

        self.app.update_display()

        self.app.open_word_file_for_project(idx)

    def restart_project(self):
        
        print("RESTART CLICKED")

        if DialogManager.ask(
            Message.RESTART_TITLE,
            Message.RESTART_CONFIRM
        ):

            self.app.logger.info("Restart Project")

            self.app.close_word_without_saving(
                self.app.projects_data[
                    self.app.current_project_idx
                ]["name"]
            )

            self.app.open_word_file_for_project(
                self.app.current_project_idx
            )

            

    def submit_project(self):

        
        print("=" * 60)
        print("SUBMIT CLICKED")
        print("Current Project:", self.app.current_project_idx)
        print("Total Projects :", len(self.app.projects_data))
        print("=" * 60)

        if DialogManager.askyesno(
            Message.SUBMIT_TITLE,
            Message.SUBMIT_CONFIRM
        ):

            print("USER CLICKED YES")

            self.app.logger.info("Submit Project")

            try:
                self.app.report.save_report()

            except Exception as e:
                self.app.exception.handle(e)
                return

            self.app.close_word_without_saving(
                self.app.projects_data[
                    self.app.current_project_idx
                ]["name"]
            )

            if self.app.current_project_idx < len(self.app.projects_data) - 1:

                print("Jump to:", self.app.current_project_idx + 1)

                self.jump_to_project(
                    self.app.current_project_idx + 1
                )

            else:

                print("LAST PROJECT")

                DialogManager.showinfo(
                    Message.FINISH_TITLE,
                    Message.FINISH_MESSAGE
                )
