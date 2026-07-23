"""
==========================================
MOS Practice V15
Update Manager
==========================================
"""

from app.cloud import CloudManager
from app.cache import CacheManager
from app.config_manager import ConfigManager



class UpdateManager:

    def __init__(self, logger):

        self.cloud = CloudManager()

        self.cache = CacheManager()

        self.config = ConfigManager()

        self.logger = logger

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

        cloud_version = self.config.project_version(
            project_name
        )

        self.cache.save_version(
            project_name,
            cloud_version
        )

        self.logger.info(
            f"Saved version {cloud_version}"
        )

        return self.cache.get_file_path(
            filename
        )
     
    
    def download_questions(self):
        """
        Download questions.json từ Cloud.
        """

        url = self.config.questions_url()

        self.logger.info(
            f"Questions URL: {url}"
        )

        data = self.cloud.download_text(
        url
        )

        self.logger.info(
            "Questions downloaded successfully"
        )

        self.logger.info(
            f"Preview: {data[:100]}"
        )

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

    def prepare_project(self, project_name):
        """
        Chuẩn bị Project trước khi mở.
        """

        if self.need_download(project_name):

            print("Project cần cập nhật -> Download")

            self.logger.info(
                f"Updating {project_name}"
            )

            path = self.download_project(project_name)

        else:

            filename = f"{project_name}.docx"

            path = self.cache.get_file_path(filename)

        return path

