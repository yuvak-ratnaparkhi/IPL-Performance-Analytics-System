import os

# Get the directory where check_csv.py is located (the root)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct path pointing into the machine_learning/dataset folder
DATA_PATH = os.path.join(ROOT_DIR, "machine_learning", "dataset", "match_winner_dataset.csv")

print(f"🔍 Looking for file at: {DATA_PATH}")

try:
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("\n📋 HEADER LINE (Line 1):", lines[0].strip())
    
    # Check if the file even has 48 lines
    if len(lines) >= 48:
        print("⚠️ PROBLEM LINE (Line 48):", lines[47].strip())
    else:
        print(f"⚠️ File only has {len(lines)} lines! It might be empty or corrupted.")
        
except FileNotFoundError:
    print("\n❌ Still can't find it. Check the path above!")