# -*- coding: utf-8 -*-
from flask import Flask, render_template
import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route('/')
def index():
  
    base_url = 'https://api.binance.com/api/v3/klines'
    symbol = 'BTCUSDT'  # Symbol pary handlowej
    interval = '1d'  # Interwał (1d - dzienny, 1h - godzinowy, 1m - minutowy, itp.)
    limit = 1000  # Ilość rekordów do pobrania

    
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(base_url, params=params)
    data = response.json()

 
    df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                     'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                     'Taker Buy Quote Asset Volume', 'Ignore'])
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close'] = df['Close'].astype(float)

  
    df['Date'] = df['Open Time'].dt.date
    df['Time'] = df['Open Time'].dt.time

 
    X = df.index.values.reshape(-1, 1)
    y = df['Close'].values

    model = LinearRegression()
    model.fit(X, y)

  
    latest_params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1  # Pobierz tylko ostatni rekord
    }
    latest_response = requests.get(base_url, params=latest_params)
    latest_data = latest_response.json()
    latest_close = float(latest_data[0][4])

    latest_prediction = model.predict([[len(df)]])

    # Określanie daty predykcji
    latest_date = df['Date'].iloc[-1]
    next_date = latest_date + timedelta(days=1)

    return render_template('index.html', latest_close=latest_close, current_date=datetime.now(), prediction_date=next_date, latest_prediction=latest_prediction[0])

if __name__ == '__main__':
    app.run()
