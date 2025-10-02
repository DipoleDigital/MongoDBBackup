#!/usr/bin/env python3
"""
MongoDB Restore Script
=====================

This script restores collections from JSON backups created by mongodb_backup_simple.py

Usage:
    python mongodb_restore.py --host <host> --database <db> --backup-dir <backup_dir>
    python mongodb_restore.py --host <host> --database <db> --backup-dir <backup_dir> --collection <collection_name>
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    from bson import json_util
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please install required packages: pip install pymongo")
    sys.exit(1)


class MongoDBRestore:
    """MongoDB restore utility."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the restore utility with configuration."""
        self.config = config
        self.client: Optional[MongoClient] = None
        self.db = None
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('mongodb_restore.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> bool:
        """Connect to MongoDB database."""
        try:
            connection_string = self.build_connection_string()
            self.logger.info(f"Connecting to MongoDB at {self.config['host']}:{self.config['port']}")
            
            # Connection options
            client_options = {
                'serverSelectionTimeoutMS': 30000,
                'connectTimeoutMS': 10000,
                'socketTimeoutMS': 30000
            }
            
            # Add authentication if provided
            if self.config.get('username') and self.config.get('password'):
                client_options['authSource'] = self.config.get('auth_database', 'admin')
                
            self.client = MongoClient(connection_string, **client_options)
            
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.config['database']]
            
            self.logger.info("Successfully connected to MongoDB")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def build_connection_string(self) -> str:
        """Build MongoDB connection string."""
        host = self.config['host']
        port = self.config['port']
        username = self.config.get('username')
        password = self.config.get('password')
        
        if username and password:
            return f"mongodb://{username}:{password}@{host}:{port}"
        else:
            return f"mongodb://{host}:{port}"
    
    def find_backup_collections(self, backup_dir: Path) -> List[str]:
        """Find all collections in the backup directory."""
        collections = []
        if backup_dir.exists():
            for item in backup_dir.iterdir():
                if item.is_dir():
                    json_file = item / f"{item.name}.json"
                    if json_file.exists():
                        collections.append(item.name)
        return collections
    
    def restore_collection(self, collection_name: str, backup_dir: Path, drop_existing: bool = False) -> bool:
        """Restore a single collection from JSON backup."""
        try:
            collection_dir = backup_dir / collection_name
            json_file = collection_dir / f"{collection_name}.json"
            
            if not json_file.exists():
                self.logger.error(f"Backup file not found: {json_file}")
                return False
            
            collection = self.db[collection_name]
            
            # Drop existing collection if requested
            if drop_existing:
                self.logger.info(f"Dropping existing collection: {collection_name}")
                collection.drop()
            
            # Read and restore documents
            self.logger.info(f"Restoring collection: {collection_name}")
            
            documents = []
            with open(json_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            # Parse MongoDB Extended JSON (preserves ObjectId, Date, etc.)
                            doc = json_util.loads(line)
                            documents.append(doc)
                            
                            # Insert in batches of 1000
                            if len(documents) >= 1000:
                                collection.insert_many(documents)
                                self.logger.info(f"Inserted {len(documents)} documents (line {line_num})")
                                documents = []
                                
                        except json.JSONDecodeError as e:
                            self.logger.error(f"Invalid JSON on line {line_num}: {e}")
                            continue
            
            # Insert remaining documents
            if documents:
                collection.insert_many(documents)
                self.logger.info(f"Inserted final {len(documents)} documents")
            
            # Get final count
            final_count = collection.count_documents({})
            self.logger.info(f"Successfully restored collection '{collection_name}' with {final_count} documents")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore collection '{collection_name}': {e}")
            return False
    
    def restore_collections(self, collections: List[str], backup_dir: Path, drop_existing: bool = False) -> Dict[str, bool]:
        """Restore multiple collections."""
        results = {}
        
        for collection in collections:
            self.logger.info(f"Starting restore of collection: {collection}")
            success = self.restore_collection(collection, backup_dir, drop_existing)
            results[collection] = success
            
            if success:
                self.logger.info(f"✓ Successfully restored: {collection}")
            else:
                self.logger.error(f"✗ Failed to restore: {collection}")
        
        return results
    
    def run_restore(self):
        """Run the complete restore process."""
        # Connect to database
        if not self.connect():
            self.logger.error("Failed to connect to database. Exiting.")
            return False
        
        backup_dir = Path(self.config['backup_dir'])
        if not backup_dir.exists():
            self.logger.error(f"Backup directory not found: {backup_dir}")
            return False
        
        # Get collections to restore
        if 'collection' in self.config and self.config['collection']:
            collections = [self.config['collection']]
        else:
            # Find all collections in backup directory
            available_collections = self.find_backup_collections(backup_dir)
            if not available_collections:
                self.logger.error("No backup collections found in directory")
                return False
            
            print(f"\nAvailable collections in backup directory:")
            for i, collection in enumerate(available_collections, 1):
                print(f"{i}. {collection}")
            
            try:
                selection = input("\nEnter collection numbers to restore (comma-separated, or 'all' for all): ").strip()
                if selection.lower() == 'all':
                    collections = available_collections
                else:
                    indices = [int(x.strip()) - 1 for x in selection.split(',')]
                    collections = [available_collections[i] for i in indices if 0 <= i < len(available_collections)]
            except (ValueError, IndexError) as e:
                self.logger.error(f"Invalid selection: {e}")
                return False
        
        if not collections:
            self.logger.error("No collections selected for restore")
            return False
        
        # Ask about dropping existing collections
        drop_existing = False
        if not self.config.get('force', False):
            response = input("\nDrop existing collections before restore? (y/N): ").strip().lower()
            drop_existing = response in ['y', 'yes']
        
        self.logger.info(f"Starting restore of {len(collections)} collections from {backup_dir}")
        
        # Perform restore
        results = self.restore_collections(collections, backup_dir, drop_existing)
        
        # Report results
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        self.logger.info(f"Restore completed: {successful}/{total} collections restored successfully")
        
        if self.client:
            self.client.close()
        
        return successful == total


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='MongoDB Restore Script')
    parser.add_argument('--host', required=True, help='MongoDB host')
    parser.add_argument('--port', type=int, default=27017, help='MongoDB port (default: 27017)')
    parser.add_argument('--database', '-d', required=True, help='Database name')
    parser.add_argument('--backup-dir', required=True, help='Backup directory path')
    parser.add_argument('--collection', help='Specific collection to restore (optional)')
    parser.add_argument('--username', '-u', help='MongoDB username')
    parser.add_argument('--password', '-p', help='MongoDB password')
    parser.add_argument('--auth-database', default='admin', help='Authentication database')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    # Build configuration
    config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'backup_dir': args.backup_dir,
        'username': args.username,
        'password': args.password,
        'auth_database': args.auth_database,
        'force': args.force
    }
    
    if args.collection:
        config['collection'] = args.collection
    
    # Run restore
    restore = MongoDBRestore(config)
    success = restore.run_restore()
    
    if success:
        print("Restore completed successfully!")
    else:
        print("Restore completed with errors. Check the log file for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

