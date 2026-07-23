"""
==========================================
MOS Practice V15
Exception Manager
==========================================
"""

from tkinter import messagebox


class ExceptionManager:

    def __init__(self, logger):
        self.logger = logger

    def handle(self, exception):

        self.logger.error(str(exception))

        messagebox.showerror(
            "Lỗi",
            str(exception)
        )