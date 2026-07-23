import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.update_manager import UpdateManager

update = UpdateManager()

print(update.need_download("Project 1"))