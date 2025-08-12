# Enhanced Mock Generation System

A comprehensive system for generating mock JSON outputs with support for probability-based scenarios, master template integration, and flexible output formats. Supports both legacy `Edit_X` format and new `Model_X` format.

## 🚀 Features

- **Master Template Integration**: Uses `master.json` as a base template and merges it with user input
- **Probability-Based Generation**: Generate positive, negative, and exclusion probability scenarios
- **Multiple Model Support**: Handles various model types (Model_1, Model_1_Positive, Model_1_Negative, etc.)
- **Flexible Output Formats**: Single file, multiple records, or split files
- **Backward Compatibility**: Supports both new Model_X format and legacy Edit_X format
- **CLI Interface**: Easy-to-use command-line interface with various options
- **Standalone Probability Generator**: Specialized tool for probability-based outputs

## 📁 File Structure

```
Mockup_up_data/
├── user_input.json                    # User-defined models and data
├── master.json                       # Master template structure
├── src/mockgen/                     # Core system modules
│   ├── core.py                      # Main functionality
│   └── cli.py                       # Command-line interface
├── mock_outputs/                    # Generated output files
├── demo_enhanced_system.py          # Demonstration script
└── generate_probability_outputs.py  # Probability generator
```

## 🎯 Quick Start

### Enhanced System (Recommended)

```bash
# Generate enhanced output for all models
python -m src.mockgen.cli --enhanced

# Generate output for specific model
python -m src.mockgen.cli --enhanced --model Model_1

# Generate multiple records
python -m src.mockgen.cli --model Model_1 --count 5

# Generate split output files
python -m src.mockgen.cli --enhanced --output-format split
```

### Probability Generator

```bash
# Generate all probability types for all models
python generate_probability_outputs.py --all

# Generate only positive probabilities
python generate_probability_outputs.py --positive

# Generate negative probabilities for specific model
python generate_probability_outputs.py --negative --model Model_1

# Generate multiple records
python generate_probability_outputs.py --all --count 5

# Generate separate files for each record
python generate_probability_outputs.py --positive --count 3 --split

# List available models
python generate_probability_outputs.py --list
```

## 📋 Input File Format

### user_input.json

The system supports two formats:

#### Model_X Format (Recommended)
```json
{
  "Model_1": {
    "name": ["Vishnu", "Priyan", "Raja", "Raji"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com", "ramdon@gamil.com"],
    "address": ["123456", "12345", "654321", "123"],
    "city": ["Hyderabad", "Chennai", "Kovai", "Dindigul"]
  },
  "Model_1_Positive": {
    "name": ["Vishnu", "Priyan", "Raja", "Raji"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com", "ramdon@gamil.com"],
    "address": ["123456", "12345", "654321", "123"],
    "city": ["Hyderabad", "Chennai", "Kovai", "Dindigul"]
  },
  "Model_1_Negative": {
    "name": ["", "123", "@@@"],
    "mail_id": ["invalid-email", "no-at-symbol", "user@invalid_domain"],
    "address": ["", "!@#", "????"],
    "city": ["", "Atlantis", "12345"]
  },
  "Model_1_Exclusion": {
    "name": ["Vishnu", "Priyan", "Raja", "Raji"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com", "ramdon@gamil.com"],
    "address": ["123456", "12345", "654321", "123"],
    "city": ["Hyderabad", "Chennai", "Kovai", "Dindigul"]
  }
}
```

#### Legacy Edit_X Format
```json
{
  "Edit_1": {
    "name": "Vishnu,Priyan",
    "mail_id": "Vishnupriyannatarajan@gmail.com,ramdon@gamil.com",
    "address": "123456,12345",
    "city": "Hyderabad,Chennai"
  }
}
```

### master.json

The master template provides the base structure:

```json
{
  "user_profile": {
    "first_name": ["John"],
    "last_name": ["Smith"],
    "email": ["john.smith@email.com"],
    "phone": ["+1-555-0101"],
    "date_of_birth": ["1990-01-15"],
    "street_address": ["123 Main Street"],
    "name": ["Vishnu", "Priyan", "Raja", "Raji"],
    "mail_id": ["Vishnupriyannatarajan@gmail.com"],
    "address": ["123456", "12345", "654321", "123"],
    "city": ["Hyderabad"],
    "state": ["NY"],
    "zip_code": ["10001"],
    "country": ["United States"]
  }
}
```

