"""
==========================================
MOS Practice V15
Report Manager
==========================================
"""
import json
import os

from datetime import datetime

class ReportManager:

    def __init__(self, app):

        self.app = app

    def build_report(self):

        progress = self.app.progress.get_progress()

        return {

            "project_name":
                self.app.projects_data[
                    self.app.current_project_idx
                ]["name"],

            "project_index":
                self.app.current_project_idx,

            "completed":
                progress["completed"],

            "review":
                progress["review"],

            "remaining":
                progress["remaining"],

            "total":
                progress["total"],

            "elapsed_seconds":
                self.app.timer.elapsed_seconds
        }
    
    def save_report(self):

        report = self.build_report()

        os.makedirs(
            "reports",
            exist_ok=True
        )

        filename = datetime.now().strftime(
            "report_%Y-%m-%d_%H-%M-%S.json"
        )

        filepath = os.path.join(
            "reports",
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False
            )

        return filepath