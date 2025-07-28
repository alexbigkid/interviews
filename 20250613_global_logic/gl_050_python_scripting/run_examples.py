#!/usr/bin/env python3
"""
Example Runner - DevOps Python Examples

This script helps you run all the Python examples in the repository.
Demonstrates how to structure and organize multiple Python applications.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_example(example_dir: str, script_name: str, description: str):
    """Run a specific example with error handling."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Directory: {example_dir}")
    print(f"{'='*60}")
    
    script_path = Path(example_dir) / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        # Change to the example directory
        original_dir = os.getcwd()
        os.chdir(example_dir)
        
        # Run the script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True)
        
        # Return to original directory
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        os.chdir(original_dir)  # Ensure we return to original directory
        return False


def main():
    """Run all Python examples."""
    print("🐍 Python DevOps Examples Runner")
    print("=" * 60)
    
    examples = [
        ("file_processor", "file_processor.py", "File Processing Utility"),
        ("web_scraper", "web_scraper.py", "Web Scraper with Error Handling"),
        ("log_analyzer", "log_analyzer.py", "Log Analyzer with Regex"),
        ("system_monitor", "system_monitor.py", "System Monitor")
    ]
    
    successful = 0
    total = len(examples)
    
    for example_dir, script_name, description in examples:
        if run_example(example_dir, script_name, description):
            successful += 1
        
        # Add a small delay between examples
        import time
        time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {successful}/{total} examples ran successfully")
    print(f"{'='*60}")
    
    if successful == total:
        print("🎉 All examples completed successfully!")
    else:
        print(f"⚠️  {total - successful} examples had issues")
    
    print("\n📚 For more information, check the README.md file")
    print("🔧 To run individual examples:")
    for example_dir, script_name, description in examples:
        print(f"   cd {example_dir} && python {script_name}")


if __name__ == "__main__":
    main()