"""
MockGen Core - Core functionality for mock data generation
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class MockGenCore:
    """Core MockGen functionality for generating probability scenarios."""
    
    def __init__(self, config_file: str = "user_input.json", output_dir: str = "generated_outputs"):
        self.config_file = Path(config_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with self.config_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def _get_probability_data(self, model_name: str, probability_type: str) -> Optional[Dict[str, List[str]]]:
        """Get probability data for specific model and type."""
        # Try different key formats
        key_formats = [
            f"{model_name}_{probability_type}",
            f"{model_name.capitalize()}_{probability_type}",
            f"{probability_type}_{model_name}",
            f"{probability_type}_{model_name.capitalize()}"
        ]
        
        for key in key_formats:
            if key in self.config:
                return self.config[key]
        
        return None
    
    def _get_model_names(self) -> List[str]:
        """Get list of available model names from config."""
        models = set()
        for key in self.config.keys():
            if "_positive" in key or "_negative" in key or "_exclusion" in key:
                model_name = key.replace("_positive", "").replace("_negative", "").replace("_exclusion", "")
                models.add(model_name)
        return list(models)
    
    def _generate_single_value_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate single random values for each field in the data structure."""
        result = {}
        
        for key, value in data.items():
            if isinstance(value, list):
                if value:  # Check if list is not empty
                    if isinstance(value[0], dict):
                        # Handle nested list of objects (like ClaimDetails)
                        result[key] = [self._generate_single_value_data(value[0])]
                    else:
                        # Handle simple list values
                        result[key] = random.choice(value)
                else:
                    result[key] = ""
            elif isinstance(value, dict):
                result[key] = self._generate_single_value_data(value)
            else:
                result[key] = value
        
        return result
    
    def _generate_wgs_format(self, data: Dict[str, List[str]], probability_type: str) -> Dict[str, Any]:
        """Generate output in WGS format matching the exact template structure."""
        key_name = f"WGS_csbd_medicaid_{probability_type.lower()}"
        
        output = {}
        
        # Add all the template fields in the exact order from the reference template
        template_fields = [
            "first_proc_cd", "last_proc_cd", "email", "phone", "date_of_birth",
            "street_address", "proc_cd", "mail_id", "address", "city", "state",
            "zip_code", "country", "PRICNG_ZIP_STATE", "CLM_TYPE", "SRVC_FROM_DT",
            "HCID", "PAT_BRTH_DT", "PAT_FRST_NME", "PAT_LAST_NME", "ClaimDetails"
        ]
        
        # Initialize output with empty values - will be populated from user_input.json
        for field in template_fields:
            output[field] = []
        
        # Add probability-specific data from user_input.json
        for field, values in data.items():
            if field == "ClaimDetails":
                # Handle ClaimDetails specially - ensure it uses the structure from user_input.json
                if isinstance(values, list) and len(values) > 0:
                    claim_detail = values[0]  # Take the first claim detail
                    if isinstance(claim_detail, dict):
                        # Ensure each field in ClaimDetails uses values from user_input.json
                        processed_claim = {}
                        for claim_field, claim_values in claim_detail.items():
                            if isinstance(claim_values, list) and len(claim_values) > 0:
                                # For all scenarios, randomly select one value to ensure variety
                                processed_claim[claim_field] = random.choice(claim_values)
                            else:
                                processed_claim[claim_field] = claim_values
                        output[field] = [processed_claim]
                    else:
                        output[field] = values
                else:
                    output[field] = values
            else:
                # For other fields, use values from user_input.json
                if isinstance(values, list) and len(values) > 0:
                    # For all scenarios, randomly select one value to ensure variety
                    output[field] = [random.choice(values)]
                else:
                    output[field] = values
        
        # Ensure all template fields have values (use random value from user input if available)
        for field in template_fields:
            if not output[field] or len(output[field]) == 0:
                # If field is empty, try to get a default value from the data
                if field in data and isinstance(data[field], list) and len(data[field]) > 0:
                    output[field] = [random.choice(data[field])]  # Randomly select one value
                else:
                    # Provide a fallback default value
                    output[field] = ["Default Value"]
        
        return {key_name: output}
    
    def generate_probability_scenarios(self, probability_type: str, model: str, count: int = 1, wgs: bool = False) -> List[Path]:
        """Generate probability scenarios with proper count handling.
        
        Args:
            probability_type: Type of scenario (positive, negative, exclusion)
            model: Model name to generate scenarios for
            count: Number of JSON files to generate
            wgs: Whether to use WGS format (complete template structure)
            
        Returns:
            List of generated file paths
        """
        data = self._get_probability_data(model, probability_type)
        if not data:
            raise ValueError(f"No {probability_type} data found for {model}")
        
        generated_files = []
        
        # Generate separate files for each count
        for i in range(count):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{model}_{probability_type}_{timestamp}_{i+1:06d}.json"
            filepath = self.output_dir / filename
            
            if wgs:
                # Generate WGS format output
                output = self._generate_wgs_format(data, probability_type)
            else:
                # Generate single random values for each field
                single_value_data = self._generate_single_value_data(data)
                
                # Create output structure
                output = {
                    "model": model,
                    "probability_type": probability_type,
                    "timestamp": timestamp,
                    "record_number": i + 1,
                    "data": single_value_data
                }
            
            with filepath.open("w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            generated_files.append(filepath)
        
        return generated_files
    
    def generate_all_scenarios(self, model: str, count: int = 1, wgs: bool = False) -> List[Path]:
        """Generate all available scenario types (positive, negative, exclusion) for a model.
        
        Args:
            model: Model name to generate scenarios for
            count: Number of JSON files to generate for each scenario type
            wgs: Whether to use WGS format (complete template structure)
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        # Get available probability types for this model
        available_types = []
        for prob_type in ["positive", "negative", "exclusion"]:
            data = self._get_probability_data(model, prob_type)
            if data:
                available_types.append(prob_type)
        
        if not available_types:
            raise ValueError(f"No probability data found for model {model}")
        
        # Generate scenarios for each available type
        for prob_type in available_types:
            try:
                files = self.generate_probability_scenarios(prob_type, model, count, wgs)
                generated_files.extend(files)
            except Exception as e:
                print(f"Warning: Failed to generate {prob_type} scenarios for {model}: {e}")
                continue
        
        return generated_files
    
    def list_models(self) -> Dict[str, Dict[str, bool]]:
        """List available models and their probability types.
        
        Returns:
            Dictionary mapping model names to their available probability types
        """
        models = self._get_model_names()
        result = {}
        
        for model in models:
            result[model] = {}
            for prob_type in ["positive", "negative", "exclusion"]:
                data = self._get_probability_data(model, prob_type)
                result[model][prob_type] = data is not None
        
        return result
    
    def validate_config(self) -> List[str]:
        """Validate configuration file for common issues.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not self.config:
            errors.append("Configuration file is empty")
            return errors
        
        # Check for required probability types
        required_types = ["positive", "negative", "exclusion"]
        
        for model in self._get_model_names():
            for prob_type in required_types:
                data = self._get_probability_data(model, prob_type)
                if not data:
                    errors.append(f"Missing {prob_type} data for model {model}")
        
        return errors
