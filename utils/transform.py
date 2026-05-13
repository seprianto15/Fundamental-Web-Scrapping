import pandas as pd

def transform_to_Dataframe(data):
    """Mengubah data yang sudah diekstrak menjadi DataFrame."""
    try:
        df = pd.DataFrame(data)

        return df
    
    except ValueError as e:
        raise ValueError(f'Error dalam mengubah data ke DataFrame: {e}')
    
    except Exception as e:
        raise Exception(f'Unexpected error in transform_to_Dataframe: {type(e).__name__} - {e}')
    

def transform_data(data, exchange_rate):

    """Membersihkan dan mengubah data sesuai kebutuhan"""
    try:
        # Transformasi Price
        if 'Price' in data.columns:
            # Menghapus simbol mata uang dan koma
            clean_price = data['Price'].str.replace(r'[^\d.]', '', regex=True)
            # Mengubah ke numerik, jika ada nilai yang tidak bisa diubah, akan menjadi NaN
            data['Price_in_dollars'] = pd.to_numeric(clean_price, errors='coerce')
            # Transformasi ke Rupiah
            data['Price'] = data['Price_in_dollars'] * float(exchange_rate)
    
        # Transformasi Rating
        if 'Rating' in data.columns:
            # Menghapus teks 'Rating:' jika ada
            clean_rating = data['Rating'].str.extract(r'(\d+(\.\d+)?)')[0]
            # Mengubah ke numerik, jika ada nilai yang tidak bisa diubah, akan menjadi NaN
            data['Rating'] = pd.to_numeric(clean_rating, errors='coerce')
    
        # Transformasi Colors
        if 'Colors' in data.columns:
            # Menghapus teks 'Colors:' jika ada
            clean_colors = data['Colors'].str.extract(r'(\d+)')[0]
            # Mengubah ke numerik, jika ada nilai yang tidak bisa diubah, akan menjadi NaN
            data['Colors'] = pd.to_numeric(clean_colors, errors='coerce').fillna(0).astype(int)

        # Transformasi Size
        if 'Size' in data.columns:
            # Menghapus teks 'Size:' dan spasi jika ada
            data['Size'] = data['Size'].str.replace(r'Size:\s*', '', regex=True).str.strip().str.upper()

        # Transformasi Gender
        if 'Gender' in data.columns:
            data['Gender'] = data['Gender'].str.replace(r'Gender:\s*', '', regex=True).str.strip().str.upper()

        # Menambahkan Timestamp
        data['Timestamp'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

        return data

    except KeyError as e:
        raise KeyError(f'Kolom yang diperlukan tidak ditemukan: {e}')    
    
    except ValueError as e:
        raise ValueError(f'Error dalam mengubah tipe data: {e}')
    
    except TypeError as e:
        raise TypeError(f'Error dalam memproses data: {e}')
    
    except Exception as e:
        raise Exception(f'Unexpected error transforming data: {type(e).__name__} - {e}')
    

def clean_data(data):
    """Membersihkan data dari nilai yang tidak valid atau duplikat."""
    try:
        # Menghapus baris dengan nilai yang hilang pada kolom
        data = data.dropna()
    
        # Menghapus baris jika Title berisi "Unknown Product"
        data = data[data['Title'] != "Unknown Product"]

        # Menghapus baris jika Gender berisi nilai "Gender"
        data = data[data['Gender'] != "GENDER"]

        # Menghapus kolom Price_in_dollars dan Price
        data = data.drop(columns='Price_in_dollars', errors='ignore')

        # Menghapus duplikat berdasarkan Title
        data = data.drop_duplicates(subset=['Title'])
    
        return data

    except KeyError as e:
        raise KeyError(f"Structural Error: Column {e} not found during the cleaning process.")
    
    except Exception as e:
        raise Exception(f"Unexpected Error clean_data: {e}")

    

