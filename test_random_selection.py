#!/usr/bin/env python3
"""
Test script to demonstrate random selection from multiple edits.
This script shows how values are randomly selected from Edit_1 and Edit_2.
"""

import sys
import json
import random
from pathlib import Path

# Ensure local package in `src/` is importable without installation
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mockgen.core import load_user_config, _select_random_edit_and_record  # noqa: E402

def main():
    # Load the configuration
    config_path = Path("user_input.json")
    if not config_path.exists():
        print("Error: user_input.json not found!")
        return
    
    edits = load_user_config(config_path)
    print(f"Loaded {len(edits)} edits: {', '.join(edits.keys())}")
    print()
    
    # Show the available options for each edit
    for edit_key, edit_data in edits.items():
        print(f"=== {edit_key} ===")
        for field, choices in edit_data.items():
            print(f"  {field}: {choices}")
        print()
    
    # Generate 5 random selections to demonstrate
    print("=== Random Selections ===")
    for i in range(1, 6):
        edit_key, record = _select_random_edit_and_record(edits)
        print(f"Selection {i} (from {edit_key}):")
        for field, value in record.items():
            print(f"  {field}: {value}")
        print()

if __name__ == "__main__":
    main()
