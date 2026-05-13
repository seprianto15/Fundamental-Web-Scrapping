import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_to_google_sheets, save_to_csv, save_to_postgres


class TestLoad(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame untuk testing
        self.sample_data = pd.DataFrame({
            'Title': ['Product A', 'Product B'],
            'Price_in_dollars': [100.0, 150.0],
            'Price_IDR': [1700000.0, 2550000.0],
            'Rating': [4.5, 4.0],
            'Colors': [3, 2],
            'Size': ['M', 'L'],
            'Gender': ['Unisex', 'Unisex']
        })
        self.db_url = "postgresql://user:pass@localhost:5432/db"

    #--- Test 1: Save to CSV ---
    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        """Validasi pemanggilan method to_csv dengan parameter yang benar."""
        filename = 'test_output.csv'
        save_to_csv(self.sample_data, filename)
        
        mock_to_csv.assert_called_once_with(filename, index=False)

    # --- Test 2: Save to Google Sheets ---
    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets_success(self, mock_from_file, mock_build):
        """Validasi alur integrasi API Google Sheets tanpa koneksi internet."""
        # Arrange
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_creds = MagicMock()
        mock_from_file.return_value = mock_creds
        
        spreadsheet_id = 'test_id'
        sheet_name = 'Sheet1!A1'

        # Act
        save_to_google_sheets(self.sample_data, spreadsheet_id, sheet_name)

        # Assert
        mock_from_file.assert_called_once_with(
            './google-sheets-api.json', 
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_creds)
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    # --- Test 3: Save to PostgreSQL ---
    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_save_to_postgres_success(self, mock_to_sql, mock_create_engine):
        """Memastikan integrasi database PostgreSQL menggunakan SQLAlchemy engine."""
        # Act
        save_to_postgres(self.sample_data, self.db_url)

        # Assert
        mock_create_engine.assert_called_once_with(self.db_url)
        
        # Verifikasi argumen spesifik pada to_sql
        mock_to_sql.assert_called_once()
        args, kwargs = mock_to_sql.call_args
        self.assertEqual(args[0], 'products')
        self.assertEqual(kwargs['if_exists'], 'replace')
        self.assertFalse(kwargs['index'])


if __name__ == '__main__':
    unittest.main()