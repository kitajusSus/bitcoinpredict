import requests
import pandas as pd

# Konfiguracja zapytania do API Binance
base_url = 'https://api.binance.com/api/v3/klines'
symbol = 'BTCUSDT'  # Symbol pary handlowej
interval = '1d'  # Interwał (1d - dzienny, 1h - godzinowy, 1m - minutowy, itp.)
limit = 1000  # Ilość rekordów do pobrania

# Wykonanie zapytania GET do API Binance
params = {
    'symbol': symbol,
    'interval': interval,
    'limit': limit
}
response = requests.get(base_url, params=params)
data = response.json()

# Przetworzenie danych do formatu DataFrame
df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                 'Taker Buy Quote Asset Volume', 'Ignore'])
df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
df['Close'] = df['Close'].astype(float)

# Rozdzielenie kolumny "Open Time" na "Date" i "Time"
df['Date'] = df['Open Time'].dt.date
df['Time'] = df['Open Time'].dt.time

# Zapisanie danych do pliku CSV
df.to_csv('dane_bitcoin.csv', columns=['Date', 'Time', 'Close'], index=False)