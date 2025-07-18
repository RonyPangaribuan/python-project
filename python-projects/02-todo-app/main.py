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
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                     values=["Rendah", "Normal", "Tinggi", "Urgent"], width=27)
        priority_combo.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Deadline
        ttk.Label(input_frame, text="Deadline (opsional):").grid(row=8, column=0, sticky=tk.W, pady=(10, 2))
        self.deadline_var = tk.StringVar()
        deadline_entry = ttk.Entry(input_frame, textvariable=self.deadline_var, width=30)
        deadline_entry.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(input_frame, text="Format: YYYY-MM-DD", font=("Arial", 8)).grid(row=10, column=0, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=11, column=0, pady=20, sticky=(tk.W, tk.E))
        
        add_btn = ttk.Button(button_frame, text="➕ Tambah Task", command=self.add_task)
        add_btn.grid(row=0, column=0, padx=(0, 5))
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear Form", command=self.clear_form)
        clear_btn.grid(row=0, column=1)
        
        # Right panel - Task list
        list_frame = ttk.LabelFrame(main_frame, text="Daftar Task", padding="10")
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Cari:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.filter_tasks)
        
        # Filter by category
        ttk.Label(search_frame, text="Kategori:").grid(row=0, column=2, padx=(10, 5))
        self.filter_category_var = tk.StringVar(value="Semua")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_category_var, width=15)
        filter_combo.grid(row=0, column=3)
        filter_combo.bind('<<ComboboxSelected>>', self.filter_tasks)
        
        # Task treeview
        columns = ('ID', 'Title', 'Category', 'Priority', 'Deadline', 'Status')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Column headings
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Title', text='Judul Task')
        self.task_tree.heading('Category', text='Kategori')
        self.task_tree.heading('Priority', text='Prioritas')
        self.task_tree.heading('Deadline', text='Deadline')
        self.task_tree.heading('Status', text='Status')
        
        # Column widths
        self.task_tree.column('ID', width=50)
        self.task_tree.column('Title', width=200)
        self.task_tree.column('Category', width=100)
        self.task_tree.column('Priority', width=80)
        self.task_tree.column('Deadline', width=100)
        self.task_tree.column('Status', width=80)
        
        self.task_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), columnspan=4)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=1, column=4, sticky=(tk.N, tk.S))
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Task action buttons
        action_frame = ttk.Frame(list_frame)
        action_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        complete_btn = ttk.Button(action_frame, text="✅ Selesai", command=self.mark_completed)
        complete_btn.grid(row=0, column=0, padx=5)
        
        edit_btn = ttk.Button(action_frame, text="✏️ Edit", command=self.edit_task)
        edit_btn.grid(row=0, column=1, padx=5)
        
        delete_btn = ttk.Button(action_frame, text="🗑️ Hapus", command=self.delete_task)
        delete_btn.grid(row=0, column=2, padx=5)
        
        view_btn = ttk.Button(action_frame, text="👁️ Detail", command=self.view_task_detail)
        view_btn.grid(row=0, column=3, padx=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistik", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.grid(row=0, column=0)
    
    def load_categories(self):
        """Load categories from database"""
        self.cursor.execute('SELECT name FROM categories ORDER BY name')
        categories = [row[0] for row in self.cursor.fetchall()]
        self.category_combo['values'] = categories
        
        # Also update filter combo
        if hasattr(self, 'filter_category_var'):
            filter_combo = None
            for widget in self.root.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and child.cget('text') == 'Daftar Task':
                        for subchild in child.winfo_children():
                            if isinstance(subchild, ttk.Frame):
                                for item in subchild.winfo_children():
                                    if isinstance(item, ttk.Combobox) and item.cget('width') == 15:
                                        item['values'] = ['Semua'] + categories
                                        break
    
    def add_task(self):
        """Add new task to database"""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Judul task tidak boleh kosong!")
            return
        
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        deadline = self.deadline_var.get().strip()
        
        # Convert priority to number
        priority_map = {"Rendah": 1, "Normal": 2, "Tinggi": 3, "Urgent": 4}
        priority_num = priority_map.get(priority, 2)
        
        # Validate deadline
        deadline_date = None
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Format tanggal tidak valid! Gunakan YYYY-MM-DD")
                return
        
        try:
            self.cursor.execute('''
                INSERT INTO tasks (title, description, category, priority, deadline)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, description, category, priority_num, deadline_date))
            
            self.conn.commit()
            messagebox.showinfo("Sukses", "Task berhasil ditambahkan!")
            self.clear_form()
            self.load_tasks()
            self.update_statistics()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah task: {e}")
    
    def clear_form(self):
        """Clear input form"""
        self.title_var.set("")
        self.desc_text.delete("1.0", tk.END)
        self.category_var.set("")
        self.priority_var.set("Normal")
        self.deadline_var.set("")
    
    def load_tasks(self):
        """Load tasks from database to treeview"""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Load tasks
        self.cursor.execute('''
            SELECT id, title, category, priority, deadline, completed
            FROM tasks
            ORDER BY completed ASC, priority DESC, created_at DESC
        ''')
        
        priority_map = {1: "Rendah", 2: "Normal", 3: "Tinggi", 4: "Urgent"}
        
        for row in self.cursor.fetchall():
            task_id, title, category, priority, deadline, completed = row
            
            priority_text = priority_map.get(priority, "Normal")
            status = "✅ Selesai" if completed else "⏳ Pending"
            deadline_text = deadline if deadline else "-"
            
            # Insert into treeview
            item = self.task_tree.insert('', 'end', values=(
                task_id, title, category, priority_text, deadline_text, status
            ))
            
            # Color coding for completed tasks
            if completed:
                self.task_tree.set(item, 'Title', f"✅ {title}")
    
    def filter_tasks(self, event=None):
        """Filter tasks based on search and category"""
        search_term = self.search_var.get().lower()
        category_filter = self.filter_category_var.get()
        
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Build query
        query = '''
            SELECT id, title, category, priority, deadline, completed
            FROM tasks
            WHERE 1=1
        '''
        params = []
        
        if search_term:
            query += ' AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)'
            params.extend([f'%{search_term}%', f'%{search_term}%'])
        
        if category_filter and category_filter != 'Semua':
            query += ' AND category = ?'
            params.append(category_filter)
        
        query += ' ORDER BY completed ASC, priority DESC, created_at DESC'
        
        self.cursor.execute(query, params)
        
        priority_map = {1: "Rendah", 2: "Normal", 3: "Tinggi", 4: "Urgent"}
        
        for row in self.cursor.fetchall():
            task_id, title, category, priority, deadline, completed = row
            
            priority_text = priority_map.get(priority, "Normal")
            status = "✅ Selesai" if completed else "⏳ Pending"
            deadline_text = deadline if deadline else "-"
            
            item = self.task_tree.insert('', 'end', values=(
                task_id, title, category, priority_text, deadline_text, status
            ))
            
            if completed:
                self.task_tree.set(item, 'Title', f"✅ {title}")
    
    def mark_completed(self):
        """Mark selected task as completed"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Pilih task yang ingin diselesaikan!")
            return
        
        item = selection[0]
        task_id = self.task_tree.item(item, 'values')[0]
        
        try:
            self.cursor.execute(
                'UPDATE tasks SET completed = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (task_id,)
            )
            self.conn.commit()
            messagebox.showinfo("Sukses", "Task berhasil diselesaikan!")
            self.load_tasks()
            self.update_statistics()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyelesaikan task: {e}")
    
    def edit_task(self):
        """Edit selected task"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Pilih task yang ingin diedit!")
            return
        
        item = selection[0]
        task_id = self.task_tree.item(item, 'values')[0]
        
        # Get task details
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = self.cursor.fetchone()
        
        if task:
            # Fill form with current data
            self.title_var.set(task[1])  # title
            self.desc_text.delete("1.0", tk.END)
            self.desc_text.insert("1.0", task[2] or "")  # description
            self.category_var.set(task[3] or "")  # category
            
            priority_map = {1: "Rendah", 2: "Normal", 3: "Tinggi", 4: "Urgent"}
            self.priority_var.set(priority_map.get(task[4], "Normal"))
            
            self.deadline_var.set(task[5] or "")  # deadline
            
            messagebox.showinfo("Info", "Data task telah dimuat ke form. Edit dan klik 'Tambah Task' untuk menyimpan perubahan.")
    
    def delete_task(self):
        """Delete selected task"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Pilih task yang ingin dihapus!")
            return
        
        item = selection[0]
        task_id = self.task_tree.item(item, 'values')[0]
        task_title = self.task_tree.item(item, 'values')[1]
        
        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus task '{task_title}'?"):
            try:
                self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                self.conn.commit()
                messagebox.showinfo("Sukses", "Task berhasil dihapus!")
                self.load_tasks()
                self.update_statistics()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus task: {e}")
    
    def view_task_detail(self):
        """View detailed task information"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Pilih task yang ingin dilihat detailnya!")
            return
        
        item = selection[0]
        task_id = self.task_tree.item(item, 'values')[0]
        
        # Get task details
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = self.cursor.fetchone()
        
        if task:
            detail_window = tk.Toplevel(self.root)
            detail_window.title("Detail Task")
            detail_window.geometry("400x300")
            
            # Task details
            details = f"""
ID: {task[0]}
Judul: {task[1]}
Deskripsi: {task[2] or 'Tidak ada deskripsi'}
Kategori: {task[3] or 'Tidak ada kategori'}
Prioritas: {['', 'Rendah', 'Normal', 'Tinggi', 'Urgent'][task[4]]}
Deadline: {task[5] or 'Tidak ada deadline'}
Status: {'Selesai' if task[6] else 'Pending'}
Dibuat: {task[7]}
Diupdate: {task[8]}
            """
            
            text_widget = tk.Text(detail_window, wrap=tk.WORD, padx=10, pady=10)
            text_widget.insert("1.0", details.strip())
            text_widget.config(state="disabled")
            text_widget.pack(fill=tk.BOTH, expand=True)
    
    def update_statistics(self):
        """Update statistics display"""
        # Get task counts
        self.cursor.execute('SELECT COUNT(*) FROM tasks')
        total_tasks = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = 1')
        completed_tasks = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = 0')
        pending_tasks = self.cursor.fetchone()[0]
        
        # Get overdue tasks
        today = date.today()
        self.cursor.execute(
            'SELECT COUNT(*) FROM tasks WHERE deadline < ? AND completed = 0',
            (today,)
        )
        overdue_tasks = self.cursor.fetchone()[0]
        
        stats_text = f"""📊 Total: {total_tasks} | ✅ Selesai: {completed_tasks} | ⏳ Pending: {pending_tasks} | 🚨 Terlambat: {overdue_tasks}"""
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
