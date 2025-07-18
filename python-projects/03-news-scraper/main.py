"""
Simple Web Scraper untuk Berita
Mengumpulkan berita dari berbagai sumber online
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json
import csv
from urllib.parse import urljoin, urlparse

class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.news_data = []
    
    def scrape_detik_news(self, max_articles=10):
        """Scrape berita dari Detik.com"""
        print("🔍 Mengambil berita dari Detik.com...")
        
        try:
            url = "https://news.detik.com/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find news articles (adjust selector as needed)
            articles = soup.find_all('article', class_='list-content__item')[:max_articles]
            
            for article in articles:
                try:
                    # Extract title
                    title_elem = article.find('h2') or article.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else "No title"
                    
                    # Extract link
                    link_elem = title_elem.find('a') if title_elem else None
                    link = link_elem['href'] if link_elem and link_elem.get('href') else ""
                    
                    # Make absolute URL
                    if link and not link.startswith('http'):
                        link = urljoin(url, link)
                    
                    # Extract summary/description
                    desc_elem = article.find('div', class_='media__desc')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Extract time
                    time_elem = article.find('div', class_='media__date')
                    pub_time = time_elem.get_text(strip=True) if time_elem else ""
                    
                    news_item = {
                        'title': title,
                        'description': description,
                        'url': link,
                        'source': 'Detik.com',
                        'published_time': pub_time,
                        'scraped_at': datetime.now().isoformat(),
                        'category': 'News'
                    }
                    
                    self.news_data.append(news_item)
                    print(f"✅ {title[:50]}...")
                    
                except Exception as e:
                    print(f"❌ Error processing article: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error scraping Detik: {e}")
    
    def scrape_kompas_news(self, max_articles=10):
        """Scrape berita dari Kompas.com"""
        print("🔍 Mengambil berita dari Kompas.com...")
        
        try:
            url = "https://www.kompas.com/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find news articles (adjust selector as needed)
            articles = soup.find_all('div', class_='article__list')[:max_articles]
            
            for article in articles:
                try:
                    # Extract title
                    title_elem = article.find('h3') or article.find('h2')
                    title = title_elem.get_text(strip=True) if title_elem else "No title"
                    
                    # Extract link
                    link_elem = article.find('a')
                    link = link_elem['href'] if link_elem and link_elem.get('href') else ""
                    
                    # Make absolute URL
                    if link and not link.startswith('http'):
                        link = urljoin(url, link)
                    
                    # Extract description
                    desc_elem = article.find('div', class_='article__lead')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Extract time
                    time_elem = article.find('div', class_='article__date')
                    pub_time = time_elem.get_text(strip=True) if time_elem else ""
                    
                    news_item = {
                        'title': title,
                        'description': description,
                        'url': link,
                        'source': 'Kompas.com',
                        'published_time': pub_time,
                        'scraped_at': datetime.now().isoformat(),
                        'category': 'News'
                    }
                    
                    self.news_data.append(news_item)
                    print(f"✅ {title[:50]}...")
                    
                except Exception as e:
                    print(f"❌ Error processing article: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error scraping Kompas: {e}")
    
    def scrape_all_sources(self, articles_per_source=5):
        """Scrape dari semua sumber berita"""
        print("🚀 Memulai web scraping berita...")
        print("=" * 50)
        
        # Scrape dari berbagai sumber
        self.scrape_detik_news(articles_per_source)
        time.sleep(2)  # Delay untuk menghormati server
        
        self.scrape_kompas_news(articles_per_source)
        time.sleep(2)
        
        print(f"\n📊 Total artikel berhasil dikumpulkan: {len(self.news_data)}")
    
    def save_to_csv(self, filename=None):
        """Simpan data ke file CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_data_{timestamp}.csv"
        
        if not self.news_data:
            print("❌ Tidak ada data untuk disimpan")
            return
        
        df = pd.DataFrame(self.news_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Data berhasil disimpan ke: {filename}")
        return filename
    
    def save_to_json(self, filename=None):
        """Simpan data ke file JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_data_{timestamp}.json"
        
        if not self.news_data:
            print("❌ Tidak ada data untuk disimpan")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.news_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Data berhasil disimpan ke: {filename}")
        return filename
    
    def get_statistics(self):
        """Tampilkan statistik data yang dikumpulkan"""
        if not self.news_data:
            print("❌ Tidak ada data untuk dianalisis")
            return
        
        df = pd.DataFrame(self.news_data)
        
        print("\n📈 STATISTIK DATA BERITA")
        print("=" * 40)
        print(f"Total artikel: {len(df)}")
        print(f"Sumber berita: {df['source'].nunique()}")
        print("\nArtikel per sumber:")
        print(df['source'].value_counts())
        
        print(f"\nWaktu scraping: {df['scraped_at'].iloc[0] if len(df) > 0 else 'N/A'}")
        
        # Tampilkan sample data
        print(f"\n📄 SAMPLE DATA (5 artikel pertama):")
        print("-" * 40)
        for i, row in df.head().iterrows():
            print(f"{i+1}. {row['title'][:60]}...")
            print(f"   Sumber: {row['source']}")
            print(f"   URL: {row['url']}")
            print()
    
    def search_news(self, keyword):
        """Cari berita berdasarkan keyword"""
        if not self.news_data:
            print("❌ Tidak ada data untuk dicari")
            return []
        
        df = pd.DataFrame(self.news_data)
        
        # Search in title and description
        mask = (df['title'].str.contains(keyword, case=False, na=False) | 
                df['description'].str.contains(keyword, case=False, na=False))
        
        results = df[mask]
        
        print(f"\n🔍 Hasil pencarian untuk '{keyword}': {len(results)} artikel")
        print("-" * 50)
        
        for i, row in results.iterrows():
            print(f"📰 {row['title']}")
            print(f"   {row['description'][:100]}...")
            print(f"   Sumber: {row['source']} | URL: {row['url']}")
            print()
        
        return results.to_dict('records')

def main():
    # Inisialisasi scraper
    scraper = NewsScraper()
    
    print("🤖 News Scraper Indonesia")
    print("=" * 50)
    
    while True:
        print("\nPilihan:")
        print("1. Scrape berita terbaru")
        print("2. Lihat statistik data")
        print("3. Cari berita")
        print("4. Simpan ke CSV")
        print("5. Simpan ke JSON")
        print("6. Keluar")
        
        choice = input("\nPilih opsi (1-6): ").strip()
        
        if choice == '1':
            articles_count = input("Berapa artikel per sumber? (default: 5): ").strip()
            articles_count = int(articles_count) if articles_count.isdigit() else 5
            
            scraper.news_data = []  # Reset data
            scraper.scrape_all_sources(articles_count)
            
        elif choice == '2':
            scraper.get_statistics()
            
        elif choice == '3':
            keyword = input("Masukkan kata kunci pencarian: ").strip()
            if keyword:
                scraper.search_news(keyword)
            
        elif choice == '4':
            scraper.save_to_csv()
            
        elif choice == '5':
            scraper.save_to_json()
            
        elif choice == '6':
            print("👋 Terima kasih!")
            break
            
        else:
            print("❌ Pilihan tidak valid")

if __name__ == "__main__":
    main()
