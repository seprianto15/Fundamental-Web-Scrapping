import unittest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import fetching_content, extract_product_data, scrape_product


class TestExtract(unittest.TestCase):

    def setUp(self):
        self.url = 'https://fashion-studio.dicoding.dev/'
        
        self.success_content = b'<html><body>Test</body></html>'
        
        # HTML dummy untuk pengujian extract_product_data (Price di tag span)
        self.html_price_span = """
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$102.15</span>
            <p>Rating: ⭐ 3.9 / 5</p>
            <p>3 Colors</p>
            <p>Size: M, L, XL</p>
            <p>Gender: Unisex</p>
        </div>
        """
        self.soup_price_span = BeautifulSoup(self.html_price_span, 'html.parser')


    def _setup_mock_response(
            self, 
            mock_session, 
            status_code=200, 
            content=b'', 
            error_message=None):
        
        """Helper untuk konfigurasi mock response."""
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.content = content
        
        if error_message:
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(error_message)
        else:
            mock_response.raise_for_status.return_value = None

        mock_session.return_value.get.return_value = mock_response
        return mock_response


# --- Test 1: Fetching Content ---

    @patch('utils.extract.requests.Session')
    def test_fetching_content(self, mock_session):
        """Test fetching_content dengan berbagai kondisi respons HTTP."""
        scenarios = [
            {'code': 200, 'content': self.success_content, 'error': None},
            {'code': 404, 'content': b'', 'error': '404 Not Found'},
            {'code': 500, 'content': b'', 'error': '500 Internal Server Error'},
        ]

        for scenario in scenarios:
            with self.subTest(status=scenario['code']):
                self._setup_mock_response(
                    mock_session, 
                    status_code=scenario['code'], 
                    content=scenario['content'], 
                    error_message=scenario['error']
                )
                
                if scenario['code'] == 200:
                    result = fetching_content(self.url)
                    self.assertEqual(result, scenario['content'])
                else:
                    with self.assertRaises(Exception) as context:
                        fetching_content(self.url)
                    self.assertIn(scenario['error'], str(context.exception))


# --- Test 2: Extract Product Data ---

    def test_extract_product_data_price_in_span(self):
        """Menguji extract_product_data dengan Price ada di tag span."""
        product = self.soup_price_span.find('div', class_='collection-card')
        result = extract_product_data(product)

        expected = {
            'Title': 'Test Product',
            'Price': '$102.15',
            'Rating': 'Rating: ⭐ 3.9 / 5',
            'Colors': '3 Colors',
            'Size': 'Size: M, L, XL',
            'Gender': 'Gender: Unisex'
        }

        self.assertEqual(result, expected)

    
    def test_extract_product_data_price_in_p(self):
        """Menguji extract_product_data dengan Price ada di tag p."""
        # Ganti span menjadi p secara dinamis untuk menguji ekstraksi harga dari tag p
        html_price_p = self.html_price_span.replace(
            '<span class="price">$102.15</span>',
            '<p>Price Unavailable</p>'
        )
        
        soup_price_p = BeautifulSoup(html_price_p, 'html.parser')
        product = soup_price_p.find('div', class_='collection-card')
        
        result = extract_product_data(product)
        self.assertEqual(result['Price'], 'Price Unavailable')


# --- Test 3: Scrape Product (Integration/Flow Test) ---

    @patch('utils.extract.time.sleep', return_value=None)
    @patch('utils.extract.fetching_content')
    def test_scrape_product_full_flow(self, mock_fetch, _):  
        # Setup halaman 1 
        html_page_1 = f"""
        <html>
            <body>
                {self.html_price_span}
                <li class="page-item next"><a href="#">Next</a></li>
            </body>
        </html>
        """.encode('utf-8')

        # Setup halaman terakhir
        html_last_page = f"""
        <html>
            <body>
                {self.html_price_span}
                <li class="page-item disabled">Next</li>
            </body>
        </html>
        """.encode('utf-8')

        # Simulasi scrapping dengan 50 halaman 
        mock_fetch.side_effect = ([html_page_1]*49 + [html_last_page])
    
        # Eksekusi
        base_url = "https://fashion-studio.dicoding.dev/index{}.html"
        result = scrape_product(base_url, start_page=1, delay=0)

        self.assertEqual(len(result), 50)
        self.assertEqual(mock_fetch.call_count, 50)
        self.assertEqual(result[49]['Price'], '$102.15')



if __name__ == '__main__':
    unittest.main()