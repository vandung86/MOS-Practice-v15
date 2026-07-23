"""
==========================================
MOS Practice V15
Window Manager
==========================================
"""

import threading
import time

try:
    import win32gui
    import win32con
    import pygetwindow as gw
except ImportError:
    gw = None


class WindowManager:

    def __init__(self, root):

        self.root = root

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.app_height = 240
        self.position_mode = "bottom"

    def update_geometry(self):

        y = (
            self.screen_height - self.app_height - 40
            if self.position_mode == "bottom"
            else 0
        )

        self.root.geometry(
            f"{self.screen_width}x{self.app_height}+0+{y}"
        )

        self.root.update_idletasks()

    def toggle_position(self, keyword):

        self.position_mode = (
            "top"
            if self.position_mode == "bottom"
            else "bottom"
        )

        self.update_geometry()

        threading.Thread(
            target=self.autofit,
            args=(keyword,),
            daemon=True
        ).start()

    def autofit(self, keyword):

        if gw is None:
            return

        time.sleep(1.2)

        try:

            for window in gw.getAllWindows():

                if keyword.lower() in window.title.lower() \
                        or "word" in window.title.lower():

                    win32gui.ShowWindow(
                        window._hWnd,
                        win32con.SW_SHOWNORMAL
                    )

                    y = (
                        0
                        if self.position_mode == "bottom"
                        else self.app_height
                    )

                    win32gui.SetWindowPos(
                        window._hWnd,
                        win32con.HWND_NOTOPMOST,
                        0,
                        y,
                        self.screen_width,
                        self.screen_height
                        - self.app_height
                        - 45,
                        win32con.SWP_SHOWWINDOW
                    )

                    break

        except Exception:
            pass
