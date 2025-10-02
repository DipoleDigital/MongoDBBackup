#!/usr/bin/env python3
"""
MongoDB Backup GUI Application
=============================

A GUI application for MongoDB backup with VPN support.
Preserves MongoDB data types using Extended JSON format.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    from bson import json_util
except ImportError as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Missing Dependencies", f"Missing required dependencies: {e}\nPlease install: pip install pymongo")
    root.destroy()
    exit(1)


class MongoDBBackupGUI:
    """MongoDB Backup GUI Application."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("MongoDB Backup Tool")
        self.root.geometry("900x850")
        self.root.resizable(True, True)
        
        # Center the window on screen
        self.center_window()
        
        # Variables
        self.client = None
        self.db = None
        self.collections = []
        self.collection_vars = {}
        self.backup_thread = None
        
        # Setup logging
        self.setup_logging()
        
        # Create GUI
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_logging(self):
        """Setup logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mongodb_backup_gui.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="MongoDB Backup Tool", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Connection Section
        self.create_connection_section(main_frame, row=1)
        
        # Collections Section
        self.create_collections_section(main_frame, row=2)
        
        # Backup Section
        self.create_backup_section(main_frame, row=3)
        
        # Log Section
        self.create_log_section(main_frame, row=4)
        
    def create_connection_section(self, parent, row):
        """Create the connection section."""
        # Connection frame
        conn_frame = ttk.LabelFrame(parent, text="Database Connection", padding="10")
        conn_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        conn_frame.columnconfigure(1, weight=1)
        
        # IP Address
        ttk.Label(conn_frame, text="VPN IP Address:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.ip_var = tk.StringVar(value="")
        self.ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var, width=20)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Port
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.port_var = tk.StringVar(value="27017")
        self.port_entry = ttk.Entry(conn_frame, textvariable=self.port_var, width=8)
        self.port_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Database
        ttk.Label(conn_frame, text="Database:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.db_var = tk.StringVar(value="PDV")
        self.db_entry = ttk.Entry(conn_frame, textvariable=self.db_var, width=20)
        self.db_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # Test Connection Button
        self.test_btn = ttk.Button(conn_frame, text="Test Connection", command=self.test_connection)
        self.test_btn.grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Connection Status
        self.status_var = tk.StringVar(value="Not connected")
        self.status_label = ttk.Label(conn_frame, textvariable=self.status_var, foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(10, 0))
        
    def create_collections_section(self, parent, row):
        """Create the collections selection section."""
        # Collections frame
        collections_frame = ttk.LabelFrame(parent, text="Collections Selection", padding="10")
        collections_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        collections_frame.columnconfigure(0, weight=1)
        collections_frame.rowconfigure(1, weight=1)
        
        # Select All/None buttons
        buttons_frame = ttk.Frame(collections_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Select All", command=self.select_all_collections).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Select None", command=self.select_none_collections).pack(side=tk.LEFT)
        
        # Collections listbox with scrollbar
        list_frame = ttk.Frame(collections_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for collections with checkboxes
        columns = ('select', 'collection', 'count')
        self.collections_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.collections_tree.heading('select', text='✓')
        self.collections_tree.heading('collection', text='Collection Name')
        self.collections_tree.heading('count', text='Documents')
        
        self.collections_tree.column('select', width=50, anchor='center')
        self.collections_tree.column('collection', width=300, anchor='w')
        self.collections_tree.column('count', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.collections_tree.yview)
        self.collections_tree.configure(yscrollcommand=scrollbar.set)
        
        self.collections_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click to toggle selection
        self.collections_tree.bind('<Double-1>', self.toggle_collection_selection)
        
    def create_backup_section(self, parent, row):
        """Create the backup section."""
        # Backup frame
        backup_frame = ttk.LabelFrame(parent, text="Backup Operations", padding="10")
        backup_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        backup_frame.columnconfigure(0, weight=1)
        
        # Output directory
        ttk.Label(backup_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Directory selection frame
        dir_frame = ttk.Frame(backup_frame)
        dir_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar(value="./backups")
        self.output_entry = ttk.Entry(dir_frame, textvariable=self.output_var)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        self.browse_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        self.browse_btn.grid(row=0, column=1, sticky=tk.W)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(backup_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress label
        self.progress_label = ttk.Label(backup_frame, text="Ready to backup")
        self.progress_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        # Backup button
        self.backup_btn = ttk.Button(backup_frame, text="Start Backup", command=self.start_backup, state='disabled')
        self.backup_btn.grid(row=4, column=0, sticky=tk.W)
        
    def create_log_section(self, parent, row):
        """Create the log section."""
        # Log frame
        log_frame = ttk.LabelFrame(parent, text="Log Output", padding="10")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_directory(self):
        """Open directory browser to select backup location."""
        directory = filedialog.askdirectory(
            title="Select Backup Directory",
            initialdir=self.output_var.get() if self.output_var.get() else "."
        )
        if directory:
            self.output_var.set(directory)
            self.log_message(f"Selected backup directory: {directory}")
        
    def test_connection(self):
        """Test the database connection."""
        def test_thread():
            try:
                self.log_message("Testing connection...")
                self.test_btn.config(state='disabled')
                
                host = self.ip_var.get().strip()
                port_str = self.port_var.get().strip()
                database = self.db_var.get().strip()
                
                if not host or not database:
                    self.root.after(0, lambda: self.log_message("Please enter IP address and database name"))
                    return
                
                # Validate port
                try:
                    port = int(port_str)
                except ValueError:
                    self.root.after(0, lambda: self.log_message("Invalid port number"))
                    return
                
                self.log_message(f"Connecting to {host}:{port}...")
                
                # Create connection with better error handling
                connection_string = f"mongodb://{host}:{port}"
                client = MongoClient(
                    connection_string, 
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000
                )
                
                self.log_message("Testing ping...")
                # Test connection
                client.admin.command('ping')
                
                self.log_message(f"Accessing database '{database}'...")
                db = client[database]
                
                self.log_message("Getting collections...")
                # Get collections
                collections = db.list_collection_names()
                
                if not collections:
                    self.root.after(0, lambda: self.log_message("No collections found in database"))
                    return
                
                self.log_message(f"Found {len(collections)} collections")
                
                # Update UI
                self.root.after(0, lambda: self.connection_success(client, db, collections))
                
            except ConnectionFailure as e:
                self.root.after(0, lambda: self.connection_failed(f"Connection failed: {e}"))
            except ServerSelectionTimeoutError as e:
                self.root.after(0, lambda: self.connection_failed(f"Server timeout: {e}"))
            except Exception as e:
                self.root.after(0, lambda: self.connection_failed(f"Unexpected error: {e}"))
            finally:
                self.root.after(0, lambda: self.test_btn.config(state='normal'))
        
        # Run in separate thread
        threading.Thread(target=test_thread, daemon=True).start()
        
    def connection_success(self, client, db, collections):
        """Handle successful connection."""
        self.client = client
        self.db = db
        self.collections = collections
        
        self.status_var.set(f"Connected - {len(collections)} collections found")
        self.status_label.config(foreground="green")
        
        # Populate collections list
        self.populate_collections()
        
        # Enable backup button
        self.backup_btn.config(state='normal')
        
        self.log_message(f"Connected successfully! Found {len(collections)} collections")
        
    def connection_failed(self, error):
        """Handle failed connection."""
        self.status_var.set("Connection failed")
        self.status_label.config(foreground="red")
        self.log_message(f"Connection failed: {error}")
        
    def populate_collections(self):
        """Populate the collections list."""
        # Clear existing items
        for item in self.collections_tree.get_children():
            self.collections_tree.delete(item)
        
        # Add collections
        for collection in self.collections:
            try:
                # Use a longer timeout for counting documents
                count = self.db[collection].count_documents({}, maxTimeMS=30000)
                item_id = self.collections_tree.insert('', 'end', values=('☐', collection, count))
                self.collection_vars[collection] = False  # Unchecked by default
            except Exception as e:
                self.log_message(f"Error getting count for {collection}: {e}")
                item_id = self.collections_tree.insert('', 'end', values=('☐', collection, 'Error'))
                self.collection_vars[collection] = False
        
        # Select all by default
        self.select_all_collections()
        
    def toggle_collection_selection(self, event):
        """Toggle collection selection on double-click."""
        item = self.collections_tree.selection()[0]
        collection = self.collections_tree.item(item, 'values')[1]
        
        # Toggle selection
        self.collection_vars[collection] = not self.collection_vars[collection]
        
        # Update display
        status = '☑' if self.collection_vars[collection] else '☐'
        self.collections_tree.item(item, values=(status, collection, self.collections_tree.item(item, 'values')[2]))
        
    def select_all_collections(self):
        """Select all collections."""
        for item in self.collections_tree.get_children():
            collection = self.collections_tree.item(item, 'values')[1]
            self.collection_vars[collection] = True
            self.collections_tree.item(item, values=('☑', collection, self.collections_tree.item(item, 'values')[2]))
        
    def select_none_collections(self):
        """Select no collections."""
        for item in self.collections_tree.get_children():
            collection = self.collections_tree.item(item, 'values')[1]
            self.collection_vars[collection] = False
            self.collections_tree.item(item, values=('☐', collection, self.collections_tree.item(item, 'values')[2]))
        
    def start_backup(self):
        """Start the backup process."""
        if self.client is None or self.db is None:
            messagebox.showerror("Error", "Please test connection first")
            return
        
        # Get selected collections
        selected_collections = [col for col, selected in self.collection_vars.items() if selected]
        
        if not selected_collections:
            messagebox.showwarning("Warning", "Please select at least one collection to backup")
            return
        
        # Confirm backup
        result = messagebox.askyesno(
            "Confirm Backup",
            f"Backup {len(selected_collections)} collections?\n\n"
            f"Selected: {', '.join(selected_collections[:5])}{'...' if len(selected_collections) > 5 else ''}"
        )
        
        if not result:
            return
        
        # Start backup in separate thread
        self.backup_thread = threading.Thread(target=self.run_backup, args=(selected_collections,), daemon=True)
        self.backup_thread.start()
        
    def run_backup(self, collections):
        """Run the backup process."""
        try:
            self.root.after(0, lambda: self.backup_btn.config(state='disabled', text='Backing up...'))
            self.root.after(0, lambda: self.progress_var.set(0))
            self.root.after(0, lambda: self.progress_label.config(text="Starting backup..."))
            
            # Create output directory with IP to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ip_clean = self.ip_var.get().replace(".", "_").replace(":", "_")
            output_dir = Path(self.output_var.get()) / f"{self.db_var.get()}_{ip_clean}_{timestamp}"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            total_collections = len(collections)
            successful = 0
            
            for i, collection_name in enumerate(collections):
                try:
                    self.root.after(0, lambda c=collection_name: self.log_message(f"Backing up {c}..."))
                    
                    # Create collection directory
                    collection_dir = output_dir / collection_name
                    collection_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Get collection
                    collection = self.db[collection_name]
                    count = collection.count_documents({})
                    
                    if count == 0:
                        self.root.after(0, lambda c=collection_name: self.log_message(f"Collection {c} is empty, skipping"))
                        continue
                    
                    # Export to Extended JSON
                    json_file = collection_dir / f"{collection_name}.json"
                    with open(json_file, 'w', encoding='utf-8') as f:
                        cursor = collection.find({})
                        for doc in cursor:
                            doc_str = json_util.dumps(doc, ensure_ascii=False)
                            f.write(doc_str + '\n')
                    
                    # Create metadata
                    metadata = {
                        'collection': collection_name,
                        'database': self.db_var.get(),
                        'document_count': count,
                        'backup_timestamp': datetime.now().isoformat(),
                        'json_file': f"{collection_name}.json",
                        'format': 'MongoDB Extended JSON'
                    }
                    
                    metadata_file = collection_dir / "metadata.json"
                    with open(metadata_file, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    successful += 1
                    self.root.after(0, lambda c=collection_name: self.log_message(f"Successfully backed up {c}"))
                    
                except Exception as e:
                    self.root.after(0, lambda c=collection_name, e=str(e): self.log_message(f"Failed to backup {c}: {e}"))
                
                # Update progress
                progress = ((i + 1) / total_collections) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda p=progress, s=successful, t=total_collections: 
                               self.progress_label.config(text=f"Progress: {s}/{t} collections ({p:.1f}%)"))
            
            # Create summary
            summary = {
                'backup_timestamp': datetime.now().isoformat(),
                'database': self.db_var.get(),
                'host': self.ip_var.get(),
                'port': self.port_var.get(),
                'collections_backed_up': successful,
                'total_collections': total_collections,
                'successful_backups': [c for c in collections if c in [item for item in collections]],
                'output_directory': str(output_dir),
                'format': 'MongoDB Extended JSON'
            }
            
            summary_file = output_dir / "backup_summary.json"
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            # Final update
            self.root.after(0, lambda: self.backup_completed(successful, total_collections, output_dir))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Backup failed: {e}"))
            self.root.after(0, lambda: self.backup_btn.config(state='normal', text='Start Backup'))
            
    def backup_completed(self, successful, total, output_dir):
        """Handle backup completion."""
        self.progress_var.set(100)
        self.progress_label.config(text=f"Completed: {successful}/{total} collections backed up")
        self.backup_btn.config(state='normal', text='Start Backup')
        
        self.log_message(f"Backup completed! {successful}/{total} collections backed up successfully")
        self.log_message(f"Backup saved to: {output_dir}")
        
        messagebox.showinfo(
            "Backup Completed",
            f"Backup completed successfully!\n\n"
            f"Collections backed up: {successful}/{total}\n"
            f"Location: {output_dir}"
        )
        
    def log_message(self, message):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Also log to file
        self.logger.info(message)
        
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main function."""
    app = MongoDBBackupGUI()
    app.run()


if __name__ == "__main__":
    main()
