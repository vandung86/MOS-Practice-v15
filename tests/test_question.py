import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.question_manager import QuestionManager

qm = QuestionManager()

projects = qm.load()

print("="*50)

print("Project:", len(projects))

print("="*50)

for p in projects:
    print(p["name"], len(p["tasks"]))