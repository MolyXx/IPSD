import requests
import pandas as pd
import os
import subprocess

# Konfigurasi API Visual Crossing
API_KEY = 'VGBQCJT36BZT8ZM38J3SNWS9Y'
LOCATION = 'Jakarta,ID'  # Lokasi cuaca yang diinginkan
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
CSV_FILE = 'weather_data.csv'

# Fungsi untuk mengambil semua data dari API Visual Crossing
def fetch_weather_data():
    url = f'{BASE_URL}/{LOCATION}?key={API_KEY}&unitGroup=metric&include=fcst'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecasts = data['days']
        # Mengembalikan semua data dalam setiap entri
        return forecasts
    else:
        print('Gagal mengambil data cuaca.')
        return []

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(data):
    df = pd.DataFrame(data)

    # Jika file CSV sudah ada, tambahkan data tanpa header
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
    else:
        # Jika file belum ada, buat file baru dengan header
        df.to_csv(CSV_FILE, index=False)

    print(f'Data berhasil disimpan ke {CSV_FILE}.')

# Fungsi untuk melakukan commit ke GitHub
def commit_to_github():
    try:
        subprocess.run(['git', 'add', CSV_FILE], check=True)
        subprocess.run(['git', 'commit', '-m', 'Update weather data'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print('Data berhasil di-commit dan di-push ke GitHub.')
    except subprocess.CalledProcessError as e:
        print(f'Gagal melakukan commit ke GitHub: {e}')

# Fungsi utama untuk streaming data
def stream_to_csv():
    weather_data = fetch_weather_data()
    if weather_data:
        save_to_csv(weather_data)
        commit_to_github()
    else:
        print('Tidak ada data baru yang disimpan.')

# Jalankan streaming
stream_to_csv()
