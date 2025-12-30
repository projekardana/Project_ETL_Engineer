from unittest.mock import patch, MagicMock
from utils.extract import fetching_content, extract_fashion_data


@patch("requests.Session.get")
def test_fetching_content_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html></html>"
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    content = fetching_content("http://dummy-url")
    assert content == b"<html></html>"


@patch("requests.Session.get")
def test_fetching_content_failed(mock_get):
    mock_get.side_effect = Exception("Connection error")

    content = fetching_content("http://dummy-url")
    assert content is None


def test_extract_fashion_data():
    html = """
    <div class="collection-card">
        <h3>T-Shirt</h3>
        <div class="price-container">$10</div>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    card = soup.find("div", class_="collection-card")

    data = extract_fashion_data(card)

    assert data["Title"] == "T-Shirt"
    assert data["Price"] == "$10"
    assert data["Colors"] == "3 Colors"
    assert data["Size"] == "Size: M"
    assert data["Gender"] == "Gender: Men"
