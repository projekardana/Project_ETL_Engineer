import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data


def sample_raw_data():
    return [
        {
            "Title": "T-shirt",
            "Price": "$10.00",
            "Rating": "Rating: 4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
        }
    ]



# Test transform_to_DataFrame
def test_transform_to_dataframe_success():
    df = transform_to_DataFrame(sample_raw_data())
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1


# Test transform_data (valid)
def test_transform_data_valid():
    df = transform_to_DataFrame(sample_raw_data())
    result = transform_data(df, 16000)

    assert result.loc[0, "Price"] == 160000
    assert result.loc[0, "Rating"] == 4.5
    assert result.loc[0, "Colors"] == 3
    assert result.loc[0, "Size"] == "M"
    assert result.loc[0, "Gender"] == "Men"
    assert result.loc[0, "Title"] == "T-shirt"


# Test invalid title removed
def test_transform_remove_invalid_product():
    data = [
        {
            "Title": "Unknown Product",
            "Price": "$5.00",
            "Rating": "Rating: 3 / 5",
            "Colors": "2 Colors",
            "Size": "Size: S",
            "Gender": "Gender: Women",
        }
    ]

    df = transform_to_DataFrame(data)
    result = transform_data(df, 16000)

    assert result.empty


def test_transform_drop_duplicates():
    data = sample_raw_data() * 2  # duplicate data

    df = transform_to_DataFrame(data)
    result = transform_data(df, 16000)

    assert len(result) == 1



# Test error handling
def test_transform_error_handling():
    # Price tidak bisa di-cast ke float
    data = [
        {
            "Title": "T-shirt",
            "Price": "INVALID",
            "Rating": "Rating: 4 / 5",
            "Colors": "2 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
        }
    ]

    df = transform_to_DataFrame(data)
    result = transform_data(df, 16000)
    assert result.empty

def test_transform_add_timestamp():
    df = transform_to_DataFrame([
        {
            "Title": "T-Shirt",
            "Price": "$10.00",
            "Rating": "Rating: 4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men"
        }
    ])

    result = transform_data(df, 16000)
    assert "timestamp" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])