"""
==========================================
MOS Practice V15
Timer Manager
==========================================
"""


class TimerManager:

    def __init__(self, root, label):

        self.root = root
        self.label = label

        self.elapsed_seconds = 0

    def start(self):
        """
        Bắt đầu Timer
        """

        self.update()

    def update(self):
        """
        Cập nhật đồng hồ mỗi giây
        """

        self.elapsed_seconds += 1

        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60

        self.label.config(
            text=f"⏱ {minutes:02d}:{seconds:02d}"
        )

        if hasattr(self.root, "app"):

            try:
                self.root.app.update_dashboard()

            except Exception:
                pass
        
        self.root.after(
            1000,
            self.update
        )

    def reset(self):
        """
        Reset Timer
        """

        self.elapsed_seconds = 0

        self.label.config(
            text="⏱ 00:00"
        )
