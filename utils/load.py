import pandas as pd
from sqlalchemy import create_engine
import gspread
from google.oauth2.service_account import Credentials


def save_to_google_sheets(df, sheet_name="fashion_products", json_file="client_secret.json"):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]

        creds = Credentials.from_service_account_file(json_file, scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open(sheet_name).sheet1
        sheet.clear()
        sheet.append_row(df.columns.tolist())
        for row in df.values.tolist():
            sheet.append_row(row)

        print("Data saved to Google Sheets successfully")

    except Exception as e:
        print(f"Google Sheets load error: {e}")


def save_to_csv(df, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        print("Data saved to CSV successfully")
    except Exception as e:
        print(f"Load error: {e}")

def save_to_postgres(
    df,
    db_name="fashion_db",
    user="postgres",
    password="ardana22",
    host="localhost",
    port="5432",
    table_name="products"
):
    try:
        engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        )

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        print("Data saved to PostgreSQL successfully")

    except Exception as e:
        print(f"PostgreSQL load error: {e}")
