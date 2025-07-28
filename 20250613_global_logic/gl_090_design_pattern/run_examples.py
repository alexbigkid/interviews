#!/usr/bin/env python3
"""
Script to run all design pattern examples
"""

import sys
import subprocess
from pathlib import Path

PATTERNS = [
    "singleton",
    "factory", 
    "observer",
    "strategy",
    "command",
    "decorator",
    "adapter", 
    "builder"
]

def run_pattern(pattern_name):
    """Run a specific pattern example"""
    pattern_file = f"src/design_patterns/{pattern_name}.py"
    print(f"\n{'='*50}")
    print(f"Running {pattern_name.title()} Pattern Example")
    print('='*50)
    
    try:
        result = subprocess.run([sys.executable, pattern_file], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running {pattern_name}: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

def main():
    """Run all pattern examples"""
    print("Design Patterns Examples")
    print("========================")
    
    for pattern in PATTERNS:
        run_pattern(pattern)
    
    print(f"\n{'='*50}")
    print("All examples completed!")
    print('='*50)

if __name__ == "__main__":
    main()