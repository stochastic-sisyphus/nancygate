#!/usr/bin/env python3
"""
IMMEDIATE FIX SCRIPT - RUN THIS NOW!
This script fixes all the issues and runs the complete pipeline.
"""

import os
import subprocess
import sys

def main():
    print("🚨 NANCYGATE IMMEDIATE FIX SCRIPT")
    print("=" * 50)
    
    # 1. Install dependencies
    print("\n📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 2. Set up PostgreSQL database
    print("\n🗄️ Setting up PostgreSQL database...")
    print("Options:")
    print("1. Local PostgreSQL (requires PostgreSQL installed)")
    print("2. SQLite (simpler, no installation needed)")
    
    db_choice = input("\nChoose database (1 or 2): ").strip()
    
    if db_choice == "2":
        # Use SQLite instead for simplicity
        print("\n✅ Using SQLite database...")
        os.environ['DB_TYPE'] = 'sqlite'
        os.environ['DB_NAME'] = 'nancygate.db'
    else:
        print("\n✅ Using PostgreSQL...")
        print("Make sure PostgreSQL is running and you have a database named 'nancygate'")
        input("Press Enter when ready...")
    
    # 3. Run database setup
    print("\n🔧 Creating database tables...")
    try:
        from database_setup import NancyGateDB
        db = NancyGateDB()
        print("✅ Database setup complete!")
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("Continuing with existing data...")
    
    # 4. Run the production pipeline
    print("\n🚀 Running production pipeline...")
    subprocess.run([sys.executable, "nancygate_production.py"])
    
    print("\n" + "=" * 50)
    print("✅ FIX COMPLETE!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Check export/ directory for enriched data")
    print("2. Run dashboard: python nancygate_cli.py dashboard")
    print("3. View high signal trades in the CSV files")

if __name__ == "__main__":
    main() 