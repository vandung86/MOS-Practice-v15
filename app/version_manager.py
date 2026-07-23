"""
==========================================
MOS Practice V15
Version Manager
==========================================
"""

from app.config_manager import ConfigManager
from app.config import APP_VERSION


class VersionManager:

    def __init__(self):

        self.config = ConfigManager()

    def current_version(self):
        """
        Trả về phiên bản hiện tại của ứng dụng.
        """
        return APP_VERSION

    def cloud_version(self):
        """
        Trả về phiên bản mới nhất trên Cloud.
        """
        return self.config.version()

    def is_new_version(self):
        """
        So sánh phiên bản hiện tại và phiên bản trên Cloud.
        Trả về True nếu có phiên bản mới.
        """
        current = self.current_version()

        cloud = self.cloud_version()

        return current != cloud

    def check_update(self):
        """
        Kiểm tra và trả về thông tin cập nhật.
        """

        current = self.current_version()

        latest = self.cloud_version()

        need_update = self.is_new_version()

        return {
            "current": current,
            "latest": latest,
            "need_update": need_update
        }

    

        
