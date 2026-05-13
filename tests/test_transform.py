import unittest
import pandas as pd
from utils.transform import transform_to_Dataframe, transform_data, clean_data

class TestTransform(unittest.TestCase):

    def setUp(self):
        # Sample data untuk testing
        self.sample_data = [
            {
                'Title': 'Product Available',
                'Price': '$100.00',
                'Rating': 'Rating: ⭐ 4.5 / 5',
                'Colors': '3 Colors',
                'Size': 'Size: M',
                'Gender': 'Gender: Unisex'
            },
            {
                'Title': 'Unknown Product', # Akan dihapus di clean_data
                'Price': '$100.00',
                'Rating': '4.5',
                'Colors': '1',
                'Size': 'M',
                'Gender': 'GENDER' # Akan dihapus di clean_data
            }
        ]
        self.exchange_rate = 16000


# --- Test 1: Transform data to DataFrame ---
    # --- Test 1: Transform to DataFrame ---
    def test_transform_to_Dataframe(self):
        """Memastikan konversi list-to-dataframe mempertahankan struktur yang benar."""
        df = transform_to_Dataframe(self.sample_data)
        
        expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender']
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertListEqual(list(df.columns), expected_columns)


# --- Test 2: Transform data ---
    """Validasi pembersihan string, konversi kurs, dan ekstraksi numerik."""
    def test_transform_data(self):
        df = transform_to_Dataframe(self.sample_data)
        transformed_df = transform_data(df, self.exchange_rate)

        # Verifikasi keberadaan kolom hasil transformasi
        for col in ['Price_in_dollars', 'Timestamp']:
            self.assertIn(col, transformed_df.columns)

        # Cek konversi harga
        self.assertEqual(transformed_df.loc[0, 'Price_in_dollars'], 100.00)
        self.assertEqual(transformed_df.loc[0, 'Price'], 100.00 * self.exchange_rate)
        
        # Cek ekstraksi numerik
        self.assertEqual(transformed_df.loc[0, 'Rating'], 4.5)
        self.assertEqual(transformed_df.loc[0, 'Colors'], 3)
        
        # Cek pembersihan string (ubah ke upper case dan penghapusan teks)
        self.assertEqual(transformed_df.loc[0, 'Size'], 'M')
        self.assertEqual(transformed_df.loc[0, 'Gender'], 'UNISEX')
       

# --- Test 3: Clean data ---
    def test_clean_data(self):
        """Validasi penghapusan Unknown Product, kolom gender dengan value 'GENDER', kolom Price dan Price_in_dollars"""
        df_raw = transform_to_Dataframe(self.sample_data)
        df_transformed = transform_data(df_raw, self.exchange_rate)

        cleaned_df = clean_data(df_transformed)

        # Cek penghapusan baris dengan Title "Unknown Product"
        self.assertNotIn("Unknown Product", cleaned_df['Title'].values)

        # Cek penghapusan baris dengan Gender "GENDER"
        self.assertNotIn("GENDER", cleaned_df['Gender'].values)

        # Cek pembersihan kolom
        for col in ['Price_in_dollars']:
            self.assertNotIn(col, cleaned_df.columns)

        # Cek hanya tersisa 1 baris yang valid
        self.assertEqual(len(cleaned_df), 1)
    
    
    def test_clean_data_duplicates(self):
        # Test penghapusan duplikat berdasarkan Title
        data_dup = [
            {
                'Title': 'Product Available',
                'Price': '$100.00',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'L',
                'Gender': 'Unisex'
            },
            {
                'Title': 'Product Available',
                'Price': '$200.00',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex'
            }
        ]
        df_dup = transform_to_Dataframe(data_dup)
        df_transformed_dup = transform_data(df_dup, self.exchange_rate)
        cleaned_df_dup = clean_data(df_transformed_dup)

        # Cek penghapusan duplikat
        self.assertEqual(len(cleaned_df_dup), 1)
    

    def test_clean_data_missing_values(self):
        # Test penghapusan baris dengan nilai yang hilang
        data_missing = [
            {
                'Title': 'Product Available',
                'Price': None,
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'L',
                'Gender': 'Unisex'
            },
            {
                'Title': 'Product Available',
                'Price': '$200.00',
                'Rating': '4.5',
                'Colors': '3',
                'Size': 'M',
                'Gender': 'Unisex'
            }
        ]
        df_missing = transform_to_Dataframe(data_missing)
        df_transformed_missing = transform_data(df_missing, self.exchange_rate)
        cleaned_df_missing = clean_data(df_transformed_missing)

        # Cek penghapusan baris dengan nilai yang hilang
        self.assertEqual(len(cleaned_df_missing), 1)



if __name__ == '__main__':
    unittest.main()