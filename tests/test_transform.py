import pandas as pd
from utils.transform import clean_data

def test_clean_data_price_conversion():
    raw_data = [
        {
            "title": "T-Shirt",
            "price": "$10",
            "rating": "4.5",
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
            "timestamp": "2024-01-01"
        }
    ]

    df = clean_data(raw_data)
    assert df["price"].iloc[0] == 160000


def test_clean_data_remove_invalid_title():
    raw_data = [
        {
            "title": "Unknown Product",
            "price": "$10",
            "rating": "4.5",
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
            "timestamp": "2024-01-01"
        }
    ]

    df = clean_data(raw_data)
    assert df.empty
