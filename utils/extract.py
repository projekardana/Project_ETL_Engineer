import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

timestamp = datetime.now()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang di berikan. """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terdapat {url}: {e}")
        return None


def extract_fashion_data(card):

    title_tag = card.find('h3')
    price_tag = card.find('div', class_='price-container')

    info = card.find_all('p')

    #validasi
    if not title_tag or not price_tag or len(info) < 4:
        return None


    rating = info[0]
    colors = info[1]
    size = info[2]
    gender = info[3]

    fashion = {
        "Title": title_tag.text.strip(),
        "Price": price_tag.text.strip(),
        "Rating": rating.text.strip(),
        "Colors": colors.text.strip(),
        "Size": size.text.strip(),
        "Gender": gender.text.strip(),
        "timestamp": timestamp
    }

    return fashion

def scrape_fashion_data(base_url, max_pages=50, delay=0, verbose=False):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""

    product = []
    url = base_url
    page_count = 1

    while page_count <= max_pages:
        if verbose:
            print(f"Scrapping Halaman {page_count}: {url}")

        content = fetching_content(url)
        if not content:
            break

        soup = BeautifulSoup(content, "html.parser")
        cards = soup.find_all('div', class_='collection-card')
        print(f"Jumlah product ditemukan: {len(cards)}")

        for card in cards:
            fashion = extract_fashion_data(card)
            if fashion:
                product.append(fashion)


        next_button = soup.find('li', class_='page-item next')
        if next_button or not next_button.find('a'):
            break

        next_url = next_button.find('a')["href"]
        if not next_url.startswith('http'):
            url = base_url.rstrip('/') + next_url
        else:
            url = next_url
            time.sleep(delay)

        page_count += 1
        time.sleep(delay)

    return product