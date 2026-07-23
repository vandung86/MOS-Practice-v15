"""
==========================================
MOS Practice V15
Cache Manager
==========================================
"""

from pathlib import Path

from app.config import CACHE_DIR


class CacheManager:

    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def save_text(self, filename, text):

        path = CACHE_DIR / filename

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def load_text(self, filename):

        path = CACHE_DIR / filename

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def save_binary(self, filename, data):
        """
        Lưu file nhị phân (docx, pdf...)
        """

        path = CACHE_DIR / filename

        with open(path, "wb") as f:
            f.write(data)

        return path


    def get_file_path(self, filename):
        """
        Trả về đường dẫn file trong cache.
        """

        return CACHE_DIR / filename

    def save_version(self, project_name, version):
        """
        Lưu version của Project.
        """

        filename = f"{project_name}.version"

        self.save_text(
            filename,
            version
        )


    def load_version(self, project_name):
        """
        Đọc version của Project.
        """

        filename = f"{project_name}.version"

        return self.load_text(
            filename
        )