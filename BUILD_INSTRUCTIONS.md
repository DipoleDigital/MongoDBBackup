# MongoDB Backup Tool - Build Instructions

This guide explains how to create executable files for the MongoDB Backup Tool that work on both Windows and macOS.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build Executable
```bash
python build_executable.py
```

### 3. Find Your Executable
The executable will be created in the `dist/` directory:
- **Windows**: `MongoDB_Backup_Tool_Windows.exe`
- **macOS**: `MongoDB_Backup_Tool_macOS.app`

## Detailed Build Process

### Prerequisites

#### For Windows:
- Python 3.7+ installed
- Windows 10/11
- Administrator privileges (for some installations)

#### For macOS:
- Python 3.7+ installed
- macOS 10.14+ (Mojave or later)
- Xcode Command Line Tools (run `xcode-select --install`)

### Step-by-Step Build Process

#### 1. Clone/Download the Project
```bash
git clone <your-repo-url>
cd MongoDBbackup
```

#### 2. Install Python Dependencies
```bash
# Install all dependencies including build tools
pip install -r requirements.txt

# Verify PyInstaller installation
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)"
```

#### 3. Build for Current Platform
```bash
# Build for your current operating system
python build_executable.py
```

#### 4. Build for Specific Platform
```bash
# Build for Windows (on Windows machine)
python build_executable.py --platform windows

# Build for macOS (on macOS machine)
python build_executable.py --platform macos
```

#### 5. Clean Build (if needed)
```bash
# Clean previous builds and rebuild
python build_executable.py --clean
```

### Build Output

After successful build, you'll find:

```
dist/
├── MongoDB_Backup_Tool_Distribution/          # Complete distribution package
│   ├── MongoDB_Backup_Tool_Windows.exe        # Windows executable
│   ├── MongoDB_Backup_Tool_macOS.app          # macOS application
│   ├── install_windows.bat                    # Windows installer script
│   ├── install_macos.sh                      # macOS installer script
│   ├── README.md                             # Documentation
│   ├── requirements.txt                      # Dependencies
│   └── mongodb_restore.py                    # Restore script
├── MongoDB_Backup_Tool_Windows.exe            # Standalone Windows executable
└── MongoDB_Backup_Tool_macOS.app             # Standalone macOS application
```

## Cross-Platform Building

### Building for Multiple Platforms

To create executables for both Windows and macOS, you need to build on each platform:

#### Windows Machine:
```bash
python build_executable.py --platform windows
```

#### macOS Machine:
```bash
python build_executable.py --platform macos
```

### Alternative: Using Virtual Machines

If you only have one platform, you can use virtual machines:

1. **Windows on macOS**: Use Parallels Desktop or VMware Fusion
2. **macOS on Windows**: Use VMware Workstation (requires macOS license)

## Distribution

### Creating Distribution Package

The build script automatically creates a complete distribution package in `dist/MongoDB_Backup_Tool_Distribution/` containing:

- Executables for both platforms
- Installer scripts
- Documentation
- Dependencies list

### Sharing Your Application

#### Option 1: Share the Distribution Folder
1. Zip the `MongoDB_Backup_Tool_Distribution` folder
2. Share the zip file
3. Users extract and run the appropriate executable

#### Option 2: Share Individual Executables
1. Share `MongoDB_Backup_Tool_Windows.exe` for Windows users
2. Share `MongoDB_Backup_Tool_macOS.app` for macOS users
3. Include `README.md` and `requirements.txt` for reference

### User Installation

#### For Windows Users:
1. Download `MongoDB_Backup_Tool_Windows.exe`
2. Double-click to run (no installation required)
3. Or run `install_windows.bat` for dependency installation

#### For macOS Users:
1. Download `MongoDB_Backup_Tool_macOS.app`
2. Double-click to run (may need to allow in Security & Privacy)
3. Or run `install_macos.sh` for dependency installation

## Troubleshooting

### Common Build Issues

#### 1. PyInstaller Not Found
```bash
# Solution: Install PyInstaller
pip install pyinstaller
```

#### 2. Missing Dependencies
```bash
# Solution: Install all requirements
pip install -r requirements.txt
```

#### 3. Permission Errors (macOS)
```bash
# Solution: Grant permissions
chmod +x build_executable.py
```

#### 4. Windows Defender Blocking
- Add the project folder to Windows Defender exclusions
- Or temporarily disable real-time protection during build

#### 5. macOS Security Warnings
```bash
# Solution: Allow the application
# Go to System Preferences > Security & Privacy > General
# Click "Allow" next to the blocked application
```

### Build Logs

Check these files for build information:
- `build/` - Temporary build files
- `dist/` - Final executables
- Console output during build process

### Testing Your Executable

#### Windows:
```cmd
# Navigate to dist folder
cd dist
# Run the executable
MongoDB_Backup_Tool_Windows.exe
```

#### macOS:
```bash
# Navigate to dist folder
cd dist
# Run the application
open "MongoDB_Backup_Tool_macOS.app"
```

## Advanced Configuration

### Custom Icons

To add custom icons:

1. **Windows**: Place `icon.ico` in project root
2. **macOS**: Place `icon.icns` in project root

The build script will automatically detect and use these icons.

### Custom Build Options

You can modify `build_executable.py` to:
- Add additional data files
- Change executable names
- Modify build parameters
- Add custom hooks

### Spec File Customization

The build script creates PyInstaller spec files in `specs/` directory:
- `mongodb_backup_windows.spec` - Windows configuration
- `mongodb_backup_macos.spec` - macOS configuration

You can modify these files for advanced customization.

## Performance Optimization

### Reducing Executable Size

1. **Exclude unnecessary modules**:
   ```python
   # In spec files, add to excludes list:
   excludes=['matplotlib', 'numpy', 'pandas']
   ```

2. **Use UPX compression** (already enabled):
   ```python
   upx=True  # In spec files
   ```

3. **Remove debug information**:
   ```python
   debug=False  # In spec files
   ```

### Build Time Optimization

1. **Use virtual environments** to avoid conflicts
2. **Clean builds** when switching platforms
3. **Use SSD storage** for faster I/O

## Security Considerations

### Code Signing (Optional)

#### Windows:
```bash
# Sign the executable (requires certificate)
signtool sign /f certificate.pfx /p password MongoDB_Backup_Tool_Windows.exe
```

#### macOS:
```bash
# Sign the application (requires Apple Developer account)
codesign --force --sign "Developer ID Application: Your Name" MongoDB_Backup_Tool_macOS.app
```

### Antivirus Considerations

Some antivirus software may flag PyInstaller executables as suspicious. This is normal and can be resolved by:

1. Adding the executable to antivirus exclusions
2. Code signing the executable
3. Submitting to antivirus vendors for whitelisting

## Support

If you encounter issues:

1. Check the build logs in console output
2. Verify all dependencies are installed
3. Ensure you have sufficient disk space
4. Try a clean build with `--clean` flag

For additional help, check the main README.md file or create an issue in the project repository.
