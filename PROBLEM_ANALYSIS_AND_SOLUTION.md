# Problem Analysis and Solution: Mock Data Generation Issue

## Problem Description

Users were unable to generate mock data outputs using the `generate_probability_outputs.py` script with the following commands:
- `python generate_probability_outputs.py --positive --count 3 --split`
- `python generate_probability_outputs.py --negative --count 2`
- `python generate_probability_outputs.py --exclusion --count 2`
- `python generate_probability_outputs.py --all --count 2`

The script was returning the error message:
```
No outputs generated. Check your configuration and model names.
```

## Root Cause Analysis

The issue was a **naming convention mismatch** between the configuration file and the script:

### 1. Configuration File (`user_input.json`)
The configuration file used **lowercase** suffixes for probability types:
```json
{
  "Model_1_positive": { ... },
  "Model_1_negative": { ... },
  "Model_1_exclusion": { ... }
}
```

### 2. Script (`generate_probability_outputs.py`)
The script was looking for **uppercase** suffixes:
```python
# Script was looking for:
key = f"{model_name}_{probability_type}"  # e.g., "Model_1_Positive"
```

This mismatch caused the script to fail to find the configuration data, resulting in no outputs being generated.

## Solution Implemented

### 1. Fixed `_get_probability_data()` Method
Updated the method to handle both uppercase and lowercase suffixes:
```python
def _get_probability_data(self, model_name: str, probability_type: str) -> Optional[Dict[str, List[str]]]:
    """Get data for a specific model and probability type."""
    # Handle both uppercase and lowercase probability type suffixes
    key_upper = f"{model_name}_{probability_type}"
    key_lower = f"{model_name}_{probability_type.lower()}"
    
    # Try uppercase first, then lowercase
    if key_upper in self.config:
        return self.config.get(key_upper)
    elif key_lower in self.config:
        return self.config.get(key_lower)
    else:
        return None
```

### 2. Fixed `_get_model_names()` Method
Updated to recognize both uppercase and lowercase suffixes:
```python
def _get_model_names(self) -> List[str]:
    """Get base model names (without _Positive, _Negative, _Exclusion suffixes)."""
    base_models = set()
    for key in self.config.keys():
        if ("_Positive" in key or "_positive" in key or 
            "_Negative" in key or "_negative" in key or 
            "_Exclusion" in key or "_exclusion" in key):
            base_name = key.replace("_Positive", "").replace("_positive", "").replace("_Negative", "").replace("_negative", "").replace("_Exclusion", "").replace("_exclusion", "")
            base_models.add(base_name)
        else:
            base_models.add(key)
    return list(base_models)
```

### 3. Fixed `list_available_models()` Method
Updated to check for both naming conventions:
```python
positive = "✓" if (f"{model}_Positive" in self.config or f"{model}_positive" in self.config) else "✗"
negative = "✓" if (f"{model}_Negative" in self.config or f"{model}_negative" in self.config) else "✗"
exclusion = "✓" if (f"{model}_Exclusion" in self.config or f"{model}_exclusion" in self.config) else "✗"
```

## Verification of Fix

After implementing the fix, all commands now work correctly:

### 1. List Available Models
```bash
python generate_probability_outputs.py --list
```
**Output:**
```
Available Models and Probability Types:
==================================================

Model_1:
  Positive: ✓
  Negative: ✓
  Exclusion: ✓
```

### 2. Generate Positive Outputs
```bash
python generate_probability_outputs.py --positive --count 3 --split
```
**Output:**
```
Generated Positive output 1: mock_outputs\Model_1_Positive_Record_001_20250813_093946_577790Z.json
Generated Positive output 2: mock_outputs\Model_1_Positive_Record_002_20250813_093946_578743Z.json
Generated Positive output 3: mock_outputs\Model_1_Positive_Record_003_20250813_093946_579738Z.json

Generated 3 output file(s) in 'mock_outputs' directory
```

### 3. Generate Negative Outputs
```bash
python generate_probability_outputs.py --negative --count 2
```
**Output:**
```
Generated Negative output: mock_outputs\Model_1_Negative_20250813_093950_854166Z.json

Generated 1 output file(s) in 'mock_outputs' directory
```

### 4. Generate Exclusion Outputs
```bash
python generate_probability_outputs.py --exclusion --count 2
```
**Output:**
```
Generated Exclusion output: mock_outputs\Model_1_Exclusion_20250813_093954_710572Z.json

Generated 1 output file(s) in 'mock_outputs' directory
```

### 5. Generate All Probability Types
```bash
python generate_probability_outputs.py --all --count 2
```
**Output:**
```
Generated All Probabilities output: mock_outputs\Model_1_All_Probabilities_20250813_093957_063749Z.json

Generated 1 output file(s) in 'mock_outputs' directory
```

## Generated Files

The script now successfully generates the following files in the `mock_outputs/` directory:
- `Model_1_Positive_Record_001_*.json` - Individual positive probability records
- `Model_1_Positive_Record_002_*.json` - Individual positive probability records  
- `Model_1_Positive_Record_003_*.json` - Individual positive probability records
- `Model_1_Negative_*.json` - Negative probability records
- `Model_1_Exclusion_*.json` - Exclusion probability records
- `Model_1_All_Probabilities_*.json` - Combined all probability types

## Key Benefits of the Fix

1. **Backward Compatibility**: The script now works with both uppercase and lowercase naming conventions
2. **Flexibility**: Users can use either naming style in their configuration files
3. **Robustness**: The script gracefully handles naming variations
4. **User Experience**: All commands now work as expected without errors

## Recommendations

1. **Standardize Naming**: Consider standardizing on one naming convention (either all uppercase or all lowercase) for future consistency
2. **Documentation**: Update user documentation to clarify the supported naming conventions
3. **Testing**: Test the script with various naming conventions to ensure robustness

## Conclusion

The issue was successfully resolved by making the script case-insensitive for probability type suffixes. Users can now generate mock data outputs using all the available commands without encountering the "No outputs generated" error.
