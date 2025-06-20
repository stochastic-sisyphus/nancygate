#!/usr/bin/env python3
"""
Setup script for NancyGate Congressional Trading Analysis Pipeline
"""

import os
import sys
from pathlib import Path

def main():
    print("nancygate setup")
    print("=" * 50)
    
    # Create required directories
    directories = ['data', 'export', 'config', 'fetch', 'enrich']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ created directory: {dir_name}/")
    
    # Check for .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("\n⚠️  no .env file found!")
        print("creating .env file...")
        
        api_key = input("enter your quiver quant api key (or press enter to use default): ").strip()
        
        if not api_key:
            api_key = "8e52d77555c830932c8343a44c426f6d20e876fd"
            print("using default api key")
        
        with open('.env', 'w') as f:
            f.write(f"# nancygate api configuration\n")
            f.write(f"NANCYGATE_API_KEY={api_key}\n")
        
        print("✓ created .env file")
    else:
        print("✓ .env file exists")
    
    # Install dependencies
    print("\ninstalling dependencies...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    print("\n✅ setup complete!")
    print("\nnext steps:")
    print("1. test connection: python nancygate_cli.py test-connection")
    print("2. fetch data: python nancygate_cli.py fetch-all --max-pages 5")
    print("3. analyze data: python nancygate_cli.py analyze")

if __name__ == "__main__":
    main() 