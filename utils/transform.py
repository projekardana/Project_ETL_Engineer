import pandas as pd
from datetime import datetime

def transform_to_DataFrame(product):
    """
    Mengubah data menjadi DataFrame
    """
    df = pd.DataFrame(product)
    return df

def transform_data(product, exchange_rate):
    try:
        if "timestamp" not in product.columns:
            product["timestamp"] = datetime.now()


        # Drop null dan duplicat
        product = product.dropna()
        product = product.drop_duplicates()

        # Hapus product yang invalid
        product = product[product['Title'] != "Unknown Product"]

        #Transformasi Price ke Rupiah
        product['Price'] = (
            product['Price'].str.replace("$", "", regex=False).astype(float) * exchange_rate
        ).astype(int)

        # Transformasi Rating
        product['Rating'] = (
            product['Rating'].str.extract(r"([\d\.]+)").astype(float)
        )

        # Transformasi Colors
        product["Colors"] = (
            product["Colors"].str.extract(r"(\d+)").astype(int)
        )

        # Transformasi Size
        product["Size"] = product["Size"].str.replace("Size: ", "", regex=False)

        # Transformasi Gender
        product["Gender"] = product["Gender"].str.replace("Gender: ", "", regex=False)

        product["Title"] = product["Title"].astype("string")

        data = product.reset_index(drop=True)
        return data

    except Exception as e:
        print(f"[ERROR] Transformasi Gagal: {e}")

        return pd.DataFrame()