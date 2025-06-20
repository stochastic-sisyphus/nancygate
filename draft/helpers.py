
import json
import toml

def load_config(file_path):
    """Load configuration from a TOML or JSON file."""
    if file_path.endswith('.toml'):
        with open(file_path, 'r') as f:
            return toml.load(f)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format")

def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def format_currency(value):
    """Format a number as currency."""
    return "${:,.2f}".format(value)
