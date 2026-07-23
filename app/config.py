"""
==========================================
MOS Practice V15
Config
==========================================
"""

from pathlib import Path

# Thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent

# Thư mục config
CONFIG_DIR = BASE_DIR / "config"

# Thư mục cache
CACHE_DIR = BASE_DIR / "cache"

# File config local
CONFIG_FILE = CONFIG_DIR / "config.json"

# URL config trên Google Drive
CONFIG_URL = "https://drive.google.com/uc?export=download&id=1h1U1zr9MUSNcgw5XsvRQyi3C3sOREb_f"

# Timeout khi tải file
DOWNLOAD_TIMEOUT = 10

# Phiên bản hiện tại của ứng dụng
APP_VERSION = "1.0.0"
