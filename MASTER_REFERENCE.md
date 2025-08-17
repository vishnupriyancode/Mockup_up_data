# 🚀 Master Reference Guide - Mock Data Generation System

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [System Architecture](#system-architecture)
4. [Command Line Interface](#command-line-interface)
5. [Usage Examples](#usage-examples)
6. [Output Formats](#output-formats)
7. [File Management](#file-management)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Cleanup & Maintenance](#cleanup--maintenance)

---

## 🎯 Overview

This project provides a **consolidated mock data generation system** that eliminates redundancy and provides a single, comprehensive solution for generating mock data scenarios. The system supports probability types (positive, negative, exclusion) with configurable count parameters and generates separate JSON files for each requested scenario.

### ✨ Key Features

- **Probability Scenarios**: Generate positive, negative, and exclusion scenarios
- **Separate JSON Files**: Each scenario generates individual JSON files (not arrays in single files)
- **Configurable Count**: Generate multiple JSON files based on count parameters
- **Model Support**: Work with different models defined in configuration
- **Flexible Output**: Each scenario generates a separate, timestamped JSON file
- **Easy Management**: Simple to identify and manage individual test cases
- **No Repetition**: Each file contains exactly one complete scenario

### ⚠️ Important Note

**Positive scenario generation is disabled for Model_1** to prevent specific data conflicts. Use negative or exclusion scenarios for Model_1 instead.

---

## 🚀 Quick Start

### Option 1: Interactive Batch File (Windows)
```bash
# Double-click to run
consolidated_generator.bat
```

### Option 2: Python Script
```bash
# Generate all scenarios for all models
python consolidated_generator.py --all

# Generate positive scenarios for specific model
python consolidated_generator.py --positive --model Model_1

# Generate WGS format scenarios
python consolidated_generator.py --wgs --negative

# Get help
python consolidated_generator.py --help
```

### Option 3: Direct CLI Commands
```bash
# List available models
python -m src.mockgen.cli --list

# Generate positive scenarios (DISABLED for Model_1)
# python -m src.mockgen.cli --probability --positive --model Model_1

# Generate multiple scenarios (DISABLED for Model_1)
# python -m src.mockgen.cli --probability --positive --model Model_1 --count 5

# Generate negative scenarios for Model_1
python -m src.mockgen.cli --probability --negative --model Model_1

# Generate exclusion scenarios for Model_1
python -m src.mockgen.cli --probability --exclusion --model Model_1
```

---

## 🏗️ System Architecture

### Project Structure
```
Mockup_up_data/
├── src/mockgen/           # Core system (don't modify)
│   ├── __init__.py
│   ├── cli.py            # Command-line interface
│   └── core.py           # Core business logic
├── consolidated_generator.py    # Main Python script
├── consolidated_generator.bat   # Interactive Windows interface
├── user_input.json              # Your data configuration
├── master.json                  # Template structure
├── requirements.txt             # Dependencies
└── generated_outputs/           # Output directory
```

### Core Components
- **`cli.py`**: Command-line interface and argument parsing
- **`core.py`**: Core business logic for scenario generation
- **`consolidated_generator.py`**: Unified Python interface
- **`consolidated_generator.bat`**: Interactive Windows interface

---

## 💻 Command Line Interface

### Key Behavior: Separate JSON Files

**Important**: When using the `--count` parameter, the CLI generates separate JSON files, each containing a single JSON object. This is different from generating arrays with multiple objects in a single file.

**Example**: `--count 3` generates 3 separate files:
- `Model_1_positive_20250816_100632_000001.json` (contains 1 JSON object)
- `Model_1_positive_20250816_100632_000002.json` (contains 1 JSON object)  
- `Model_1_positive_20250816_100632_000003.json` (contains 1 JSON object)

### Command Line Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `--probability` | Yes* | Flag to indicate probability scenario generation | - |
| `--positive` | Yes* | Generate positive scenarios (disabled for Model_1) | - |
| `--negative` | Yes* | Generate negative scenarios | - |
| `--exclusion` | Yes* | Generate exclusion scenarios | - |
| `--all` | Yes* | Generate all scenario types | - |
| `--list` | Yes* | List available models and their probability types | - |
| `--model` | Yes** | Model name to generate scenarios for | - |
| `--count` | No | Number of separate JSON files to generate (each with 1 JSON object, max: 10) | 1 |
| `--split` | No | Generate separate files for each record | False |
| `--config` | No | Path to configuration file | `user_input.json` |
| `--output-dir` | No | Output directory for generated files | `generated_outputs` |
| `--wgs` | No | Use WGS format output | False |
| `--enhanced` | No | Enhanced mode with master template | False |

*One of these must be specified (mutually exclusive)
**Required when generating scenarios (not needed with `--list`)

---

## 📚 Usage Examples

### 🎯 Individual Scenario Generation

#### Positive Scenarios
```bash
# Generate 1 positive scenario (1 file) - DISABLED for Model_1
# python -m src.mockgen.cli --probability --positive --model Model_1

# Generate 2 positive scenarios (2 separate files) - DISABLED for Model_1
# python -m src.mockgen.cli --probability --positive --model Model_1 --count 2

# Generate 5 positive scenarios (5 separate files) - DISABLED for Model_1
# python -m src.mockgen.cli --probability --positive --model Model_1 --count 5

# Note: Positive scenarios are disabled for Model_1. Use negative or exclusion scenarios instead.
```

#### Negative Scenarios
```bash
# Generate 1 negative scenario (1 file)
python -m src.mockgen.cli --probability --negative --model Model_1

# Generate 3 negative scenarios (3 separate files)
python -m src.mockgen.cli --probability --negative --model Model_1 --count 3

# Generate 10 negative scenarios (10 separate files)
python -m src.mockgen.cli --probability --negative --model Model_1 --count 10
```

#### Exclusion Scenarios
```bash
# Generate 1 exclusion scenario (1 file)
python -m src.mockgen.cli --probability --exclusion --model Model_1

# Generate 2 exclusion scenarios (2 separate files)
python -m src.mockgen.cli --probability --exclusion --model Model_1 --count 2

# Generate 7 exclusion scenarios (7 separate files)
python -m src.mockgen.cli --probability --exclusion --model Model_1 --count 7
```

### 🔄 Combined Generation

#### All Scenarios in One File
```bash
python -m src.mockgen.cli --probability --all --model Model_1
```
**Output**: Single file with all three scenarios, each with complete template structure

#### All Scenario Types with Multiple Records
```bash
# Generate all types with 1 scenario each (3 files)
python -m src.mockgen.cli --probability --all --model Model_1 --count 1

# Generate all types with 3 scenarios each (9 files total)
python -m src.mockgen.cli --probability --all --model Model_1 --count 3
```

### 🚀 Enhanced Features

#### Enhanced Mode (Master Template + User Input)
```bash
python -m src.mockgen.cli --enhanced --model Model_1
```
**Output**: Enhanced output with master template merged, all models include complete structure

#### WGS Format
```bash
# Generate positive scenarios in WGS format - DISABLED for Model_1
# python -m src.mockgen.cli --probability --positive --model Model_1 --wgs

# Generate negative scenarios in WGS format
python -m src.mockgen.cli --probability --negative --model Model_1 --wgs

# Generate exclusion scenarios in WGS format
python -m src.mockgen.cli --probability --exclusion --model Model_1 --wgs
```
**Output**: WGS format with complete template structure

#### Multiple Records & Split Files
```bash
# Generate multiple records in one file - DISABLED for Model_1 positive scenarios
# python -m src.mockgen.cli --probability --positive --model Model_1 --count 5

# Generate split files (one file per record) - DISABLED for Model_1 positive scenarios
# python -m src.mockgen.cli --probability --positive --model Model_1 --count 3 --split

# Generate multiple negative records in one file
python -m src.mockgen.cli --probability --negative --model Model_1 --count 5

# Generate split files for negative scenarios (one file per record)
python -m src.mockgen.cli --probability --negative --model Model_1 --count 3 --split
```

### 🎮 Consolidated Generator Examples

```bash
# Generate all scenarios
python consolidated_generator.py --all

# Generate positive scenarios (disabled for Model_1)
python consolidated_generator.py --positive

# Generate negative scenarios for specific model
python consolidated_generator.py --negative --model Model_1

# Generate exclusion scenarios with WGS format
python consolidated_generator.py --exclusion --wgs

# Note: Positive scenario generation is disabled for Model_1
```

---

## 📊 Output Formats

### Standard Format
```json
{
  "positive_data": {
    "PRICNG_ZIP_STATE": ["NY"],
    "CLM_TYPE": ["Inpatient"],
    "ClaimDetails": [...]
  }
}
```

### WGS Format (Complete Template Structure)
```json
{
  "WGS_csbd_medicaid_[scenario]": {
    "first_proc_cd": ["John"],
    "last_proc_cd": ["Smith"],
    "email": ["john.smith@email.com"],
    "phone": ["+1-555-0101"],
    "date_of_birth": ["1990-01-15"],
    "street_address": ["123 Main Street"],
    "proc_cd": ["Vishnu", "Priyan", "Raja", "Raji"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com"],
    "address": ["123456", "12345", "654321", "123"],
    "city": ["Hyderabad"],
    "state": ["NY"],
    "zip_code": ["10001"],
    "country": ["United States"],
    "PRICNG_ZIP_STATE": "[scenario-specific-value]",
    "CLM_TYPE": "[scenario-specific-value]",
    "SRVC_FROM_DT": "[scenario-specific-value]",
    "HCID": "[scenario-specific-value]",
    "PAT_BRTH_DT": "[scenario-specific-value]",
    "PAT_FRST_NME": "[scenario-specific-value]",
    "PAT_LAST_NME": "[scenario-specific-value]",
    "ClaimDetails": [
      {
        "SRVC_FROM_DT": "[scenario-specific-value]",
        "proc_cd": "[scenario-specific-value]",
        "BILL_TYPE": "[scenario-specific-value]"
      }
    ]
  }
}
```

### Enhanced Mode Output
```json
{
  "model": "Model_1",
  "probability_type": "positive",
  "timestamp": "20250816_100632",
  "record_number": 1,
  "data": {
    // Scenario data from configuration merged with master template
  }
}
```

---

## 📁 File Management

### File Naming Convention

#### Single Scenario (count = 1)
- `Model_1_Positive_20250816_035243_352336Z.json`
- `Model_1_Negative_20250816_035243_352336Z.json`
- `Model_1_Exclusion_20250816_035243_352336Z.json`

#### Multiple Scenarios (count > 1)
- `Model_1_Positive_Record_001_20250816_035651_491361Z.json`
- `Model_1_Positive_Record_002_20250816_035651_493360Z.json`
- `Model_1_Positive_Record_003_20250816_035651_495359Z.json`

#### Consolidated Generator Output
- **Single Model:** `Model_1_positive_20241201_143022.json`
- **Multiple Records:** `Model_1_positive_20241201_143022_000001Z.json`
- **Combined:** `combined_all_scenarios_20241201_143022.json`
- **Report:** `project_report_20241201_143022.json`

### Output Directory Structure
```
generated_outputs/
├── Model_1_Positive_[timestamp].json
├── Model_1_Negative_[timestamp].json
├── Model_1_Exclusion_[timestamp].json
├── Model_1_All_Probabilities_[timestamp].json
├── enhanced_output_[timestamp].json
└── [other generated files]
```

---

## ⚙️ Configuration

### Configuration File Structure

The system expects a JSON configuration file (`user_input.json`) with this structure:

```json
{
  "Model_1_positive": {
    "PRICNG_ZIP_STATE": ["TN", "KL"],
    "CLM_TYPE": ["P"],
    "SRVC_FROM_DT": ["04/20/2025"],
    "HCID": ["ABCDEFGHI", "ABCDEFGHI"],
    "PAT_BRTH_DT": ["01/01/1990"],
    "PAT_FRST_NME": ["Mohan", "Raj"],
    "PAT_LAST_NME": ["Kumar", "AJ"],
    "ClaimDetails": [...]
  },
  "Model_1_negative": {
    // Negative scenario data
  },
  "Model_1_exclusion": {
    // Exclusion scenario data
  }
}
```

### Model Requirements
- Models should have `_positive`, `_negative`, and `_exclusion` suffixes
- Each model type should contain the required fields for that scenario
- Values should be arrays to allow random selection

---

## 🔍 Verification & Testing

### Test Commands
```bash
# Test format generation
python test_format_generation.py

# Compare different scenario types
python compare_scenarios.py

# Verify all generated files
python verify_generation.py

# Test CLI functionality
python test_cli_functionality.py
```

### Quick Test Commands
```bash
# Generate test scenarios
python -m src.mockgen.cli --probability --positive --model Model_1 --count 2
python -m src.mockgen.cli --probability --negative --model Model_1 --count 2
python -m src.mockgen.cli --probability --exclusion --model Model_1 --count 2
```

---

## 🛠️ Troubleshooting

### Common Issues

1. **"No module named 'mockgen'"**
   - Ensure you're in the project root directory
   - Check that `src/mockgen/` directory exists

2. **"File not found"**
   - Check that `user_input.json` exists in current directory
   - Verify file paths are correct

3. **"Invalid JSON"**
   - Validate your JSON files using online JSON validator
   - Check for syntax errors (missing commas, brackets, etc.)

4. **"Missing model"**
   - Use `--list` to see available models
   - Ensure model names match exactly (case-sensitive)

5. **"No data found"**
   - Check that your model has the required probability type suffix
   - Verify data exists in the configuration file

### Debug Mode
```bash
# Get detailed help
python -m src.mockgen.cli --help
python consolidated_generator.py --help

# List available models first
python -m src.mockgen.cli --list

# Test with single scenario
python -m src.mockgen.cli --probability --positive --model Model_1
```

---

## 🧹 Cleanup & Maintenance

### Files That Can Be Deleted

After confirming the consolidated tools work, you can safely delete these old files:

#### Batch Files (9 files → 1 file)
- `generate_all_scenarios.bat` → `consolidated_generator.bat`
- `generate_exclusion.bat` → `consolidated_generator.bat`
- `generate_negative.bat` → `consolidated_generator.bat`
- `generate_positive.bat`