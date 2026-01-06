import pandas as pd
from utils.extract import scrape_fashion_data
from utils.transform import transform_data, transform_to_DataFrame
from utils.load import load_to_csv, load_to_postgres, load_to_google_sheets


def main():
    """Fungsi utama untuk keseluruhan proses scrapping hingga menyimoannya."""

    BASE_URL = 'https://fashion-studio.dicoding.dev/'

    all_data = scrape_fashion_data(BASE_URL, max_pages=50, verbose=False)

    if all_data:
        df_transform = transform_to_DataFrame(all_data)
        df = transform_data(df_transform, 16000)
        print(df.head())

        # Menyimpan ke CSV
        load_to_csv(df)

        # Menyimpan ke DBMS Postgres
        load_to_postgres(df, table_name='products')

        # Menyimpan ke Google Sheets API JSON
        load_to_google_sheets(df, sheet_name="Sheet1")

    else:
        print("Tidak Ada Data yang di temukan")


if __name__ == '__main__':
    main()