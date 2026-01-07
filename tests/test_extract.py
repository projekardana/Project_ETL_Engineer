import pytest
from unittest.mock import Mock, patch
import requests
from bs4 import BeautifulSoup
from utils.extract import fetching_content, extract_fashion_data, scrape_fashion_data

# Test 1: fetching_content Web ketika success
def test_fetching_content_success():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.content = b"<html></html>"

    with patch("utils.extract.requests.get", return_value=mock_response):
        content = fetching_content("https://example.com")
        assert content == b"<html></html>"

# Test 2 : Jika fetching_content Web ketika gagal
def test_fetching_content_fail():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

    with patch("utils.extract.requests.get", return_value=mock_response):
        content = fetching_content("https://example.com")
        assert content is None



# Pengujian ketiga hasil scraping extract data valid

def test_extract_fashion_data_valid_card():
    html = """
    <div class="collection-card">
        <h3>T-shirt Test</h3>
        <div class="price-container">$99.99</div>
        <p>Rating: 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    card = soup.find("div", class_="collection-card")

    result = extract_fashion_data(card)

    assert result["Title"] == "T-shirt Test"
    assert result["Price"] == "$99.99"
    assert result["Rating"] == "Rating: 4.5 / 5"
    assert result["Colors"] == "3 Colors"
    assert result["Size"] == "Size: M"
    assert result["Gender"] == "Gender: Men"


# Pengujian keempat hasil pengujian scraping_data ketika gagal
def test_scrape_fashion_data():
    # buat HTML page
    html_page = """
    <div class="collection-card">
        <h3>T-shirt 1</h3>
        <div class="price-container">$10.00</div>
        <p>Rating: 5 / 5</p>
        <p>2 Colors</p>
        <p>Size: L</p>
        <p>Gender: Unisex</p>
    </div>
    """

    with patch("utils.extract.fetching_content", return_value=html_page.encode()):
        result = scrape_fashion_data("https://example.com/", max_page=1)

    assert len(result) == 1
    assert result[0]["Title"] == "T-shirt 1"
    assert result[0]["Price"] == "$10.00"
