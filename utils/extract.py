import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang di berikan. """

    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadapat {url}: {e}")
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
        "Gender": gender.text.strip()
    }

    return fashion

def scrape_fashion_data(base_url, start_page=1, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""

    product = []
    page_number = start_page

    while True:
        # khusus halaman pertama
        if page_number == 1:
            url = base_url
        else:
            url = f"{base_url}page/{page_number}"

        print(f"Scrapping Halaman: {url}")

        content = fetching_content(url)
        if not content:
            break

        soup = BeautifulSoup(content, "html.parser")
        cards = soup.find_all('div', class_='collection-card')
        print(f"Jumlah card ditemukan: {len(cards)}")

        if not cards:
            break

        for card in cards:
            fashion = extract_fashion_data(card)
            if fashion:
                product.append(fashion)


        next_button = soup.find('li', class_='page-item next')
        if next_button and next_button.find('a'):
            next_url = next_button.find('a')['href']

            if not next_url.startswith('http'):
                next_url = base_url.rstrip('/') + next_url
            url = next_url
            time.sleep(delay)
        else:
            break # berhenti jika sudah tidak ada next button

    return product