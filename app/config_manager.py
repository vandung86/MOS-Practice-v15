"""
==========================================
MOS Practice V15
config_manager.py
Quản lý config.json
==========================================
"""

import json

from app.cloud import CloudManager
from app.cache import CacheManager
from app.config import CONFIG_URL, DOWNLOAD_TIMEOUT
from app.config import CONFIG_FILE


class ConfigManager:

    def __init__(self):

        self.cloud = CloudManager(DOWNLOAD_TIMEOUT)
        self.cache = CacheManager()
        self._config = None

    def load(self):
        """
        Đọc config.json từ Cloud.
        Nếu mất mạng thì đọc cache.
        """

        if self._config is not None:
            return self._config
        
        try:
            
            print("Đang tải config từ Cloud...")

            text = self.cloud.download_text(CONFIG_URL)

            print("===== CONFIG FROM CLOUD =====")
            print(text)
            print("=============================")

            self.cache.save_text(
                CONFIG_FILE.name,
                text
            )

        except Exception as e:

            print("Lỗi Cloud:", e)
            print("Đọc từ cache...")

            
            text = self.cache.load_text(
                CONFIG_FILE.name
            )

        if not text:
            raise Exception(
                "Không đọc được config.json"
            )

        self._config = json.loads(text)

        return self._config
    

    def version(self):
        """
        Trả về version của ứng dụng từ config.json
        """

        config = self.load()

        return config.get(
            "version",
            "Unknown"
        )


    def project_version(self, project_name):
        """
        Trả về version của Project.
        """

        config = self.load()

        projects = config["projects"]

        if project_name not in projects:

            raise Exception(
                f"{project_name} không tồn tại."
            )

        return projects[project_name]["version"]
    

    def questions_url(self):

        config = self.load()

        return config["questions"]

    
    def project_url(self, project_name):

        config = self.load()

        projects = config["projects"]

        if project_name not in projects:

            raise Exception(
                f"{project_name} không tồn tại."
            )

        return projects[project_name]["url"]

    
