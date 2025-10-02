# MongoDB Backup Script with VPN Support

A Python script that allows you to backup specific MongoDB collections from a remote database accessed via VPN, similar to `mongodump` but with selective collection backup capabilities.

## Features

- 🔗 Connect to MongoDB via VPN IP address
- 📦 Selective collection backup (choose which collections to backup)
- 💾 Export collections in BSON format (compatible with mongodump/mongorestore)
- 📊 Detailed logging and backup summaries
- ⚙️ Flexible configuration via JSON file or command line
- 🔒 Support for MongoDB authentication
- 📁 Organized backup output with metadata

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a configuration file:
```bash
python mongodb_backup.py --create-config
```

3. Edit the `config_sample.json` file with your MongoDB connection details and rename it to `config.json`.

## Usage

### Using Configuration File (Recommended)

1. Create and edit your configuration file:
```bash
python mongodb_backup.py --create-config
# Edit config_sample.json and rename to config.json
```

2. Run the backup:
```bash
python mongodb_backup.py --config config.json
```

### Using Command Line Arguments

```bash
python mongodb_backup.py --host <vpn_ip> --port <port> --database <db_name> --collections <collection1,collection2> --username <user> --password <pass>
```

### Interactive Collection Selection

If you don't specify collections in the configuration or command line, the script will show you all available collections and let you select which ones to backup:

```bash
python mongodb_backup.py --host 192.168.1.100 --port 27017 --database mydb
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `host` | MongoDB host (VPN IP address) | Required |
| `port` | MongoDB port | 27017 |
| `database` | Database name to backup | Required |
| `username` | MongoDB username | Optional |
| `password` | MongoDB password | Optional |
| `auth_database` | Authentication database | admin |
| `collections` | List of collections to backup | All collections |
| `output_dir` | Output directory for backups | ./backups |
| `connection_timeout` | Connection timeout (ms) | 30000 |
| `connect_timeout` | Connect timeout (ms) | 10000 |
| `socket_timeout` | Socket timeout (ms) | 30000 |
| `log_level` | Logging level | INFO |

## Output Structure

The script creates a timestamped backup directory with the following structure:

```
backups/
└── your_database_20231201_143022/
    ├── collection1/
    │   ├── collection1.bson
    │   └── metadata.json
    ├── collection2/
    │   ├── collection2.bson
    │   └── metadata.json
    └── backup_summary.json
```

## Examples

### Basic Usage
```bash
# Backup specific collections
python mongodb_backup.py --host 10.0.0.100 --port 27017 --database production --collections users,orders --username admin --password secret

# Interactive collection selection
python mongodb_backup.py --host 10.0.0.100 --port 27017 --database production --username admin --password secret
```

### Using Configuration File
```json
{
  "host": "10.0.0.100",
  "port": 27017,
  "database": "production",
  "username": "admin",
  "password": "secret",
  "collections": ["users", "orders", "products"],
  "output_dir": "./my_backups"
}
```

## Logging

The script creates detailed logs in `mongodb_backup.log` and displays progress in the console. Log levels include:
- INFO: General information and progress
- WARNING: Non-critical issues
- ERROR: Errors that prevent backup completion

## Error Handling

The script includes comprehensive error handling for:
- Connection failures
- Authentication errors
- Collection access issues
- File system errors
- Network timeouts

## Restoring Backups

The BSON files created by this script are compatible with MongoDB's `mongorestore` utility:

```bash
mongorestore --host localhost --port 27017 --db restored_db /path/to/backup/collection1/
```

## Requirements

- Python 3.7+
- pymongo 4.0+
- bson 0.5+
- Network access to MongoDB via VPN

## Troubleshooting

### Connection Issues
- Verify VPN connection is active
- Check MongoDB host and port
- Ensure firewall allows MongoDB connections
- Verify authentication credentials

### Permission Issues
- Ensure write permissions for output directory
- Check MongoDB user permissions for target collections

### Timeout Issues
- Increase timeout values in configuration
- Check network stability
- Consider backing up smaller collections first


