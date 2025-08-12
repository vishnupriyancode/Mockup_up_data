# Mock Generation System - Usage Guide

## 🚀 Getting Started

The Mock Generation System is now working correctly! Here's how to use it:

## 📁 Project Structure

```
Mockup_up_data/
├── user_input.json          # Your data models and values
├── master.json             # Base template structure
├── src/mockgen/           # Core system (don't modify)
├── mock_outputs/          # Generated JSON files
└── generate_probability_outputs.py  # Probability generator
```

## 🎯 Basic Commands

### 1. Generate Enhanced Output (Recommended)

```bash
# Generate output for all models
python -m src.mockgen.cli --enhanced

# Generate output for specific model
python -m src.mockgen.cli --enhanced --model Model_1

# Generate multiple records
python -m src.mockgen.cli --enhanced --count 5

# Generate split output files (one per model)
python -m src.mockgen.cli --enhanced --output-format split

# Generate multiple records in separate files
python -m src.mockgen.cli --enhanced --output-format multiple --count 3
```

### 2. CLI Help and Options

```bash
# Get help for CLI options
python -m src.mockgen.cli --help

# Available options:
# --config: Path to input JSON file
# --master: Path to master template file
# --init: Create/overwrite template input JSON
# --count: Number of random outputs
# --split: Write each output to separate file
# --model: Generate output for specific model
# --enhanced: Use enhanced mode with master template
# --models: Specific models to generate for
# --output-format: single/multiple/split
# --legacy: Force legacy mode for Edit_X format
```

### 3. Probability Generator

```bash
# Generate all probability types
python generate_probability_outputs.py --all

# Generate specific scenarios
python generate_probability_outputs.py --positive --model Model_1
python generate_probability_outputs.py --negative --model Model_1
python generate_probability_outputs.py --exclusion --model Model_1

# Generate multiple records with split files
python generate_probability_outputs.py --all --count 5 --split

# Get help for probability generator
python generate_probability_outputs.py --help
```

## 🔧 How It Works

1. **Master Template** (`master.json`): Provides the base structure and realistic data
2. **User Input** (`user_input.json`): Defines your custom models and values
3. **System Merges**: Combines both to create realistic mock data
4. **Output**: Generates timestamped JSON files in `mock_outputs/` folder

## 📊 Understanding the Output

The system generates data that combines:
- **Base fields**: first_name, last_name, email, phone, etc. (from master template)
- **Custom fields**: name, mail_id, address, city (from your user input)
- **Randomization**: Values are randomly selected from your arrays

## 🎲 Available Models

- **Model_1**: Standard data model
- **Model_1_Positive**: Valid/positive test cases
- **Model_1_Negative**: Invalid/negative test cases
- **Model_1_Exclusion**: Exclusion scenario data

## 🚨 Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure you're in the project root directory (`Mockup_up_data/`)

### Issue: "File not found"
**Solution**: Ensure `user_input.json` and `master.json` exist in the current directory

### Issue: No output generated
**Solution**: Check that the `mock_outputs/` folder exists and is writable

### Issue: Commands not working
**Solution**: Try the basic command first: `python -m src.mockgen.cli --enhanced`

## ✅ Verification

To verify everything is working, run:

```bash
python -m src.mockgen.cli --enhanced
```

You should see:
```
Loaded master template from 'master.json'
Loaded user input from 'user_input.json' with 4 models
Merged master template with user input requirements
Processing all models: Model_1, Model_1_Positive, Model_1_Negative, Model_1_Exclusion
Generated: mock_outputs\enhanced_output_[timestamp].json
```

## 🎉 Success!

If you see the above output, congratulations! The system is working correctly and generating JSON files in the `mock_outputs/` folder.

## 📝 Customization

To customize the data:
1. Edit `user_input.json` to add/modify models and values
2. Edit `master.json` to change the base template structure
3. Run the commands again to generate new data

## 🔄 Advanced Usage

### Generate Multiple Records
```bash
python -m src.mockgen.cli --enhanced --count 10
```

### Generate Split Files
```bash
python -m src.mockgen.cli --enhanced --output-format split
```

### Generate Multiple Records in Separate Files
```bash
python -m src.mockgen.cli --enhanced --output-format multiple --count 5
```

### Use Specific Models
```bash
python -m src.mockgen.cli --enhanced --models Model_1 Model_1_Positive Model_1_Exclusion
```

### Use Probability Generator with Custom Configuration
```bash
# Custom configuration file
python generate_probability_outputs.py --config my_config.json --all

# Custom output directory
python generate_probability_outputs.py --output-dir custom_outputs --positive

# List available models
python generate_probability_outputs.py --list
```

### Legacy Mode Support
```bash
# Backward compatibility for Edit_X format
python -m src.mockgen.cli --legacy --model Edit_1

# Legacy mode with enhanced features
python -m src.mockgen.cli --legacy --enhanced --count 10
```

### Initialize Template Configuration
```bash
# Create/overwrite template input JSON
python -m src.mockgen.cli --init
```

## 📚 Help and Documentation

### Built-in Help
```bash
# CLI help
python -m src.mockgen.cli --help

# Probability generator help
python generate_probability_outputs.py --help
```

### Available Documentation
- **README.md**: Complete project overview and quick start guide
- **docs/user-guides/PROJECT_EXPLANATION.md**: Comprehensive project explanation
- **docs/user-guides/PROJECT_STRUCTURE.md**: Detailed project organization guide
- **technical-specs/architecture/TECHNICAL_COMPONENTS.md**: Technical architecture details
- **reports/project-reports/Mock_Generation_System_Project_Report.md**: Comprehensive project report

---

**Need Help?** Use the built-in help commands or refer to the comprehensive documentation!
