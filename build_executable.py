#!/usr/bin/env python3
"""
Build script for creating cross-platform MongoDB Backup Tool executables.
Supports Windows (.exe) and macOS (.app) builds using PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class ExecutableBuilder:
    """Builds executables for MongoDB Backup Tool."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.spec_dir = self.project_root / "specs"
        
        # Create directories
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        self.spec_dir.mkdir(exist_ok=True)
        
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        try:
            import PyInstaller
            print(f"[OK] PyInstaller {PyInstaller.__version__} found")
        except ImportError:
            print("[ERROR] PyInstaller not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            
        # Check if all required packages are available
        required_packages = ["pymongo", "tkinter"]
        for package in required_packages:
            try:
                __import__(package)
                print(f"[OK] {package} found")
            except ImportError:
                print(f"[ERROR] {package} not found")
                return False
        
        # Check bson separately as it's part of pymongo
        try:
            from bson import json_util
            print(f"[OK] bson.json_util found")
        except ImportError:
            print(f"[ERROR] bson.json_util not found")
            return False
        return True
    
    def create_spec_files(self):
        """Create PyInstaller spec files for different platforms."""
        
        # Windows spec file
        windows_spec = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mongodb_backup_gui_proper.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'pymongo',
        'bson',
        'bson.json_util',
        'pymongo.errors',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MongoDB_Backup_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
        
        # macOS spec file
        macos_spec = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mongodb_backup_gui_proper.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'pymongo',
        'bson',
        'bson.json_util',
        'pymongo.errors',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MongoDB_Backup_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.icns' if os.path.exists('icon.icns') else None,
)

app = BUNDLE(
    exe,
    name='MongoDB Backup Tool.app',
    icon='icon.icns' if os.path.exists('icon.icns') else None,
    bundle_identifier='com.mongodb.backup.tool',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
    },
)
'''
        
        # Write spec files
        with open(self.spec_dir / "mongodb_backup_windows.spec", "w") as f:
            f.write(windows_spec)
            
        with open(self.spec_dir / "mongodb_backup_macos.spec", "w") as f:
            f.write(macos_spec)
            
        print("[OK] Spec files created")
    
    def build_windows(self):
        """Build Windows executable."""
        print("Building Windows executable...")
        
        spec_file = self.spec_dir / "mongodb_backup_windows.spec"
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_file)
        ]
        
        try:
            # Run from the project root
            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("[OK] Windows executable built successfully")
            
            # Copy to dist with platform suffix
            exe_path = self.dist_dir / "MongoDB_Backup_Tool.exe"
            if exe_path.exists():
                final_path = self.dist_dir / "MongoDB_Backup_Tool_Windows.exe"
                shutil.copy2(exe_path, final_path)
                print(f"[OK] Windows executable saved as: {final_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Windows build failed: {e}")
            return False
        return True
    
    def build_macos(self):
        """Build macOS application."""
        print("Building macOS application...")
        
        spec_file = self.spec_dir / "mongodb_backup_macos.spec"
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_file)
        ]
        
        try:
            # Run from the project root
            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("[OK] macOS application built successfully")
            
            # Copy to dist with platform suffix
            app_path = self.dist_dir / "MongoDB Backup Tool.app"
            if app_path.exists():
                final_path = self.dist_dir / "MongoDB_Backup_Tool_macOS.app"
                if final_path.exists():
                    shutil.rmtree(final_path)
                shutil.copytree(app_path, final_path)
                print(f"[OK] macOS application saved as: {final_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] macOS build failed: {e}")
            return False
        return True
    
    def build_current_platform(self):
        """Build for current platform."""
        current_platform = platform.system().lower()
        
        if current_platform == "windows":
            return self.build_windows()
        elif current_platform == "darwin":  # macOS
            return self.build_macos()
        else:
            print(f"Unsupported platform: {current_platform}")
            return False
    
    def build_all_platforms(self):
        """Build for all platforms (if possible)."""
        print("Building for all platforms...")
        
        # Always try to build for current platform
        current_success = self.build_current_platform()
        
        # Note: Cross-platform building requires additional setup
        print("\nNote: Cross-platform building requires:")
        print("- Windows: Use Windows machine or WINE")
        print("- macOS: Use macOS machine or virtual machine")
        print("- Linux: Use Linux machine")
        
        return current_success
    
    def create_installer_scripts(self):
        """Create installer scripts for different platforms."""
        
        # Windows batch installer
        windows_installer = '''@echo off
