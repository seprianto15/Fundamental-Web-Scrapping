import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Menambahkan header untuk menghindari blokir oleh server
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' 
        '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )
}


def fetching_content(url):
    """Mengambil konten dari URL yang diberikan."""
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Unexpected error fetching content from {url}: {type(e).__name__} - {e}")


def extract_product_data(collection_card):
    """Mengambil data product berupa : 
    1. title
    2. price 
    3. rating
    4. colors
    5. size
    6. gender 
    dari collection-card (element html)"""
    
    try:
        # title diambil dari h3 dengan class product-title
        title_elements = collection_card.find('h3', class_='product-title')
        title = title_elements.get_text(strip=True) if title_elements else None

        # price diambil dari span dengan class price
        price_elements = collection_card.find('span', class_='price')
        price = price_elements.get_text(strip=True) if price_elements else None

        # jika price tidak ditemukan, akan dicari di tag <p> yang mengandung kata 'Price'
        if not price:
            price_tag = collection_card.find('p', string=lambda t: t and 'Price' in t)
            price = price_tag.get_text(strip=True) if price_tag else None     
            
        # rating diambil dari tag <p> yang mengandung kata 'Rating'
        rating_elements = collection_card.find('p', string=lambda t: t and 'Rating' in t)
        rating = rating_elements.get_text(strip=True) if rating_elements else None

        # colors diambil dari tag <p> yang mengandung kata 'Colors'
        colors_elements = collection_card.find('p', string=lambda t: t and 'Colors' in t)
        colors = colors_elements.get_text(strip=True) if colors_elements else None

        # size diambil dari tag <p> yang mengandung kata 'Size'
        size_elements = collection_card.find('p', string=lambda t: t and 'Size' in t)
        size = size_elements.get_text(strip=True) if size_elements else None

        # gender diambil dari tag <p> yang mengandung kata 'Gender'
        gender_elements = collection_card.find('p', string=lambda t: t and 'Gender' in t)
        gender = gender_elements.get_text(strip=True) if gender_elements else None

        products = {
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender
        }

        return products

    except AttributeError as e:
        print(f'HTML Structure Changed: {e}')

    except Exception as e:
        print(f'Unexpected error extracting product data: {type(e).__name__} - {e}')


def scrape_product(base_url, start_page=1, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []
    page_number = start_page

    try:
        while True:
            if page_number == 1:
                url = "https://fashion-studio.dicoding.dev/index.html"
            else:
                url = base_url.format(page_number)
            print(f"Scraping page: {url}")
        
            content = fetching_content(url)
        
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                collection_elements = soup.find_all('div', class_='collection-card')
                for collection_card in collection_elements:
                    product_data = extract_product_data(collection_card)
                    data.append(product_data)
                
                next_button = soup.find('li', class_='page-item next')
                if next_button:
                    page_number += 1
                    time.sleep(delay)  # Menambahkan delay sebelum halaman berikutnya
                else:
                    break # Berhenti jika tidak ada next button
            else:
                break # Berhenti jika tidak ada kesalahan
    
    except requests.exceptions.RequestException as e:
        print(f'Network error on page {page_number}: {e}')
    
    except Exception as e:
        print(f'Unexpected error while scraping page {page_number}: {type(e).__name__} - {e}')
    
    return data


def collect_product():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}.html'

    try:
        # Menjalankan proses scraping
        all_products_data = scrape_product(BASE_URL)
    
    except KeyboardInterrupt:
        print('Scraping process interrupted by the user. Exiting')

    except Exception as e:
        print(f'Unexpected error in collect_product: {type(e).__name__} - {e}')

    return all_products_data