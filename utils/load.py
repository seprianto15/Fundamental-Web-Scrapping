from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine


def save_to_csv(data, filename):
    """Menyimpan data ke file CSV."""
    try:
        data.to_csv(filename, index=False)
    
    except Exception as e:
        print(f"Error saving data to CSV: {type(e).__name__} - {e}")


def save_to_google_sheets(data, spreadsheet_id, sheet_name):
    """Menyimpan data ke Google Sheets."""
    try:
        SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credential)
        values = [data.columns.tolist()] + data.values.tolist()
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_name,
            valueInputOption='RAW',
            body={'values': values}
        ).execute()
    
    except Exception as e:
        print(f"Error saving data to Google Sheets: {type(e).__name__} - {e}")


def save_to_postgres(data, db_url):
    """Menyimpan data ke database PostgreSQL."""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        # Menyimpan data ke tabel 'products', jika tabel sudah ada, data akan ditambahkan
        data.to_sql('products', engine, if_exists='replace', index=False)
    
    except Exception as e:
        print(f"Error saving data to PostgreSQL: {type(e).__name__} - {e}")