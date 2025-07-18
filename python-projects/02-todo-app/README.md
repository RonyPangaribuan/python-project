# 📝 To-Do List Manager

## Deskripsi

Aplikasi manajemen tugas (To-Do List) dengan antarmuka grafis menggunakan Tkinter dan database SQLite. Aplikasi ini memungkinkan pengguna untuk menambah, mengedit, menghapus, dan mengelola tugas harian dengan fitur kategorisasi dan prioritas.

## Fitur Utama

- ✅ **CRUD Operations**: Create, Read, Update, Delete tasks
- ✅ **Database SQLite**: Penyimpanan data persisten
- ✅ **Kategorisasi**: Organisir tugas berdasarkan kategori
- ✅ **Sistem Prioritas**: 4 level prioritas (Rendah, Normal, Tinggi, Urgent)
- ✅ **Deadline Management**: Set tanggal deadline untuk tugas
- ✅ **Search & Filter**: Cari dan filter tugas berdasarkan kategori
- ✅ **Status Tracking**: Tandai tugas sebagai selesai/pending
- ✅ **Statistik**: Overview total, selesai, pending, dan overdue tasks
- ✅ **Detail View**: Lihat detail lengkap setiap tugas

## Cara Menjalankan

### Persyaratan
- Python 3.6+
- Tkinter (sudah terinstall dengan Python)
- SQLite3 (sudah terinstall dengan Python)

### Langkah Menjalankan
1. Buka terminal/command prompt
2. Navigate ke folder proyek:
```bash
cd "c:\Users\ASUS\文档\untuk_besok\python-projects\02-todo-app"
```
3. Jalankan aplikasi:
```bash
python main.py
```

## Cara Menggunakan

### 1. Menambah Task Baru
- Isi form di panel kiri:
  - **Judul Task**: Nama tugas (wajib)
  - **Deskripsi**: Detail tugas (opsional)
  - **Kategori**: Pilih dari dropdown (Kerja, Personal, Belajar, Belanja)
  - **Prioritas**: Rendah, Normal, Tinggi, atau Urgent
  - **Deadline**: Format YYYY-MM-DD (opsional)
- Klik "➕ Tambah Task"

### 2. Mengelola Task
- **✅ Selesai**: Tandai task sebagai completed
- **✏️ Edit**: Edit task yang dipilih
- **🗑️ Hapus**: Hapus task permanen
- **👁️ Detail**: Lihat detail lengkap task

### 3. Mencari dan Filter
- **Search Box**: Cari berdasarkan judul atau deskripsi
- **Filter Kategori**: Filter berdasarkan kategori tertentu

### 4. Statistik
Panel bawah menampilkan:
- Total tasks
- Tasks selesai
- Tasks pending  
- Tasks terlambat (overdue)

## Database Structure

### Tabel Tasks
```sql
CREATE TABLE tasks (
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
```

### Tabel Categories
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#3498db'
)
```

## Screenshot Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                    📝 To-Do List Manager                        │
├───────────────────────┬─────────────────────────────────────────┤
│   Tambah Task Baru    │           Daftar Task                   │
│                       │                                         │
│ Judul Task:           │ 🔍 Cari: [____] Kategori: [Semua ▼]    │
│ [________________]    │                                         │
│                       │ ┌─────────────────────────────────────┐ │
│ Deskripsi:            │ │ID│Judul│Kategori│Prioritas│Deadline│  │ │
│ [________________]    │ │1 │Beli│Belanja │Normal   │2024-01 │  │ │
│ [________________]    │ │2 │Code│Kerja   │Tinggi   │-      │  │ │
│ [________________]    │ └─────────────────────────────────────┘ │
│                       │                                         │
│ Kategori: [Kerja ▼]   │ [✅ Selesai][✏️ Edit][🗑️ Hapus][👁️ Detail] │
│ Prioritas: [Normal▼]  │                                         │
│ Deadline: [2024-01-20]│                                         │
│                       │                                         │
│ [➕ Tambah][🗑️ Clear]  │                                         │
└───────────────────────┴─────────────────────────────────────────┤
│ 📊 Total: 15 | ✅ Selesai: 8 | ⏳ Pending: 7 | 🚨 Terlambat: 2  │
└─────────────────────────────────────────────────────────────────┘
```

## Pengembangan Selanjutnya

- [ ] Export tasks ke CSV/PDF
- [ ] Import tasks dari file
- [ ] Reminder notifications
- [ ] Recurring tasks
- [ ] Task dependencies
- [ ] Time tracking
- [ ] Dark mode theme
- [ ] Sync dengan Google Calendar
- [ ] Web interface dengan Flask

## Teknologi yang Dipelajari

- **GUI Programming**: Tkinter widgets dan layout
- **Database**: SQLite operations (CREATE, INSERT, SELECT, UPDATE, DELETE)
- **Event Handling**: Button clicks, keyboard events
- **Data Validation**: Input validation dan error handling
- **OOP**: Class structure dan method organization
- **Date/Time**: Working with datetime dan date objects

## Troubleshooting

### Error "Database locked"
- Pastikan tidak ada instance aplikasi lain yang berjalan
- Restart aplikasi

### Form tidak bisa dikosongkan
- Klik tombol "🗑️ Clear Form"

### Tasks tidak muncul
- Cek apakah ada filter aktif
- Reset search dan kategori filter

## Contributing

Contributions welcome! Silakan:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch  
5. Create Pull Request

## License

MIT License
