# Mock Data Generator

This tool generates mock data by randomly selecting values from multiple edit configurations.

## Features

- **Multiple Edits Support**: Define multiple edit sections (Edit_1, Edit_2, etc.) with different sets of values
- **Random Selection**: Randomly selects values from each edit section
- **Flexible Output**: Generate single or multiple outputs, with option to split into separate files
- **Comma-separated Values**: Support for comma-separated values in strings
- **Model/Section Mode**: Provide top-level sections like `Model_1`, `Model_2` and generate one JSON per paired record using `--model`

## Usage

### 1. Configuration File (`user_input.json`)

The configuration file may contain multiple sections (either `Edit_X` or custom like `Model_1`, `Model_2`), each with the required fields:

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

Or with custom model sections:

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

### 2. Running the Generator

#### Basic Usage (no install)
```bash
# Generate 1 random output
python generate_mock_output.py

# Generate 5 random outputs in a single file
python generate_mock_output.py --count 5

# Generate 3 random outputs, each in a separate file
python generate_mock_output.py --count 3 --split
```

#### Install and use as a CLI

```bash
# Editable install for development
python -m pip install -e .

# Then run
mockgen --count 3 --split
```

#### Command Line Options

- `--config <path>`: Path to the input JSON file (default: `user_input.json`)
- `--count <number>`: Number of random outputs to generate (default: 1)
- `--split`: If set with `--count > 1`, writes each output to its own JSON file
- `--init`: Create/overwrite a template input JSON file
- `--model <section>`: Generate records for a specific section (e.g., `Model_1`). Values are paired by index per field, using round-robin for shorter lists. The total number of files equals the maximum list length across the required fields.

### 3. Output Format

The generated output will contain randomly selected values from the edit sections:

```json
{
  "Edit_1_output_1": {
    "name": "Priyan",
    "mail_id": "Vishnupriyannatarajan@gmail.com",
    "address": "123456",
    "city": "Hyderabad"
  },
  "Edit_2_output_2": {
    "name": "Raju",
    "mail_id": "Ran@gmail.com",
    "address": "5748",
    "city": "Kovai"
  }
}
```

## How It Works

1. **Load Configuration**: Reads the `user_input.json` file and parses the edit sections
2. **Random Edit Selection**: For each output, randomly selects one of the available edits
3. **Random Value Selection**: Within the selected edit, randomly selects one value from each field
4. **Output Generation**: Creates the final JSON output with the selected values

## Examples

### Example 1: Single Output
```bash
python generate_mock_output.py
```
Output: `mock_outputs/output_20250808_051907_760451Z.json`

### Example 2: Multiple Outputs
```bash
python generate_mock_output.py --count 3
```
Generates 3 random selections in a single file.

### Example 3: Split Outputs
```bash
python generate_mock_output.py --count 2 --split
```
Generates 2 separate files, each with one random selection.

### Example 4: Model/Section Mode (index-paired records)

```
python generate_mock_output.py --model Model_1
```

If `Model_1` has values like `name=[A,B,C]`, `mail_id=[m1,m2]`, `address=[a1,a2]`, `city=[c1]`, this generates 3 files:

1. A, m1, a1, c1
2. B, m2, a2, c1
3. C, m1, a1, c1

<!-- Scenario generation is not currently implemented. -->

## Testing

Run the test script to see how the random selection works:

```bash
python test_random_selection.py
```

This will show:
- Available options for each edit
- 5 random selections demonstrating the functionality

## File Structure

```
Mockup_up_data - Copy/
├── user_input.json
├── README.md
├── pyproject.toml
├── .gitignore
├── generate_mock_output.py    # Thin wrapper to run local CLI without install
├── test_random_selection.py   # Demo script
├── src/
│   └── mockgen/
│       ├── __init__.py
│       ├── core.py            # Library functions
│       └── cli.py             # CLI entrypoint (also used by `mockgen` script)
└── mock_outputs/              # Generated files
    └── output_*.json
```
