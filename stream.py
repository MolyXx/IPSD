import requests
import pandas as pd
import os

# Konfigurasi API Visual Crossing
API_KEY = 'VGBQCJT36BZT8ZM38J3SNWS9Y'
LOCATION = 'Jakarta,ID'  # Lokasi cuaca yang diinginkan
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
EXCEL_FILE = 'weather_data.xlsx'  # Menyimpan file di Google Colab

# Fungsi untuk mengambil data dari API Visual Crossing
def fetch_weather_data():
    url = f'{BASE_URL}/{LOCATION}?key={API_KEY}&unitGroup=metric&include=fcst'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecasts = data['days']
        return [
            {
                'datetime': forecast['datetime'],
                'temperature': forecast['temp'],
                'humidity': forecast['humidity'],
                'condition': forecast['conditions']
            }
            for forecast in forecasts
        ]
    else:
        print('Gagal mengambil data cuaca.')
        return []

# Fungsi untuk menyimpan data ke file Excel
def save_to_excel(data):
    df = pd.DataFrame(data)
    if os.path.exists(EXCEL_FILE):
        with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            start_row = writer.sheets['Sheet1'].max_row
            df.to_excel(writer, index=False, header=False, startrow=start_row)
    else:
        df.to_excel(EXCEL_FILE, index=False)
    print(f'Data berhasil disimpan ke {EXCEL_FILE}.')

# Fungsi utama untuk streaming data (hanya sekali)
def stream_to_excel():
    weather_data = fetch_weather_data()
    if weather_data:
        save_to_excel(weather_data)
    else:
        print('Tidak ada data baru yang disimpan.')

# Panggil fungsi untuk dijalankan sesuai jadwal oleh scheduler
stream_to_excel()
