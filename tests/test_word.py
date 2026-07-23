import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.word_manager import WordManager

wm = WordManager()
wm.open("Project 1")
from app.word_manager import WordManager

wm = WordManager()

wm.open("Project 1")
