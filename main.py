from utils.extract import collect_product
from utils.transform import transform_to_Dataframe, transform_data, clean_data

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
        Dataframe = transform_data(Dataframe, 17000)  # 17000 adalah nilai tukar yang diperlukan
        print(Dataframe.info())
        print(Dataframe.head())
        print("\nData Berhasil Ditranformasi.")

        # Melakukan pembersihan data
        Dataframe = clean_data(Dataframe)
        print(Dataframe.info())
        print(Dataframe.head())
        print("\nData Berhasil Dibersihkan.")
    else:
        print("Tidak ada data yang ditemukan.")

    print("\nWeb Scraping Process Done...")

if __name__ == "__main__":
    main()