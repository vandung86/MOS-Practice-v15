"""
Test Version Manager
"""

import sys
import os

# Thêm thư mục gốc của project vào Python Path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.version_manager import VersionManager

vm = VersionManager()

info = vm.check_update()

print("========== VERSION TEST ==========")
print(f"Current Version : {info['current']}")
print(f"Cloud Version   : {info['latest']}")
print(f"Need Update     : {info['need_update']}")
print("==================================")