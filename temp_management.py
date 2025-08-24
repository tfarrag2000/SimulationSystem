#!/usr/bin/env python3
"""
TEMPORARY FILE MANAGEMENT
Centralizes temporary file creation to avoid cluttering main folder
"""

import os
import tempfile
from datetime import datetime

# Create temp directories
TEMP_BASE_DIR = os.path.join(os.getcwd(), "temp")
TEMP_OUTPUT_DIR = os.path.join(TEMP_BASE_DIR, "outputs")
TEMP_LOGS_DIR = os.path.join(TEMP_BASE_DIR, "logs")
TEMP_TESTS_DIR = os.path.join(TEMP_BASE_DIR, "tests")

def ensure_temp_dirs():
    """Ensure temp directories exist"""
    for dir_path in [TEMP_BASE_DIR, TEMP_OUTPUT_DIR, TEMP_LOGS_DIR, TEMP_TESTS_DIR]:
        os.makedirs(dir_path, exist_ok=True)

def get_temp_file_path(filename, subdir="outputs"):
    """Get path for temporary file in appropriate subdirectory"""
    ensure_temp_dirs()
    
    if subdir == "outputs":
        return os.path.join(TEMP_OUTPUT_DIR, filename)
    elif subdir == "logs":
        return os.path.join(TEMP_LOGS_DIR, filename)
    elif subdir == "tests":
        return os.path.join(TEMP_TESTS_DIR, filename)
    else:
        return os.path.join(TEMP_BASE_DIR, filename)

def cleanup_temp_files(older_than_hours=24):
    """Clean up temporary files older than specified hours"""
    import time
    
    ensure_temp_dirs()
    current_time = time.time()
    cutoff_time = current_time - (older_than_hours * 3600)
    
    for root, dirs, files in os.walk(TEMP_BASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff_time:
                try:
                    os.remove(file_path)
                    print(f"Cleaned up: {file_path}")
                except:
                    pass

if __name__ == "__main__":
    # Clean up old temp files when run directly
    cleanup_temp_files()
    print("✅ Temporary file cleanup complete")