echo MongoDB Backup Tool - Windows Installer
echo ======================================

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Double-click MongoDB_Backup_Tool_Windows.exe
echo 2. Or run from command line: MongoDB_Backup_Tool_Windows.exe
echo.
pause
'''
        
        # macOS shell installer
        macos_installer = '''#!/bin/bash
echo "MongoDB Backup Tool - macOS Installer"
echo "======================================"

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Installation complete!"
echo ""
echo "To run the application:"
echo "1. Double-click MongoDB_Backup_Tool_macOS.app"
echo "2. Or run from terminal: open 'MongoDB_Backup_Tool_macOS.app'"
echo ""
read -p "Press Enter to continue..."
'''
        
        # Write installer scripts
        with open(self.dist_dir / "install_windows.bat", "w") as f:
            f.write(windows_installer)
            
        with open(self.dist_dir / "install_macos.sh", "w") as f:
            f.write(macos_installer)
            
        # Make macOS script executable
        os.chmod(self.dist_dir / "install_macos.sh", 0o755)
        
        print("[OK] Installer scripts created")
    
    def create_distribution_package(self):
        """Create a complete distribution package."""
        print("Creating distribution package...")
        
        # Create distribution directory
        package_dir = self.dist_dir / "MongoDB_Backup_Tool_Distribution"
        package_dir.mkdir(exist_ok=True)
        
        # Copy executables
        for exe_file in self.dist_dir.glob("MongoDB_Backup_Tool*"):
            if exe_file.is_file() or exe_file.is_dir():
                dest = package_dir / exe_file.name
                if exe_file.is_file():
                    shutil.copy2(exe_file, dest)
                else:
                    shutil.copytree(exe_file, dest)
        
        # Copy documentation and requirements
        files_to_copy = [
            "README.md",
            "requirements.txt",
            "mongodb_restore.py"
        ]
        
        for file_name in files_to_copy:
            src_file = self.project_root / file_name
            if src_file.exists():
                shutil.copy2(src_file, package_dir / file_name)
        
        # Copy installer scripts
        for installer in self.dist_dir.glob("install_*"):
            shutil.copy2(installer, package_dir / installer.name)
        
        print(f"[OK] Distribution package created: {package_dir}")
        return package_dir
    
    def clean_build(self):
        """Clean build artifacts."""
        print("Cleaning build artifacts...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            print("[OK] Build directory cleaned")
        
        # Clean dist directory but keep final executables
        for item in self.dist_dir.iterdir():
            if item.name not in ["MongoDB_Backup_Tool_Distribution"]:
                if item.is_file() and not item.name.startswith("MongoDB_Backup_Tool"):
                    item.unlink()
                elif item.is_dir() and not item.name.startswith("MongoDB_Backup_Tool"):
                    shutil.rmtree(item)
    
    def run(self, platform=None, clean=False):
        """Run the build process."""
        print("MongoDB Backup Tool - Executable Builder")
        print("=" * 50)
        
        if clean:
            self.clean_build()
        
        # Check dependencies
        if not self.check_dependencies():
            print("[ERROR] Missing dependencies. Please install required packages.")
            return False
        
        # Create spec files
        self.create_spec_files()
        
        # Build executables
        if platform == "windows":
            success = self.build_windows()
        elif platform == "macos":
            success = self.build_macos()
        elif platform == "all":
            success = self.build_all_platforms()
        else:
            success = self.build_current_platform()
        
        if success:
            # Create installer scripts
            self.create_installer_scripts()
            
            # Create distribution package
            package_dir = self.create_distribution_package()
            
            print("\n" + "=" * 50)
            print("BUILD COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print(f"Distribution package: {package_dir}")
            print("\nExecutables created:")
            for exe in self.dist_dir.glob("MongoDB_Backup_Tool*"):
                print(f"  - {exe.name}")
            print("\nTo distribute:")
            print("1. Share the entire 'MongoDB_Backup_Tool_Distribution' folder")
            print("2. Users can run the appropriate installer script")
            print("3. Or run the executable directly")
        
        return success


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build MongoDB Backup Tool executables")
    parser.add_argument("--platform", choices=["windows", "macos", "all"], 
                       help="Target platform (default: current platform)")
    parser.add_argument("--clean", action="store_true", 
                       help="Clean build artifacts before building")
    
    args = parser.parse_args()
    
    builder = ExecutableBuilder()
    success = builder.run(platform=args.platform, clean=args.clean)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
