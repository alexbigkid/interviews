#!/usr/bin/env python3
"""
File Processing Utility - DevOps Example

This script demonstrates common file operations in DevOps scenarios:
- Batch processing files
- File monitoring and watching
- Configuration file parsing
- Log file rotation
- Directory synchronization

Key Python concepts demonstrated:
- Path manipulation with pathlib
- Context managers for file handling
- Generator expressions for memory efficiency
- Exception handling for robust operations
- Concurrent I/O with threading
"""

import os
import shutil
import hashlib
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Generator, List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import json
import yaml


class FileProcessor:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.processed_files = set()
        self.lock = threading.Lock()
    
    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file for integrity checking."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def find_files_by_pattern(self, pattern: str, recursive: bool = True) -> Generator[Path, None, None]:
        """Find files matching a pattern using generators for memory efficiency."""
        search_path = self.base_path
        if recursive:
            yield from search_path.rglob(pattern)
        else:
            yield from search_path.glob(pattern)
    
    def batch_rename_files(self, pattern: str, new_pattern: str) -> Dict[str, str]:
        """Batch rename files with logging of changes."""
        renamed_files = {}
        
        for file_path in self.find_files_by_pattern(pattern):
            if file_path.is_file():
                # Create new name by replacing pattern
                new_name = file_path.name.replace(pattern.replace("*", ""), new_pattern)
                new_path = file_path.parent / new_name
                
                try:
                    file_path.rename(new_path)
                    renamed_files[str(file_path)] = str(new_path)
                    print(f"Renamed: {file_path.name} -> {new_name}")
                except OSError as e:
                    print(f"Error renaming {file_path}: {e}")
        
        return renamed_files
    
    def compress_old_logs(self, log_dir: str, days_old: int = 7) -> List[str]:
        """Compress log files older than specified days."""
        import gzip
        
        log_path = Path(log_dir)
        compressed_files = []
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        
        for log_file in log_path.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                compressed_path = log_file.with_suffix(".log.gz")
                
                try:
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    log_file.unlink()  # Remove original
                    compressed_files.append(str(compressed_path))
                    print(f"Compressed: {log_file.name}")
                    
                except Exception as e:
                    print(f"Error compressing {log_file}: {e}")
        
        return compressed_files
    
    def sync_directories(self, source: str, destination: str, dry_run: bool = False) -> Dict[str, List[str]]:
        """Synchronize two directories with detailed reporting."""
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source directory {source} does not exist")
        
        # Ensure destination exists
        if not dry_run:
            dest_path.mkdir(parents=True, exist_ok=True)
        
        sync_report = {
            "copied": [],
            "updated": [],
            "skipped": [],
            "errors": []
        }
        
        for source_file in source_path.rglob("*"):
            if source_file.is_file():
                relative_path = source_file.relative_to(source_path)
                dest_file = dest_path / relative_path
                
                try:
                    # Check if file needs to be copied/updated
                    if not dest_file.exists():
                        if not dry_run:
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(source_file, dest_file)
                        sync_report["copied"].append(str(relative_path))
                        
                    elif source_file.stat().st_mtime > dest_file.stat().st_mtime:
                        if not dry_run:
                            shutil.copy2(source_file, dest_file)
                        sync_report["updated"].append(str(relative_path))
                        
                    else:
                        sync_report["skipped"].append(str(relative_path))
                        
                except Exception as e:
                    sync_report["errors"].append(f"{relative_path}: {e}")
        
        return sync_report
    
    def monitor_directory(self, directory: str, callback=None, interval: int = 5):
        """Monitor directory for changes (simplified file watcher)."""
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory {directory} does not exist")
        
        print(f"Monitoring {directory} for changes...")
        file_states = {}
        
        # Initial scan
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                file_states[str(file_path)] = file_path.stat().st_mtime
        
        try:
            while True:
                time.sleep(interval)
                current_files = {}
                
                # Scan for changes
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        current_mtime = file_path.stat().st_mtime
                        file_str = str(file_path)
                        current_files[file_str] = current_mtime
                        
                        # Check for new or modified files
                        if file_str not in file_states:
                            print(f"New file detected: {file_path.name}")
                            if callback:
                                callback("created", file_path)
                                
                        elif file_states[file_str] != current_mtime:
                            print(f"File modified: {file_path.name}")
                            if callback:
                                callback("modified", file_path)
                
                # Check for deleted files
                for file_str in file_states:
                    if file_str not in current_files:
                        print(f"File deleted: {Path(file_str).name}")
                        if callback:
                            callback("deleted", Path(file_str))
                
                file_states = current_files
                
        except KeyboardInterrupt:
            print("\nStopping directory monitor...")
    
    def process_config_files(self, config_dir: str) -> Dict[str, Dict]:
        """Process and validate configuration files (JSON, YAML)."""
        config_path = Path(config_dir)
        configs = {}
        
        for config_file in config_path.glob("*.{json,yaml,yml}"):
            try:
                with open(config_file, 'r') as f:
                    if config_file.suffix.lower() == '.json':
                        data = json.load(f)
                    else:  # YAML
                        data = yaml.safe_load(f)
                
                configs[config_file.name] = data
                print(f"Loaded config: {config_file.name}")
                
            except Exception as e:
                print(f"Error loading {config_file}: {e}")
                configs[config_file.name] = {"error": str(e)}
        
        return configs
    
    def parallel_file_processing(self, file_pattern: str, processor_func, max_workers: int = 4):
        """Process files in parallel using ThreadPoolExecutor."""
        files_to_process = list(self.find_files_by_pattern(file_pattern))
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(processor_func, file_path): file_path 
                for file_path in files_to_process
            }
            
            # Collect results
            for future in future_to_file:
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append((file_path, result))
                    print(f"Processed: {file_path.name}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    results.append((file_path, None))
        
        return results


def example_file_processor():
    """Example usage of the FileProcessor class."""
    processor = FileProcessor()
    
    # Create some example files for demonstration
    example_dir = Path("example_files")
    example_dir.mkdir(exist_ok=True)
    
    # Create sample files
    sample_files = [
        "app.log",
        "error.log", 
        "access.log",
        "config.json",
        "settings.yaml"
    ]
    
    for filename in sample_files:
        file_path = example_dir / filename
        with open(file_path, 'w') as f:
            if filename.endswith('.json'):
                json.dump({"app": "example", "version": "1.0"}, f)
            elif filename.endswith('.yaml'):
                yaml.dump({"database": {"host": "localhost", "port": 5432}}, f)
            else:
                f.write(f"Sample log entry for {filename}\n")
                f.write(f"Timestamp: {datetime.now()}\n")
    
    print("=== File Processing Examples ===\n")
    
    # Example 1: Find files by pattern
    print("1. Finding log files:")
    log_files = list(processor.find_files_by_pattern("*.log"))
    for log_file in log_files:
        print(f"   Found: {log_file}")
    
    # Example 2: Calculate file hashes
    print("\n2. File integrity checking:")
    for log_file in log_files[:2]:  # Just check first 2
        hash_value = processor.get_file_hash(log_file)
        print(f"   {log_file.name}: {hash_value}")
    
    # Example 3: Process config files
    print("\n3. Loading configuration files:")
    configs = processor.process_config_files("example_files")
    for config_name, config_data in configs.items():
        print(f"   {config_name}: {config_data}")
    
    # Example 4: Parallel processing
    print("\n4. Parallel file hash calculation:")
    def calculate_hash(file_path):
        return processor.get_file_hash(file_path)
    
    results = processor.parallel_file_processing("*.log", calculate_hash, max_workers=2)
    for file_path, hash_result in results:
        print(f"   {file_path.name}: {hash_result}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    # Run the example
    example_file_processor()
    
    # Uncomment to test directory monitoring (will run indefinitely)
    # processor = FileProcessor()
    # processor.monitor_directory("example_files", interval=3)