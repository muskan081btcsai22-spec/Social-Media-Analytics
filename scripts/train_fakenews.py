"""Train the fake-news model and save to models/fakenews.pkl

Usage:
  python scripts/train_fakenews.py
"""
import os
import sys

# ensure project root is on sys.path so `modules` imports work
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from modules.fakenews import train_model

CSV_PATH = os.path.join(ROOT, 'WELFake_Dataset.csv')

if __name__ == '__main__':
    if not os.path.exists(CSV_PATH):
        print('Training CSV not found at', CSV_PATH)
        sys.exit(1)
    print('Training fake-news model from', CSV_PATH)
    res = train_model(CSV_PATH)
    print(res)
