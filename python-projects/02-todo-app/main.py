"""
Aplikasi To-Do List dengan Database SQLite
Proyek untuk belajar CRUD operations dan database integration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
import json

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x600")
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
        # Load tasks
        self.load_tasks()
    
    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()
        
        # Create tasks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                priority INTEGER,
                deadline DATE,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#3498db'
            )
        ''')
        
        # Insert default categories
        default_categories = [
            ('Kerja', '#e74c3c'),
            ('Personal', '#2ecc71'),
            ('Belajar', '#9b59b6'),
            ('Belanja', '#f39c12')
        ]
        
        for category, color in default_categories:
            self.cursor.execute(
                'INSERT OR IGNORE INTO categories (name, color) VALUES (?, ?)',
                (category, color)
            )
        
        self.conn.commit()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📝 To-Do List Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Input form
        input_frame = ttk.LabelFrame(main_frame, text="Tambah Task Baru", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Task title
        ttk.Label(input_frame, text="Judul Task:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Description
        ttk.Label(input_frame, text="Deskripsi:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        self.desc_text = tk.Text(input_frame, height=4, width=30)
        self.desc_text.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Category
        ttk.Label(input_frame, text="Kategori:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, width=27)
        self.load_categories()
        self.category_combo.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Priority
        ttk.Label(input_frame, text="Prioritas:").grid(row=6, column=0, sticky=tk.W, pady=(10, 2))
        self.priority_var = tk.StringVar(value="Normal")
