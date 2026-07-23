"""
Test Config Manager
"""

import sys
from pathlib import Path

# Thêm thư mục gốc của project vào Python Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config_manager import ConfigManager


def main():

    print("=" * 50)
    print("MOS Practice V15 - Config Test")
    print("=" * 50)

    cfg = ConfigManager()

    print("\nVersion:")
    print(cfg.version())

    print("\nQuestions URL:")
    print(cfg.questions_url())

    print("\nProject 1 URL:")
    print(cfg.project_url("Project 1"))

    print("\n✅ TEST PASSED")


if __name__ == "__main__":
    main()