## 🎮 CLI Options

### Enhanced System Options
- `--config`: Path to user input file (default: user_input.json)
- `--master`: Path to master template file (default: master.json)
- `--init`: Create template input file and exit
- `--count`: Number of outputs to generate (default: 1)
- `--enhanced`: Use enhanced mode with master template
- `--model`: Generate output for specific model
- `--models`: Generate output for multiple specific models
- `--output-format`: Output format (single, multiple, split)
- `--split`: Write each output to separate file
- `--legacy`: Force legacy mode for backward compatibility

### Probability Generator Options
- `--all`: Generate all probability types (positive, negative, exclusion)
- `--positive`: Generate only positive probability outputs
- `--negative`: Generate only negative probability outputs
- `--exclusion`: Generate only exclusion probability outputs
- `--model`: Generate outputs for specific model only
- `--count`: Number of records to generate per probability type
- `--split`: Generate separate files for each record instead of combining them
- `--list`: List available models and their probability types
- `--config`: Path to configuration file (default: user_input.json)
- `--output-dir`: Output directory for generated files

## 📊 Output Examples

### Enhanced System Output
When using `--enhanced`, the output follows the master template structure:

```json
{
  "Model_1": {
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com",
    "phone": "+1-555-0101",
    "date_of_birth": "1990-01-15",
    "street_address": "123 Main Street",
    "name": "Vishnu",
    "mail_id": "Vishnupriyannatarajan@gmail.com",
    "address": "123456",
    "city": "Hyderabad",
    "state": "NY",
    "zip_code": "10001",
    "country": "United States"
  }
}
```

### Probability Generator Output

#### Single Record Output
```json
{
  "Model_1_Positive": {
    "name": "Vishnu",
    "mail_id": "Vishnupriyannatarajan@gmail.com",
    "address": "123456",
    "city": "Hyderabad"
  }
}
```

#### Multiple Records Output
```json
{
  "Model_1_Positive": [
    {
      "name": "Vishnu",
      "mail_id": "Vishnupriyannatarajan@gmail.com",
      "address": "123456",
      "city": "Hyderabad"
    },
    {
      "name": "Priyan",
      "mail_id": "ramdon@gamil.com",
      "address": "12345",
      "city": "Chennai"
    }
  ]
}
```

#### All Probabilities Output
```json
{
  "Model_1_Positive": {
    "name": "Vishnu",
    "mail_id": "Vishnupriyannatarajan@gmail.com",
    "address": "123456",
    "city": "Hyderabad"
  },
  "Model_1_Negative": {
    "name": "",
    "mail_id": "invalid-email",
    "address": "",
    "city": ""
  },
  "Model_1_Exclusion": {
    "name": "Vishnu",
    "mail_id": "Vishnupriyannatarajan@gmail.com",
    "address": "123456",
    "city": "Hyderabad"
  }
}
```

## 🔧 Usage Examples

### Enhanced System

#### Example 1: Generate Enhanced Output for All Models
```bash
python -m src.mockgen.cli --enhanced
```

#### Example 2: Generate Output for Specific Models
```bash
python -m src.mockgen.cli --enhanced --models Model_1 Model_1_Positive
```

#### Example 3: Generate Multiple Records for a Model
```bash
python -m src.mockgen.cli --model Model_1 --count 10
```

#### Example 4: Generate Split Output Files
```bash
python -m src.mockgen.cli --enhanced --output-format split
```

### Probability Generator

#### Example 1: Generate All Probability Types
```bash
python generate_probability_outputs.py --all
```

#### Example 2: Generate Only Positive Probabilities
```bash
python generate_probability_outputs.py --positive --count 3
```

#### Example 3: Generate Negative Probabilities for Specific Model
```bash
python generate_probability_outputs.py --negative --model Model_1
```

#### Example 4: Generate All Probabilities for Specific Model
```bash
python generate_probability_outputs.py --all --model Model_2 --count 2
```

## 📂 Output Directory Structure

Generated files are saved in the `mock_outputs/` directory with timestamps:

```
mock_outputs/
├── enhanced_output_20241201_143022_123456Z.json
├── Model_1_Positive_20241201_143022_123456Z.json
├── Model_1_Negative_20241201_143022_123457Z.json
├── Model_1_Exclusion_20241201_143022_123458Z.json
├── Model_1_All_Probabilities_20241201_143022_123459Z.json
└── ...
```

## 🎭 Demonstration

Run the demonstration script to see the enhanced system in action:

```bash
python demo_enhanced_system.py
```

This will:
1. Show how to load and merge configurations
2. Generate outputs for different models
3. Demonstrate various output formats
4. Show CLI usage examples

## 🔒 Safety Features

- **No Codebase Changes**: All tools are completely standalone and don't modify your existing code
- **Separate Output Directory**: All generated files go to a dedicated directory
- **Timestamped Files**: Each output file has a unique timestamp to prevent overwrites
- **Error Handling**: Comprehensive error handling with clear error messages

## 🚨 Error Handling

The system provides clear error messages for:
- Missing or invalid input files
- Invalid JSON format
- Missing required fields
- Model not found errors
- Configuration validation errors

## 🔄 Migration from Legacy Format

If you have existing `Edit_X` format files, they will continue to work. The system automatically detects the format and handles it appropriately. To migrate to the new `Model_X` format:

1. Convert comma-separated strings to arrays
2. Update section names from `Edit_X` to `Model_X`
3. Use the `--enhanced` flag for better integration with master template

## 🛠️ Troubleshooting

### Common Issues

1. **File not found**: Ensure `user_input.json` and `master.json` exist
2. **Invalid JSON**: Check JSON syntax in input files
3. **Missing fields**: Ensure all required fields are present
4. **Model not found**: Check model names in user input file

### Debug Mode

For detailed debugging, you can modify the core functions to add more logging or run the demonstration script to see step-by-step execution.

## 📝 File Naming Convention

Generated files follow this naming pattern:
- **Enhanced mode**: `enhanced_output_YYYYMMDD_HHMMSS_ffffffZ[_tag].json`
- **Model-specific**: `{model_name}_output_YYYYMMDD_HHMMSS_ffffffZ[_tag].json`
- **Probability outputs**: `{model_name}_{type}_YYYYMMDD_HHMMSS_ffffffZ.json`
- **Split probability outputs**: `{model_name}_{type}_Record_XXX_YYYYMMDD_HHMMSS_ffffffZ.json`
- **Standard mode**: `output_YYYYMMDD_HHMMSS_ffffffZ[_tag].json`

## 🔧 Advanced Usage

### Custom Configuration File
```bash
python generate_probability_outputs.py --config my_config.json --all
```

### Custom Output Directory
```bash
python generate_probability_outputs.py --output-dir custom_outputs --positive
```

### Combine Multiple Options
```bash
python generate_probability_outputs.py --positive --negative --model Model_1 --count 10
```

### Generate Separate Files for Each Record
```bash
python generate_probability_outputs.py --positive --count 3 --split
```

## 🎯 When to Use Each Tool

### Use Enhanced System (`src/mockgen/cli`) when:
- You want to integrate with master template structure
- You need complex field mappings
- You want to maintain consistent output structure
- You're working with multiple models

### Use Probability Generator when:
- You need specific probability-based scenarios
- You want quick, focused outputs
- You're testing positive/negative/exclusion cases
- You need standalone functionality

## 🤝 Contributing

The system is designed to be extensible. You can:
- Add new field types
- Implement custom output formats
- Add validation rules
- Extend the CLI with new options
- Add new probability types

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Help and Support

### Get Help for Enhanced System
```bash
python -m src.mockgen.cli --help
```

### Get Help for Probability Generator
```bash
python generate_probability_outputs.py --help
```

### List Available Models
```bash
python generate_probability_outputs.py --list
```

---

## 🎉 Ready to Use!

You now have a comprehensive system for generating mock data with:
- **Enhanced System**: Full-featured mock generation with master template integration
- **Probability Generator**: Specialized tool for probability-based scenarios
- **Unified Documentation**: Single source of truth for all functionality
- **Clean Project Structure**: No redundant files or overlapping documentation

Choose the tool that best fits your needs and start generating your mock data!
