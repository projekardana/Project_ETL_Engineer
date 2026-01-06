import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


load_dotenv()


def load_to_csv(df: pd.DataFrame, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"[INFO] Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan CSV: {e}")

def load_to_postgres(df: pd.DataFrame, table_name: str = "products", if_exists: str = "replace"):
    try:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_url)

        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        print(f"[SUCCESS] Data berhasil disimpan ke PostgreSQL pada tabel '{table_name}'")

    except Exception as e:
        raise RuntimeError(f"[ERROR] Terjadi kesalahan: {e}")

def load_to_google_sheets(df: pd.DataFrame, sheet_name: str = "Sheet1"):
    try:
        credential_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

        if not credential_path or not spreadsheet_id:
            raise ValueError("Environment variables Google Sheets belum lengkap!")

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credential = Credentials.from_service_account_file(credential_path, scopes=scopes)

        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        df_safe = df.copy()
        df_safe = df_safe.astype(str)
        values = df_safe.values.tolist()

        num_rows, num_cols = df_safe.shape
        end_col = chr(ord('A') + num_cols - 1)
        range_name = f"{sheet_name}!A1:{end_col}{num_rows}"

        body = {"values": values}

        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("[SUCCESS] Data berhasil disimpan ke Google Sheets")

    except Exception as e:
        raise RuntimeError(f"[ERROR] Google Sheets API error: {e}")


