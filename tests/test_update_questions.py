"""
Test Update Questions
"""

import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.update_manager import UpdateManager

update = UpdateManager()

path = update.download_questions()

print("========== QUESTIONS TEST ==========")
print("Downloaded:")
print(path)
print("====================================")