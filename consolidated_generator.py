#!/usr/bin/env python3
"""
Launcher script for Consolidated Mock Data Generator
This script allows users to run the generator from the root directory
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main generator
from mockgen.consolidated_generator import main

if __name__ == "__main__":
    main()
