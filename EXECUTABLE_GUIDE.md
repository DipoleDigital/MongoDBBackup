# MongoDB Backup Tool - Executable Guide

This guide explains how to create and distribute executable files for the MongoDB Backup Tool that work on both Windows and macOS.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build Executable
```bash
python build_simple.py
```

### 3. Find Your Executable
The executable will be created in the `dist/` directory:
- **Windows**: `MongoDB_Backup_Tool_Windows.exe` (16.1 MB)
- **macOS**: `MongoDB_Backup_Tool_macOS` (similar size)

## What You Get

### Executable Features
- ✅ **Standalone executable** - No Python installation required
- ✅ **Cross-platform** - Works on Windows and macOS
- ✅ **GUI interface** - User-friendly graphical interface
- ✅ **All dependencies included** - PyMongo, tkinter, etc.
- ✅ **Small file size** - ~16 MB (optimized with UPX compression)
- ✅ **No console window** - Clean GUI-only experience

### Distribution Ready
- ✅ **Single file** - Easy to share and distribute
- ✅ **No installation** - Users can run directly
- ✅ **Portable** - Can run from any location
- ✅ **Self-contained** - All libraries included

## Building Executables

### Method 1: Simple Build (Recommended)
```bash
# Build for your current platform
python build_simple.py
```

### Method 2: Advanced Build
```bash
# Build with more options
python build_executable.py --clean
```

### Method 3: Manual Build
```bash
# Windows
python -m PyInstaller --onefile --windowed --name MongoDB_Backup_Tool_Windows mongodb_backup_gui_proper.py

# macOS
python -m PyInstaller --onefile --windowed --name MongoDB_Backup_Tool_macOS mongodb_backup_gui_proper.py
```

## Cross-Platform Building

### Windows Executable
- **Platform**: Windows 10/11
- **Requirements**: Python 3.7+, PyInstaller
- **Output**: `MongoDB_Backup_Tool_Windows.exe`
- **Size**: ~16 MB

### macOS Executable
- **Platform**: macOS 10.14+ (Mojave or later)
- **Requirements**: Python 3.7+, PyInstaller, Xcode Command Line Tools
- **Output**: `MongoDB_Backup_Tool_macOS`
- **Size**: ~16 MB

## Distribution

### Sharing Your Application

#### Option 1: Direct Distribution
1. Share the executable file directly
2. Users download and run immediately
3. No installation required

#### Option 2: Package Distribution
1. Create a zip file with:
   - Executable file
   - README.md
   - requirements.txt (for reference)
2. Share the zip file
3. Users extract and run

### User Instructions

#### For Windows Users:
1. Download `MongoDB_Backup_Tool_Windows.exe`
2. Double-click to run
3. If Windows Defender blocks it:
   - Click "More info"
   - Click "Run anyway"

#### For macOS Users:
1. Download `MongoDB_Backup_Tool_macOS`
2. Right-click and select "Open"
3. If macOS blocks it:
   - Go to System Preferences > Security & Privacy
   - Click "Allow" next to the blocked application

## Testing Your Executable

### Basic Test
```bash
# Navigate to dist folder
cd dist

# Windows
MongoDB_Backup_Tool_Windows.exe

# macOS
./MongoDB_Backup_Tool_macOS
```

### Functionality Test
1. **Launch the application**
2. **Test connection** with a MongoDB instance
3. **Select collections** to backup
4. **Start backup** process
5. **Verify backup files** are created

## Troubleshooting

### Common Issues

#### 1. "App can't be opened because it is from an unidentified developer" (macOS)
**Solution**: Right-click the app → Open → Click "Open"

#### 2. Windows Defender blocks the executable
**Solution**: 
- Click "More info" → "Run anyway"
- Or add to Windows Defender exclusions

#### 3. Executable is too large
**Solution**: 
- Use `--onefile` option (already enabled)
- UPX compression is automatically applied
- Consider excluding unnecessary modules

#### 4. Missing dependencies in executable
**Solution**: 
- Check PyInstaller version: `pip install --upgrade pyinstaller`
- Rebuild with clean cache: `python build_simple.py`

### Build Issues

#### 1. PyInstaller not found
```bash
pip install pyinstaller
```

#### 2. Missing Python dependencies
```bash
pip install -r requirements.txt
```

#### 3. Build fails with errors
```bash
# Clean and rebuild
rm -rf build dist
python build_simple.py
```

## Performance Optimization

### Reducing Executable Size
- ✅ **UPX compression** - Automatically applied
- ✅ **One-file mode** - Single executable
- ✅ **Excluded unnecessary modules** - Only required dependencies
- ✅ **Optimized imports** - Only used modules included

### Build Time Optimization
- ✅ **Clean builds** - Remove old build artifacts
- ✅ **Cached dependencies** - PyInstaller caches modules
- ✅ **Parallel processing** - Multi-core build support

## Security Considerations

### Code Signing (Optional)
For production distribution, consider code signing:

#### Windows:
```bash
# Sign with certificate
signtool sign /f certificate.pfx /p password MongoDB_Backup_Tool_Windows.exe
```

#### macOS:
```bash
# Sign with Apple Developer ID
codesign --force --sign "Developer ID Application: Your Name" MongoDB_Backup_Tool_macOS
```

### Antivirus Considerations
- Some antivirus software may flag PyInstaller executables
- This is normal and can be resolved by:
  - Adding to antivirus exclusions
  - Code signing the executable
  - Submitting to antivirus vendors for whitelisting

## Advanced Configuration

### Custom Icons
To add custom icons:
1. **Windows**: Place `icon.ico` in project root
2. **macOS**: Place `icon.icns` in project root
3. Rebuild the executable

### Custom Build Options
You can modify the build scripts to:
- Add additional data files
- Change executable names
- Modify build parameters
- Add custom hooks

## Support

### Getting Help
1. Check the build logs for specific errors
2. Verify all dependencies are installed
3. Ensure sufficient disk space
4. Try a clean build

### Documentation
- Main README.md - Application usage
- BUILD_INSTRUCTIONS.md - Detailed build process
- EXECUTABLE_GUIDE.md - This guide

## Summary

Your MongoDB Backup Tool is now ready for distribution as a standalone executable! 

**Key Benefits:**
- ✅ No Python installation required for users
- ✅ Works on both Windows and macOS
- ✅ Single file distribution
- ✅ Professional GUI interface
- ✅ All MongoDB functionality included

**Next Steps:**
1. Test the executable thoroughly
2. Create distribution package
3. Share with your users
4. Collect feedback and iterate

The executable provides the same functionality as the Python script but in a user-friendly, distributable format that works across different systems without requiring Python installation.
