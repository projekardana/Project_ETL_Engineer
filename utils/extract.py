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

def scrape_fashion_data(base_url, max_page=50):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""

    product = []

    for page in range(1, max_page + 1):
        if page == 1:
            url = base_url
        else:
            url = f"{base_url.rstrip('/')}/page{page}"

        print(f"Scrapping Halaman: {url}")

        content = fetching_content(url)
        if not content:
            continue

        soup = BeautifulSoup(content, "html.parser")
        cards = soup.find_all('div', class_='collection-card')

        for card in cards:
            fashion = extract_fashion_data(card)
            if fashion:
                product.append(fashion)

    return product