import pandas as pd
from utils.extract import scrape_fashion_data


def main():
    """Fungsi utama untuk keseluruhan proses scrapping hingga menyimoannya."""

    BASE_URL = 'https://fashion-studio.dicoding.dev/'

    all_data = scrape_fashion_data(BASE_URL)

    df = pd.DataFrame(all_data)
    print(df)


if __name__ == '__main__':
    main()