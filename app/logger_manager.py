"""
==========================================
MOS Practice V15
Logger Manager
==========================================
"""

import logging
import os


class LoggerManager:

    def __init__(self, base_path):

        log_dir = os.path.join(base_path, "logs")

        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "app.log")

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)   

    def error(self, message):
        logging.error(message)
