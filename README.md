# MongoDB Backup & Restore Tool with GUI

A comprehensive Python application for backing up and restoring MongoDB collections with a user-friendly GUI interface. Supports VPN connections and preserves MongoDB data types using Extended JSON format.

## Features

### GUI Application (`mongodb_backup_gui_proper.py`)
- 🖥️ **User-friendly GUI interface** with tkinter
- 🔗 **VPN connection support** for remote MongoDB instances
- 📦 **Interactive collection selection** with document counts
- 💾 **Extended JSON format** preserving MongoDB data types (ObjectId, Date, etc.)
- 📊 **Real-time progress tracking** with progress bars and logging
- 🔍 **Connection testing** before backup operations
- 📁 **Organized backup structure** with metadata files
- ⚡ **Batch processing** for multiple collections

### Restore Script (`mongodb_restore.py`)
- 🔄 **Complete restore functionality** from JSON backups
- 🎯 **Selective collection restore** (single or multiple collections)
- 🗑️ **Drop existing collections** option before restore
- 📊 **Batch document insertion** for performance
- 🔒 **Authentication support** for secure connections
- 📝 **Comprehensive logging** and error handling

## Installation

### Prerequisites
- Python 3.7 or higher
- Network access to MongoDB via VPN (if applicable)
- MongoDB instance with appropriate permissions

### Setup

1. **Clone or download the project files**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python mongodb_backup_gui_proper.py
```

The GUI application should launch automatically. No additional configuration files are required - the application uses a graphical interface for all settings.

## Usage

### GUI Application (Recommended)

1. **Launch the GUI application:**
```bash
python mongodb_backup_gui_proper.py
```

2. **Configure connection:**
   - Enter VPN IP address (e.g., `192.168.1.100`)
   - Set port (default: `27017`)
   - Enter database name
   - Click "Test Connection" to verify connectivity

3. **Select collections:**
   - View all available collections with document counts
   - Use "Select All" or "Select None" buttons
   - Double-click individual collections to toggle selection

4. **Configure backup:**
   - Choose output directory (default: `./backups`)
   - Click "Start Backup" to begin the process

5. **Monitor progress:**
   - Watch real-time progress bar
   - View detailed logs in the application window
   - Check backup summary upon completion

### Restore Script

1. **Basic restore (interactive):**
```bash
python mongodb_restore.py --host <host> --database <db> --backup-dir <backup_directory>
```

2. **Restore specific collection:**
```bash
python mongodb_restore.py --host <host> --database <db> --backup-dir <backup_directory> --collection <collection_name>
```

3. **Restore with authentication:**
```bash
python mongodb_restore.py --host <host> --database <db> --backup-dir <backup_directory> --username <user> --password <pass>
```

4. **Force restore (skip confirmations):**
```bash
python mongodb_restore.py --host <host> --database <db> --backup-dir <backup_directory> --force
```

## Configuration Options

### GUI Application Settings
| Setting | Description | Default |
|---------|-------------|---------|
| **VPN IP Address** | MongoDB host IP address | Required |
| **Port** | MongoDB port number | 27017 |
| **Database** | Target database name | Required |
| **Output Directory** | Backup storage location | ./backups |

### Restore Script Options
| Option | Description | Default |
|--------|-------------|---------|
| `--host` | MongoDB host address | Required |
| `--port` | MongoDB port | 27017 |
| `--database` | Target database name | Required |
| `--backup-dir` | Path to backup directory | Required |
| `--collection` | Specific collection to restore | All collections |
| `--username` | MongoDB username | Optional |
| `--password` | MongoDB password | Optional |
| `--auth-database` | Authentication database | admin |
| `--force` | Skip confirmation prompts | False |

## Backup Output Structure

The GUI application creates a timestamped backup directory with the following structure:

```
backups/
└── database_192_168_1_100_20231201_143022/
    ├── collection1/
    │   ├── collection1.json          # Extended JSON format
    │   └── metadata.json             # Collection metadata
    ├── collection2/
    │   ├── collection2.json
    │   └── metadata.json
    └── backup_summary.json           # Overall backup summary
