from flask import Flask
import datetime
import requests
import pandas as pd
import numpy as np

# === CONFIG TELEGRAM ===
TELEGRAM_TOKEN = "8415756245:AAHaU2KBRsC3q05eLld2JjMt_V7S9j-o4ys"
CHAT_ID = "5814604646"

app = Flask(__name__)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erreur Telegram : {e}")

def analyse():
    tickers = ['AAPL', 'TSLA', 'NFLX']
    all_signals = []

    for ticker in tickers:
        np.random.seed(hash(ticker) % 123456)
        base_price = np.random.uniform(80, 150)
        dates = pd.date_range(end=datetime.datetime.today(), periods=60)
        close = base_price + np.cumsum(np.random.randn(60))
        open_ = close - np.random.uniform(0.5, 2.0, 60)
        volume = np.random.randint(100000, 1000000, 60)
        df = pd.DataFrame({
            'Date': dates,
            'Open': open_,
            'Close': close,
            'Volume': volume
        })

        df['Volatility'] = df['Close'].rolling(window=10).std()
        vol_mean = df['Volatility'].mean()
        vol_std = df['Volatility'].std()
        df['Z_score'] = (df['Volatility'] - vol_mean) / vol_std
        df['Tenkan_sen'] = df['Close'].rolling(window=9).mean()
        df['Kijun_sen'] = df['Close'].rolling(window=26).mean()

        df['Signal'] = np.where(
            (df['Z_score'] > 2) & (df['Close'] > df['Tenkan_sen']) & (df['Close'] > df['Kijun_sen']),
            "📈 Signal haussier Ichimoku + Volatilité",
            np.where(
                (df['Z_score'] > 2) & (df['Close'] < df['Tenkan_sen']) & (df['Close'] < df['Kijun_sen']),
                "📉 Signal baissier Ichimoku + Volatilité",
                ""
            )
        )

        alerts = df[df['Signal'] != ""][['Date', 'Close', 'Z_score', 'Signal']].tail(3)
        alerts["Ticker"] = ticker
        all_signals.append(alerts)

    final = pd.concat(all_signals)
    if not final.empty:
        messages = []
        for _, row in final.iterrows():
            messages.append(
                f"📌 {row['Ticker']} - {row['Date'].strftime('%Y-%m-%d')}\n"
                f"💰 Prix : {row['Close']:.2f} | Z: {row['Z_score']:.2f}\n"
                f"{row['Signal']}"
            )
        send_telegram_message("📊 Signaux détectés :\n\n" + "\n\n".join(messages))
        return "\n".join(messages)
    else:
        msg = "✅ Aucune anomalie détectée aujourd’hui (Ichimoku + Volatilité)."
        send_telegram_message(msg)
        return msg

@app.route("/")
def run():
    result = analyse()
    return "✅ Analyse exécutée avec succès.\n" + result