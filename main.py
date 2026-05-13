import os
from dotenv import load_dotenv
from utils.extract import collect_product
from utils.transform import transform_to_Dataframe, transform_data, clean_data
from utils.load import save_to_google_sheets, save_to_csv, save_to_postgres

# Memuat variabel dari .env
load_dotenv()

def main():

    print("Starting Web Scraping Process...")
    
    # --- EXTRACT DATA ---
    all_products_data = collect_product()
    
    # --- LOAD TO DATAFRAME dan TRANSFORM DATA ---
    if all_products_data is not None and len(all_products_data) > 0:
        # Menampilkan jumlah data yang berhasil di extract
        print(f'Berhasil mengambil data dari {len(all_products_data)} product.')
        
        # Mengubah data yang sudah diekstrak menjadi DataFrame
        Dataframe = transform_to_Dataframe(all_products_data)
        print(Dataframe.head())
        print("\nData Berhasil Diubah ke DataFrame.")
        
        # Melakukan transformasi data
        Dataframe_transform = transform_data(Dataframe, 16000)  # 16000 adalah nilai tukar yang diperlukan
        print(Dataframe_transform.info())
        print(Dataframe_transform.head())
        print("\nData Berhasil Ditranformasi.")

        # Melakukan pembersihan data
        Dataframe_clean = clean_data(Dataframe_transform)
        print(Dataframe_clean.info())
        print(Dataframe_clean.head())
        print("\nData Berhasil Dibersihkan.")

        # Menyimpan data ke Google Sheets
        save_to_google_sheets(Dataframe_clean, 
                              spreadsheet_id='1yf3kp5Zf7V5F9TLqXUYJBFHVFXxOiVA0lqx5niqgHuk', 
                              sheet_name='Sheet1!A1')
        print("\nData successfully saved to Google Sheets")
    
        # Menyimpan data ke file CSV
        save_to_csv(Dataframe_clean, 'products.csv')
        print("\nData successfully saved to products.csv")

        # Menyimpan data ke database PostgreSQL
        db_url = os.getenv("DB_URL")
        save_to_postgres(Dataframe_clean, db_url)
        print("\nData successfully saved to PostgreSQL database.")
    else:
        print("Tidak ada data yang ditemukan.")

    print("\nWeb Scraping Process Done...")



if __name__ == "__main__":
    main()