import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_postgres, load_to_google_sheets


def test_load_to_csv_success(tmp_path):
    df = pd.DataFrame({
        "Title": ["T-shirt"],
        "Price": [160000]
    })

    file_path = tmp_path / "products.csv"
    load_to_csv(df, filename=str(file_path))

    assert file_path.exists()

@patch("utils.load.create_engine")
def test_load_to_postgres_success(mock_engine):
    df = pd.DataFrame({
        "Title": ["T-shirt"],
        "Price": [160000]
    })

    mock_engine.return_value = MagicMock()

    with patch.object(pd.DataFrame, "to_sql", return_value=None) as mock_to_sql:
        load_to_postgres(df)
        mock_to_sql.assert_called_once()

@patch.dict(os.environ, {}, clear=True)
def test_load_to_google_sheets_env_missing():
    df = pd.DataFrame({"a": [1]})

    with pytest.raises(RuntimeError):
        load_to_google_sheets(df)


@patch("utils.load.build")
@patch("utils.load.Credentials.from_service_account_file")
@patch.dict(os.environ, {
    "GOOGLE_SHEETS_CREDENTIALS_JSON": "dummy.json",
    "GOOGLE_SHEETS_SPREADSHEET_ID": "dummy_id"
})
def test_load_to_google_sheets_success(mock_cred, mock_build):
    df = pd.DataFrame({
        "Title": ["T-shirt"],
        "Price": [160000]
    })

    mock_service = MagicMock()
    mock_sheet = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheet
    mock_sheet.values.return_value.update.return_value.execute.return_value = {}

    mock_build.return_value = mock_service

    load_to_google_sheets(df)

    mock_build.assert_called_once()
    mock_sheet.values.assert_called_once()



