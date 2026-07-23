from app.cloud import CloudManager
from app.cache import CacheManager
from app.config_manager import ConfigManager
import json

class QuestionManager:

    def __init__(self):
        self.cloud = CloudManager()
        self.cache = CacheManager()
        self.config = ConfigManager()


    def load(self):
        """
        Đọc questions.json từ Cloud.
        Nếu mất mạng thì đọc từ cache.
        """

        url = self.config.questions_url()

        try:

            print("Đang tải questions từ Cloud...")

            text = self.cloud.download_text(url)

            self.cache.save_text(
                "questions.json",
                text
            )

        except Exception as e:

            print("Lỗi Cloud:", e)
            print("Đọc questions từ cache...")

            text = self.cache.load_text(
                "questions.json"
            )

            if text is None:
                raise Exception(
                    "Không đọc được questions.json"
                )

        data = json.loads(text)

        return data["projects"]
