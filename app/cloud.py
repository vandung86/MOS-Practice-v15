"""
==========================================
MOS Practice V15
Cloud Manager
==========================================
"""

import requests


class CloudManager:

    def __init__(self, timeout=10):
        self.timeout = timeout

    def download_text(self, url):
        """
        Download file text từ Google Drive
        """
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def download_binary(self, url):
        """
        Download file nhị phân (docx, pdf...)
        """
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.content
