# Project Structure Guide

## 📁 Clean Project Organization

Your project has been cleaned up and organized for better maintainability.

### 🎯 **Core Files (Keep These)**
```
Mockup_up_data/
├── README.md                           # 📚 Complete documentation
├── user_input.json                     # ⚙️ User configuration
├── master.json                         # 🎨 Master template
├── demo_enhanced_system.py             # 🚀 Demo script
├── generate_probability_outputs.py     # 🎲 Main probability generator
├── .gitignore                          # 🚫 Git ignore rules
└── src/mockgen/                        # 🔧 Core system modules
    ├── __init__.py                     # Package initialization
    ├── core.py                         # Main functionality
    └── cli.py                          # Command-line interface
```

### 🗑️ **Removed Files (No Longer Needed)**
- ❌ `generate_probabilities.bat` - Redundant Windows wrapper
- ❌ `generate_probabilities.ps1` - Redundant PowerShell wrapper  
- ❌ `pyproject.toml` - Package configuration (not needed)
- ❌ `src/mockgen.egg-info/` - Build artifacts
- ❌ `__pycache__/` - Python cache directories
- ❌ `*.pyc` - Compiled Python files

### 📂 **Output Directory**
- `mock_outputs/` - Generated mock data files (auto-created)

## 🚀 **How to Use**

### **Main Probability Generator:**
```bash
python generate_probability_outputs.py --all
python generate_probability_outputs.py --positive --count 5
python generate_probability_outputs.py --negative --model Model_1
```

### **Enhanced System (CLI):**
```bash
python -m src.mockgen.cli --enhanced
python -m src.mockgen.cli --model Model_1 --count 3
```

### **Demo Script:**
```bash
python demo_enhanced_system.py
```

## 🧹 **Maintenance**

### **Regular Cleanup (Run these commands periodically):**
```bash
# Remove Python cache files
Get-ChildItem -Recurse -Name "*.pyc" | Remove-Item -Force

# Remove cache directories
Get-ChildItem -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force

# Clean output directory (optional)
Remove-Item -Recurse -Force "mock_outputs/*"
```

### **What NOT to Delete:**
- ✅ `src/mockgen/` directory and its contents
- ✅ `user_input.json` and `master.json`
- ✅ `generate_probability_outputs.py`
- ✅ `demo_enhanced_system.py`
- ✅ `README.md` and `.gitignore`

## 🎯 **Benefits of This Organization**

1. **Cleaner Structure** - No redundant files
2. **Better Maintainability** - Clear separation of concerns
3. **Faster Development** - No build artifacts cluttering the workspace
4. **Version Control** - Proper `.gitignore` prevents committing unnecessary files
5. **Portability** - Works consistently across different environments

## 🔄 **Future Development**

When adding new features:
- Put core logic in `src/mockgen/core.py`
- Add CLI options in `src/mockgen/cli.py`
- Update documentation in `README.md`
- Test with `demo_enhanced_system.py`

This organization ensures your codebase remains clean and maintainable while preserving all functionality!