```

### Backup File Formats

- **JSON Files**: MongoDB Extended JSON format preserving data types
- **Metadata Files**: Collection information, document counts, timestamps
- **Summary File**: Complete backup overview with statistics

## Restore Process

### Interactive Restore
1. **Run the restore script:**
```bash
python mongodb_restore.py --host localhost --database mydb --backup-dir ./backups/database_192_168_1_100_20231201_143022
```

2. **Select collections to restore:**
   - View available collections in backup directory
   - Choose specific collections or restore all
   - Confirm drop existing collections if needed

3. **Monitor restore progress:**
   - Real-time logging of restore operations
   - Batch insertion for performance
   - Final document counts and success status

### Restore Options

| Option | Description |
|--------|-------------|
| **Drop Existing** | Remove existing collections before restore |
| **Batch Processing** | Insert documents in batches of 1000 |
| **Error Handling** | Skip invalid documents and continue |
| **Progress Tracking** | Real-time status updates |

## Examples

### GUI Application Examples

1. **Basic Backup Workflow:**
   - Launch: `python mongodb_backup_gui_proper.py`
   - Enter VPN IP: `192.168.1.100`
   - Set port: `27017`
   - Database: `production`
   - Test connection
   - Select collections (users, orders, products)
   - Choose output directory: `./my_backups`
   - Start backup

2. **Large Database Backup:**
   - Use "Select All" for all collections
   - Monitor progress bar during backup
   - Check logs for any errors
   - Review backup summary

### Restore Script Examples

1. **Restore all collections:**
```bash
python mongodb_restore.py --host localhost --database production --backup-dir ./backups/database_192_168_1_100_20231201_143022
```

2. **Restore specific collection:**
```bash
python mongodb_restore.py --host localhost --database production --backup-dir ./backups/database_192_168_1_100_20231201_143022 --collection users
```

3. **Restore with authentication:**
```bash
python mongodb_restore.py --host 192.168.1.100 --database production --backup-dir ./backups/database_192_168_1_100_20231201_143022 --username admin --password secret
```

4. **Automated restore (no prompts):**
```bash
python mongodb_restore.py --host localhost --database production --backup-dir ./backups/database_192_168_1_100_20231201_143022 --force
```

## Logging

### GUI Application Logging
- **Real-time logs** displayed in the application window
- **File logging** saved to `mongodb_backup_gui.log`
- **Progress tracking** with visual progress bars
- **Error reporting** with detailed messages

### Restore Script Logging
- **Console output** with real-time status updates
- **File logging** saved to `mongodb_restore.log`
- **Batch processing** logs for large collections
- **Error handling** with detailed error messages

## Error Handling

### GUI Application
- **Connection testing** before backup operations
- **Collection validation** with document counts
- **File system checks** for output directories
- **Network timeout handling** with user feedback

### Restore Script
- **Backup validation** before restore operations
- **Document parsing** with error recovery
- **Batch insertion** with rollback on failure
- **Authentication error** handling

## Requirements

- **Python 3.7+** (tested with Python 3.8+)
- **pymongo 4.15.1+** (MongoDB driver)
- **tkinter** (GUI framework, included with Python)
- **bson** (MongoDB data format support)
- **Network access** to MongoDB via VPN (if applicable)

## Troubleshooting

### GUI Application Issues

**Application won't start:**
- Verify Python installation: `python --version`
- Check dependencies: `pip install -r requirements.txt`
- Ensure tkinter is available: `python -c "import tkinter"`

**Connection failures:**
- Verify VPN connection is active
- Check MongoDB host and port settings
- Test network connectivity: `ping <host>`
- Verify MongoDB service is running

**Backup failures:**
- Check output directory permissions
- Verify sufficient disk space
- Review log files for specific errors
- Test with smaller collections first

### Restore Script Issues

**Connection problems:**
- Verify MongoDB host and port
- Check authentication credentials
- Ensure database exists
- Test connection manually

**Restore failures:**
- Verify backup directory exists and is readable
- Check JSON file format and integrity
- Ensure target database has write permissions
- Review restore logs for specific errors

**Performance issues:**
- Use batch processing for large collections
- Consider restoring collections individually
- Monitor system resources during restore
- Check network stability for remote connections


