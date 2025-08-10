# Mock Data Generator

This tool generates mock data by randomly selecting values from multiple edit configurations. It supports both basic random selection mode and enhanced mode with master templates.

## Features

- **Multiple Edits Support**: Define multiple edit sections (Edit_1, Edit_2, etc.) with different sets of values
- **Random Selection**: Randomly selects values from each edit section
- **Flexible Output**: Generate single or multiple outputs, with option to split into separate files
- **Comma-separated Values**: Support for comma-separated values in strings
- **Model/Section Mode**: Provide top-level sections like `Model_1`, `Model_2` and generate one JSON per paired record using `--model`
- **Enhanced Mode**: Merge master template with BRD requirements for sophisticated data generation
- **Multiple Output Formats**: Single file, multiple records, or split files

## Quick Start Commands

### 1. Basic Random Generation (No Installation Required)

```bash
# Generate 1 random output
python generate_mock_output.py

# Generate 5 random outputs in a single file
python generate_mock_output.py --count 5

# Generate 3 random outputs, each in a separate file
python generate_mock_output.py --count 3 --split

# Generate records for a specific model section
python generate_mock_output.py --model Model_1
```

### 2. Enhanced Mode with Master Template

```bash
# Generate output for all models using master template
python generate_mock_output.py --enhanced

# Generate output for specific models
python generate_mock_output.py --enhanced --models Model_1 Model_2

# Generate multiple outputs in split files
python generate_mock_output.py --enhanced --output-format split

# Generate multiple records in one file
python generate_mock_output.py --enhanced --output-format multiple --count 3
```

### 3. CLI Tool (After Installation)

```bash
# Install the tool
python -m pip install -e .

# Use the CLI commands
mockgen --count 3 --split
mockgen --enhanced --models Model_1 Model_2
mockgen --enhanced --output-format split
```

## Complete Command Reference

### Basic Mode Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--config <path>` | Path to input JSON file | `--config my_config.json` |
| `--count <number>` | Number of random outputs | `--count 5` |
| `--split` | Split multiple outputs into separate files | `--count 3 --split` |
| `--init` | Create template input JSON file | `--init` |
| `--model <section>` | Generate records for specific section | `--model Model_1` |

### Enhanced Mode Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--enhanced` | Enable enhanced mode with master template | `--enhanced` |
| `--master <path>` | Path to master template JSON | `--master template.json` |
| `--models <list>` | Specific models to generate | `--models Model_1 Model_2` |
| `--output-format <type>` | Output format type | `--output-format split` |

### Output Format Options

| Format | Description | Command |
|--------|-------------|---------|
| `single` | Single output file (default) | `--output-format single` |
| `multiple` | Multiple records in one file | `--output-format multiple --count 3` |
| `split` | Separate file for each output | `--output-format split` |

## Usage Scenarios

### Scenario 1: Basic Random Generation
Generate random data from edit sections:

```bash
# Single random output
python generate_mock_output.py

# Multiple random outputs
python generate_mock_output.py --count 5

# Split into separate files
python generate_mock_output.py --count 3 --split
```

### Scenario 2: Model-Specific Generation
Generate paired records for a specific model:

```bash
# Generate records for Model_1
python generate_mock_output.py --model Model_1

# This creates one file per record based on field values
# If Model_1 has name=[A,B,C], mail_id=[m1,m2], address=[a1,a2], city=[c1]
# Generates 3 files with paired values:
# File 1: A, m1, a1, c1
# File 2: B, m2, a2, c1  
# File 3: C, m1, a1, c1
```

### Scenario 3: Enhanced Mode with Master Template
Use master template + BRD requirements:

```bash
# Generate for all models
python generate_mock_output.py --enhanced

# Generate for specific models
python generate_mock_output.py --enhanced --models Model_1 Model_2

# Generate split files for each model
python generate_mock_output.py --enhanced --output-format split

# Generate multiple iterations
python generate_mock_output.py --enhanced --output-format multiple --count 3
```

### Scenario 4: Template Initialization
Create configuration files:

```bash
# Create template user_input.json
python generate_mock_output.py --init

# Create with custom path
python generate_mock_output.py --init --config my_config.json
```

## Configuration Files

### 1. Basic Configuration (`user_input.json`)

```json
{
  "Edit_1": {
    "name": "Vishnu,Priyan",
    "mail_id": "Vishnupriyannatarajan@gmail.com, ramdon@gamil.com",
    "address": "123456,12345",
    "city": "Hyderabad,Chennai"
  },
  "Edit_2": {
    "name": "Raju,Natarajan",
    "mail_id": "Vishnupriyan@gmail.com, Ran@gmail.com",
    "address": "124596,5748",
    "city": "Chennai,Kovai"
  }
}
```

### 2. Model-Based Configuration

```json
{
  "Model_1": {
    "name": ["Vishnu","Priyan"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com", "ramdon@gamil.com"],
    "address": ["123456","12345"],
    "city": ["Hyderabad","Chennai"]
  },
  "Model_2": {
    "name": "Raju,Natarajan",
    "mail_id": "Vishnupriyan@gmail.com, Ran@gmail.com",
    "address": "124596,5748",
    "city": "Chennai,Kovai"
  }
}
```

### 3. Master Template (`master.json`)

```json
{
  "user_profile": {
    "first_name": ["John"],
    "last_name": ["Smith"],
    "email": ["john.smith@email.com"],
    "phone": ["+1-555-0101"],
    "name": ["Vishnu", "Priyan", "Raja", "Raji"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com"],
    "address": ["123456", "12345", "654321", "123"],
    "city": ["Hyderabad"]
  }
}
```

## Demo and Testing

### Run Demo Script
```bash
python demo_enhanced_system.py
```

### Test Random Selection
```bash
python test_random_selection.py
```

## File Structure

```
Mockup_up_data/
├── user_input.json          # BRD requirements/configuration
├── master.json              # Master template for enhanced mode
├── README.md                # This file
├── pyproject.toml          # Package configuration
├── generate_mock_output.py  # Local runner (no install needed)
├── demo_enhanced_system.py  # Enhanced mode demonstration
├── test_random_selection.py # Random selection testing
├── src/
│   └── mockgen/
│       ├── __init__.py
│       ├── core.py          # Core library functions
│       └── cli.py           # CLI entrypoint
└── mock_outputs/            # Generated output files
    └── output_*.json
```

## How It Works

### Basic Mode
1. **Load Configuration**: Reads the input JSON file and parses edit sections
2. **Random Edit Selection**: For each output, randomly selects one available edit
3. **Random Value Selection**: Within selected edit, randomly selects one value from each field
4. **Output Generation**: Creates final JSON with selected values

### Enhanced Mode
1. **Load Templates**: Reads master template and BRD requirements
2. **Merge Configuration**: Combines master template with BRD-specific values
3. **Model Processing**: Generates output for selected models using merged configuration
4. **Output Generation**: Creates enhanced JSON with template + BRD data

## Examples

### Example 1: Basic Single Output
```bash
python generate_mock_output.py
```
Output: `mock_outputs/output_20250808_051907_760451Z.json`

### Example 2: Enhanced Mode for All Models
```bash
python generate_mock_output.py --enhanced
```
Generates output using master template + BRD requirements for all models.

### Example 3: Enhanced Mode for Specific Models
```bash
python generate_mock_output.py --enhanced --models Model_1 Model_2 --output-format split
```
Generates separate files for Model_1 and Model_2 using enhanced mode.

### Example 4: Multiple Iterations
```bash
python generate_mock_output.py --enhanced --output-format multiple --count 5
```
Generates 5 iterations of all models in one file.
