import os

from app.update_manager import UpdateManager
from app.config import CACHE_DIR

class WordManager:

    def __init__(self, logger):

        self.logger = logger
        
        self.update = UpdateManager(
            self.logger
        )

    def start_background_update(self):
        """
        Khởi động cập nhật Project ở chế độ nền.
        """

        self.update.start_background_update()
    
    
    def open(self, project_name):
        """
        Mở file Word của Project.
        Nếu chưa có trong cache thì tải trước.
        """

        path = self.update.prepare_project(
            project_name
        )

        os.startfile(path)

        return path

    def close_without_saving(self, keyword=None):
        """
        Đóng file Word mà không lưu.
        """

        try:
            import win32com.client

            app = win32com.client.GetActiveObject("Word.Application")

            for doc in list(app.Documents):

                if keyword is None or (
                    doc.Name and keyword.lower() in doc.Name.lower()
                ):
                    doc.Close(SaveChanges=0)

            if app.Documents.Count == 0:
                app.Quit()

        except Exception:
            pass

    def open_project(self, project_name, window_manager):
        """
        Mở Project Word và tự động căn cửa sổ.
        """

        try:
            self.open(project_name)

            import threading

            threading.Thread(
                target=window_manager.autofit,
                args=(project_name,),
                daemon=True
            ).start()

        except Exception:

            raise

    

        
