"""
Test Update Manager
"""

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.update_manager import UpdateManager

update = UpdateManager()

path = update.download_project(
    "Project 1"
)

print("========== UPDATE TEST ==========")
print("Downloaded:")
print(path)
print("=================================")