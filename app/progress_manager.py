"""
==========================================
MOS Practice V15
Progress Manager
==========================================
"""


class ProgressManager:

    def __init__(self, app):

        self.app = app

    def get_progress(self):

        tasks = self.app.projects_data[
            self.app.current_project_idx
        ]["tasks"]

        total = len(tasks)

        completed = 0
        review = 0

        for i in range(total):

            status = self.app.task_statuses.get(
                (
                    self.app.current_project_idx,
                    i
                )
            )

            if status == "completed":
                completed += 1

            elif status == "review":
                review += 1

        remaining = total - completed - review

        return {
            "total": total,
            "completed": completed,
            "review": review,
            "remaining": remaining
        }