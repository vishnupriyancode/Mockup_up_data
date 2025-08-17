# 📋 Complete Command Reference for JSON Generation

## 🚀 **Mock Data Generation System - Command Reference**

This document provides a comprehensive list of all available commands for users to generate JSONs using the Mock Data Generation System.

---

## 🎯 **Primary Commands (Recommended)**

### **1. Consolidated Generator (Main Tool)**
```bash
# Generate all scenarios for all models
python consolidated_generator.py --all --wgs

# Generate positive scenarios (disabled for Model_1)
python consolidated_generator.py --positive --model Model_1

# Generate negative scenarios
python consolidated_generator.py --negative --model Model_1

# Generate exclusion scenarios
python consolidated_generator.py --exclusion --model Model_1

# Generate combined output
python consolidated_generator.py --combined

# Generate project report
python consolidated_generator.py --report

# List available models
python consolidated_generator.py --list
```

### **2. CLI Module Commands**
```bash
# Generate positive scenarios (requires --wgs flag)
python -m src.mockgen.cli --probability --positive --model Model_1 --wgs

# Generate negative scenarios (requires --wgs flag)
python -m src.mockgen.cli --probability --negative --model Model_1 --wgs

# Generate exclusion scenarios (requires --wgs flag)
python -m src.mockgen.cli --probability --exclusion --model Model_1 --wgs

# Generate all scenario types (requires --wgs flag)
python -m src.mockgen.cli --probability --all --model Model_1 --wgs

# List available models
python -m src.mockgen.cli --list
```

---

## 🎯 **Command Options & Parameters**

### **Core Arguments**
- `--positive`: Generate positive scenarios
- `--negative`: Generate negative scenarios  
- `--exclusion`: Generate exclusion scenarios
- `--all`: Generate all scenario types (requires `--wgs` flag)
- `--combined`: Generate combined output file
- `--list`: List available models and scenarios
- `--report`: Generate project report

### **Additional Options**
- `--model MODEL`: Specify model name (e.g., Model_1, Model_2)
- `--count COUNT`: Number of records to generate (default: 1, max: 100)
- `--split`: Generate separate files for each record
- `--wgs`: Use WGS format for output (complete template structure)
- `--config CONFIG`: Path to config file (default: `user_input.json`)
- `--output-dir OUTPUT_DIR`: Output directory (default: `generated_outputs`)

---

## 📚 **Usage Examples by Scenario Type**

### **Positive Scenarios**
```bash
# Single positive scenario
python consolidated_generator.py --positive --model Model_1

# Multiple positive scenarios
python consolidated_generator.py --positive --model Model_1 --count 5

# With WGS format
python consolidated_generator.py --positive --model Model_1 --wgs --count 3
```

### **Negative Scenarios**
```bash
# Single negative scenario
python consolidated_generator.py --negative --model Model_1

# Multiple negative scenarios
python consolidated_generator.py --negative --model Model_1 --count 5

# With WGS format
python consolidated_generator.py --negative --model Model_1 --wgs --count 3
```

### **Exclusion Scenarios**
```bash
# Single exclusion scenario
python consolidated_generator.py --exclusion --model Model_1

# Multiple exclusion scenarios
python consolidated_generator.py --exclusion --model Model_1 --count 5

# With WGS format
python consolidated_generator.py --exclusion --model Model_1 --wgs --count 3
```

### **All Scenarios Combined**
```bash
# Generate all scenario types for all models
python consolidated_generator.py --all --wgs

# Generate all scenarios for specific model
python consolidated_generator.py --all --wgs --model Model_1

# Generate multiple records of each type
python consolidated_generator.py --all --wgs --count 5 --split
```

---

## 🎮 **Interactive Options**

### **Batch Files (Windows)**
```bash
# Interactive menu
scripts/consolidated_generator.bat

# Or run from root
run_consolidated_generator.bat
```

### **Help Commands**
```bash
# Get help for consolidated generator
python consolidated_generator.py --help

# Get help for CLI module
python -m src.mockgen.cli --help
```

---

## ⚠️ **Important Notes**

1. **Model_1 Restrictions**: Positive scenario generation is disabled for Model_1
2. **WGS Flag Required**: CLI module requires `--wgs` flag for all scenario generation
3. **File Output**: Each scenario generates separate JSON files (not arrays in single files)
4. **Count Limit**: Maximum count is 100 records per scenario type
5. **Configuration**: Uses `user_input.json` as default configuration file

---

## 🚀 **Quick Start Commands**

```bash
# 1. List available models first
python consolidated_generator.py --list

# 2. Generate negative scenarios for Model_1
python consolidated_generator.py --negative --model Model_1

# 3. Generate all scenarios with WGS format
python consolidated_generator.py --all --wgs

# 4. Generate project report
python consolidated_generator.py --report
```

---

## 📁 **File Structure**

```
Mockup_up_data/
├── consolidated_generator.py          # Main launcher script
├── run_consolidated_generator.bat    # Root batch file
├── scripts/
│   └── consolidated_generator.bat    # Interactive menu batch file
├── src/mockgen/
│   ├── consolidated_generator.py     # Main generator logic
│   ├── cli.py                        # CLI interface
│   └── core.py                       # Core functionality
├── user_input.json                   # Configuration file
└── generated_outputs/                # Output directory
```

---

## 🔧 **Configuration**

The system uses `user_input.json` as the default configuration file. This file contains:
- Model definitions
- Field mappings
- Probability scenarios
- Data templates

---

## 📊 **Output**

Generated files are saved in the `generated_outputs/` directory with timestamps and descriptive names.

---

## 🛠️ **Troubleshooting**

If you encounter the error "No such file or directory" for `consolidated_generator.py`, make sure you're running the command from the root directory of the project.

The system automatically handles:
- Path resolution
- Configuration loading
- Output directory creation
- Error handling and validation

---

## 📖 **Additional Documentation**

For more detailed information, refer to:
- `MASTER_REFERENCE.md` - Comprehensive system documentation
- `docs/` directory - Additional documentation files
- `user_input.json` - Configuration examples
- `master.json` - Template structure reference
