#!/usr/bin/env python3
"""
Build script for creating executables on all platforms.
This script detects the current platform and builds accordingly.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def build_executable():
    """Build executable for current platform."""
    print("MongoDB Backup Tool - Cross-Platform Builder")
    print("=" * 50)
    
    current_platform = platform.system().lower()
    print(f"Detected platform: {current_platform}")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("[ERROR] PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Check dependencies
    try:
        import pymongo
        import tkinter
        from bson import json_util
        print("[OK] All dependencies found")
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        return False
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    print("[OK] Cleaned previous builds")
    
    # Build command based on platform
    if current_platform == "windows":
        exe_name = "MongoDB_Backup_Tool_Windows.exe"
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MongoDB_Backup_Tool_Windows",
            "--add-data", "requirements.txt;.",
            "--add-data", "README.md;.",
            "mongodb_backup_gui_proper.py"
        ]
    elif current_platform == "darwin":  # macOS
        exe_name = "MongoDB_Backup_Tool_macOS"
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MongoDB_Backup_Tool_macOS",
            "--add-data", "requirements.txt:.",
            "--add-data", "README.md:.",
            "mongodb_backup_gui_proper.py"
        ]
    elif current_platform == "linux":
        exe_name = "MongoDB_Backup_Tool_Linux"
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", "MongoDB_Backup_Tool_Linux",
            "--add-data", "requirements.txt:.",
            "--add-data", "README.md:.",
            "mongodb_backup_gui_proper.py"
        ]
    else:
        print(f"[ERROR] Unsupported platform: {current_platform}")
        return False
    
    print(f"Building for {current_platform}...")
    
    try:
        subprocess.run(cmd, check=True)
        print("[OK] Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path("dist") / exe_name
        
        if exe_path.exists():
            print(f"[OK] Executable created: {exe_path}")
            print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Make executable on Unix systems
            if current_platform in ["darwin", "linux"]:
                os.chmod(exe_path, 0o755)
                print("[OK] Made executable")
            
            return True
        else:
            print("[ERROR] Executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False

def show_platform_info():
    """Show information about cross-platform building."""
    print("\n" + "=" * 50)
    print("CROSS-PLATFORM BUILDING INFO")
    print("=" * 50)
    print("To get executables for all platforms:")
    print()
    print("1. WINDOWS EXECUTABLE:")
    print("   - Run this script on Windows")
    print("   - Creates: MongoDB_Backup_Tool_Windows.exe")
    print()
    print("2. MACOS EXECUTABLE:")
    print("   - Run this script on macOS")
    print("   - Creates: MongoDB_Backup_Tool_macOS")
    print()
    print("3. LINUX EXECUTABLE:")
    print("   - Run this script on Linux")
    print("   - Creates: MongoDB_Backup_Tool_Linux")
    print()
    print("4. AUTOMATED BUILDING:")
    print("   - Use GitHub Actions (see .github/workflows/build.yml)")
    print("   - Pushes to GitHub automatically build all platforms")
    print("   - Download executables from GitHub Releases")
    print()
    print("5. CURRENT PLATFORM:")
    current_platform = platform.system().lower()
    print(f"   - You are on: {current_platform}")
    if current_platform == "windows":
        print("   - You can create: Windows executable")
        print("   - For macOS: Use GitHub Actions or find a Mac")
    elif current_platform == "darwin":
        print("   - You can create: macOS executable")
        print("   - For Windows: Use GitHub Actions or find a Windows PC")
    elif current_platform == "linux":
        print("   - You can create: Linux executable")
        print("   - For others: Use GitHub Actions or find other platforms")

def main():
    """Main function."""
    show_platform_info()
    
    print("\n" + "=" * 50)
    print("BUILDING FOR CURRENT PLATFORM")
    print("=" * 50)
    
    success = build_executable()
    
    if success:
        print("\n" + "=" * 50)
        print("BUILD SUCCESSFUL!")
        print("=" * 50)
        print("Your executable is ready in the 'dist' folder.")
        print("For other platforms, see the information above.")
    else:
        print("\n" + "=" * 50)
        print("BUILD FAILED!")
        print("=" * 50)
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
