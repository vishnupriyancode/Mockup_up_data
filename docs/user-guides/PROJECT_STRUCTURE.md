# Project Structure Guide

## 📁 Clean Project Organization

Your project has been cleaned up and organized for better maintainability with **enhanced features**.

### 🎯 **Core Files (Keep These)**
```
Mockup_up_data/
├── README.md                           # 📚 Complete documentation
├── user_input.json                     # ⚙️ User configuration (now includes Model_1_Exclusion)
├── master.json                         # 🎨 Master template
├── generate_probability_outputs.py     # 🎲 Enhanced probability generator
├── .gitignore                          # 🚫 Git ignore rules
└── src/mockgen/                        # 🔧 Enhanced core system modules
    ├── __init__.py                     # Package initialization
    ├── core.py                         # Enhanced functionality with master template integration
    └── cli.py                          # Enhanced command-line interface
```

### 🆕 **New Enhanced Features**
- ✅ **Model_1_Exclusion** - Added exclusion scenarios for comprehensive testing
- ✅ **Enhanced CLI Options** - New `--output-format` with split/multiple/single choices
- ✅ **Master Template Integration** - Improved merging of master template with user input
- ✅ **Split File Generation** - Generate separate files for each record
- ✅ **Record Numbering** - Better file naming with record numbers
- ✅ **Master Template Wrapping** - Probability outputs now wrapped in master template structure

### 🗑️ **Removed Files (No Longer Needed)**
- ❌ `demo_enhanced_system.py` - Demo script (not implemented in current version)
- ❌ `generate_probabilities.bat` - Redundant Windows wrapper
- ❌ `generate_probabilities.ps1` - Redundant PowerShell wrapper  
- ❌ `pyproject.toml` - Package configuration (not needed)
- ❌ `src/mockgen.egg-info/` - Build artifacts
- ❌ `__pycache__/` - Python cache directories
- ❌ `*.pyc` - Compiled Python files

### 📂 **Output Directory**
- `mock_outputs/` - Generated mock data files (auto-created with enhanced naming)

## 🚀 **How to Use (Enhanced)**

### **Enhanced CLI Interface:**
```bash
# Generate enhanced output with master template integration
python -m src.mockgen.cli --enhanced

# Generate split output files (one file per model)
python -m src.mockgen.cli --enhanced --output-format split

# Generate multiple records in separate files
python -m src.mockgen.cli --enhanced --output-format multiple --count 5

# Generate for specific models
python -m src.mockgen.cli --enhanced --models Model_1 Model_1_Positive Model_1_Exclusion

# Initialize template configuration
python -m src.mockgen.cli --init
```

### **Enhanced Probability Generator:**
```bash
# Generate all probability types with split files
python generate_probability_outputs.py --all --count 3 --split

# Generate only positive probabilities for specific model
python generate_probability_outputs.py --positive --model Model_1 --count 5

# Generate exclusion scenarios
python generate_probability_outputs.py --exclusion --model Model_1

# List available models
python generate_probability_outputs.py --list

# Custom configuration and output directory
python generate_probability_outputs.py --config my_config.json --output-dir custom_outputs --all
```

### **CLI Help and Documentation:**
```bash
# Enhanced CLI help
python -m src.mockgen.cli --help

# Probability generator help
python generate_probability_outputs.py --help
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
- ✅ `README.md` and `.gitignore`

## 🎯 **Benefits of Enhanced Organization**

1. **Cleaner Structure** - No redundant files
2. **Better Maintainability** - Clear separation of concerns
3. **Enhanced Features** - New CLI options and output formats
4. **Master Template Integration** - Better data consistency
5. **Exclusion Scenarios** - Comprehensive testing coverage
6. **Split File Generation** - Flexible output options
7. **Record Numbering** - Better file organization
8. **Faster Development** - No build artifacts cluttering the workspace
9. **Version Control** - Proper `.gitignore` prevents committing unnecessary files
10. **Portability** - Works consistently across different environments

## 🔄 **Future Development**

When adding new features:
- Put core logic in `src/mockgen/core.py`
- Add CLI options in `src/mockgen/cli.py`
- Update documentation in `README.md`
- Test with CLI commands and probability generator
- Consider adding new probability scenarios (e.g., Model_1_Edge_Case)

This enhanced organization ensures your codebase remains clean and maintainable while providing powerful new features for comprehensive mock data generation!
