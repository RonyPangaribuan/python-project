# Web Scraper Berita Indonesia

## Deskripsi

Aplikasi Python untuk mengumpulkan berita dari berbagai sumber online Indonesia. Proyek ini menggunakan web scraping untuk mengambil artikel berita terbaru dan menyimpannya dalam format CSV atau JSON.

## Fitur

- ✅ Scraping berita dari multiple sumber (Detik, Kompas)
- ✅ Export data ke CSV dan JSON
- ✅ Pencarian berita berdasarkan keyword
- ✅ Statistik data yang dikumpulkan
- ✅ Command-line interface yang user-friendly
- ✅ Error handling dan retry mechanism

## Instalasi

1. Clone repository ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Menjalankan

```bash
python main.py
```

## Struktur Data

Setiap artikel berita memiliki struktur:
```json
{
  "title": "Judul berita",
  "description": "Deskripsi atau lead berita", 
  "url": "Link ke artikel lengkap",
  "source": "Sumber berita (e.g., Detik.com)",
  "published_time": "Waktu publikasi",
  "scraped_at": "Waktu scraping",
  "category": "Kategori berita"
}
```

## Contoh Output

### CSV Output
```csv
title,description,url,source,published_time,scraped_at,category
"Berita Terbaru Hari Ini","Deskripsi berita...","https://...","Detik.com","2 jam lalu","2024-01-20T10:30:00","News"
```

### JSON Output
```json
[
  {
    "title": "Berita Terbaru Hari Ini",
    "description": "Deskripsi berita...",
    "url": "https://...",
    "source": "Detik.com",
    "published_time": "2 jam lalu",
    "scraped_at": "2024-01-20T10:30:00",
    "category": "News"
  }
]
```

## Pengembangan Selanjutnya

- [ ] Sentiment analysis untuk artikel
- [ ] Scraping dari lebih banyak sumber
- [ ] Database storage (PostgreSQL/MongoDB)
- [ ] Web dashboard dengan Flask/Django
- [ ] Scheduling otomatis (cron job)
- [ ] API endpoint untuk akses data
- [ ] Real-time notification untuk berita breaking

## Teknologi yang Dipelajari

- Web scraping dengan BeautifulSoup
- HTTP requests dan session management
- Data processing dengan Pandas
- File I/O (CSV, JSON)
- Error handling dan exception management
- Command-line interface development

## Peringatan Legal

⚠️ **Penting**: Selalu hormati robots.txt dan terms of service dari website yang di-scrape. Gunakan delay yang wajar antar request untuk tidak membebani server.

## Contributing

Kontribusi sangat diterima! Silakan:
1. Fork repository ini
2. Buat feature branch
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

## License

MIT License - lihat file LICENSE untuk detail.
