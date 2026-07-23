"""
==========================================
MOS Practice V15
Update Manager
==========================================
"""

from app.cloud import CloudManager
from app.cache import CacheManager
from app.config_manager import ConfigManager
from app.logger_manager import LoggerManager


class UpdateManager:

    def __init__(self):

        self.cloud = CloudManager()

        self.cache = CacheManager()

        self.config = ConfigManager()

        self.logger = LoggerManager().logger

    def download_project(self, project_name):
        """
        Download Project từ Cloud và lưu vào cache.
        """

        self.logger.info(
            f"Downloading {project_name}"
        )

        url = self.config.project_url(
            project_name
        )

        data = self.cloud.download_binary(
            url
        )

        filename = f"{project_name}.docx"

        self.cache.save_binary(
            filename,
            data
        )

        self.logger.info(
            f"Saved {filename}"
        )

        return self.cache.get_file_path(
            filename
        )

    def download_questions(self):
        """
        Download questions.json từ Cloud.
        """

        url = self.config.questions_url()

        print("=" * 50)
        print("Questions URL:")
        print(url)
        print("=" * 50)

        data = self.cloud.download_text(
        url
        )

        print("=" * 50)
        print("Questions Download:")
        print(data[:200])      # chỉ in 200 ký tự đầu
        print("=" * 50)

        self.cache.save_text(
            "questions.json",
            data
        )

        return self.cache.get_file_path(
            "questions.json"
        )

    def need_download(self, project_name):
        """
        Kiểm tra Project có cần tải lại không.
        """

        # Version trên Cloud
        cloud_version = self.config.project_version(
            project_name
        )

        # Version trong Cache
        cache_version = self.cache.load_version(
            project_name
        )

        # Kiểm tra file Word
        filename = f"{project_name}.docx"

        file_exists = self.cache.get_file_path(
            filename
        ).exists()


        self.logger.info(
            f"Checking {project_name}"
        )

        self.logger.info(
            f"Cloud Version : {cloud_version}"
        )

        self.logger.info(
            f"Cache Version : {cache_version}"
        )

        self.logger.info(
            f"File Exists : {file_exists}"
        )



        if not file_exists:

            self.logger.warning(
                f"{project_name} not found in cache"
            )

            return True

        if cloud_version != cache_version:

            self.logger.warning(
                f"{project_name} needs update"
            )

            return True

        self.logger.info(
            f"{project_name} is up to date"
        )

            return False
    

