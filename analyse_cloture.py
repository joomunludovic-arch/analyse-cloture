import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import os

# === CONFIGURATION TELEGRAM ===
TELEGRAM_TOKEN = "8415756245:AAHaU2KBRsC3q05eLld2JjMt_V7S9j-o4ys"
CHAT_ID = "5814604646"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erreur envoi Telegram : {e}")

def send_telegram_image(image_path, caption="📈 Analyse graphique"):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': caption}
        try:
            requests.post(url, files=files, data=data)
        except Exception as e:
            print(f"Erreur envoi image Telegram : {e}")

def generate_fake_data(ticker, days=60):
    np.random.seed(hash(ticker) % 123456)
    base_price = np.random.uniform(80, 150)
    dates = pd.date_range(end=datetime.today(), periods=days)
    close = base_price + np.cumsum(np.random.randn(days))
    open_ = close - np.random.uniform(0.5, 2.0, days)
    volume = np.random.randint(100_000, 1_000_000, days)
    return pd.DataFrame({
        'Date': dates,
        'Ticker': ticker,
        'Open': open_,
        'Close': close,
        'Volume': volume
    })

def calculate_ichimoku(df):
    df['Tenkan_sen'] = df['Close'].rolling(window=9).mean()
    df['Kijun_sen'] = df['Close'].rolling(window=26).mean()
    return df

def run():
    try:
        tickers = ['AAPL', 'TSLA', 'NFLX']
        all_signals = []

        plt.figure(figsize=(12, 6))

        for ticker in tickers:
            df = generate_fake_data(ticker)
            df = df.sort_values(by='Date')
            df['Volatility'] = df['Close'].rolling(window=10).std()
            vol_mean = df['Volatility'].mean()
            vol_std = df['Volatility'].std()
            df['Z_score'] = (df['Volatility'] - vol_mean) / vol_std
            df = calculate_ichimoku(df)

            df['Signal'] = np.where(
                (df['Z_score'] > 2) & (df['Close'] > df['Tenkan_sen']) & (df['Close'] > df['Kijun_sen']),
                "📈 Signal haussier Ichimoku + Volatilité",
                np.where(
                    (df['Z_score'] > 2) & (df['Close'] < df['Tenkan_sen']) & (df['Close'] < df['Kijun_sen']),
                    "📉 Signal baissier Ichimoku + Volatilité",
                    ""
                )
            )

            # Graphique pour chaque ticker
            plt.plot(df['Date'], df['Close'], label=f'{ticker} - Close')
            plt.scatter(df['Date'][df['Signal'] != ""], df['Close'][df['Signal'] != ""], color='red', s=30)

            signals = df[df['Signal'] != ""][['Date', 'Ticker', 'Close', 'Z_score', 'Signal']].tail(3)
            all_signals.append(signals)

        plt.title("📊 Clôture & Signaux de volatilité")
        plt.xlabel("Date")
        plt.ylabel("Prix")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        image_path = "/tmp/signal_multi_ticker.png"
        plt.savefig(image_path)
        plt.close()

        final_alerts = pd.concat(all_signals)

        if not final_alerts.empty:
            messages = []
            for _, row in final_alerts.iterrows():
                msg = (
                    f"📌 {row['Ticker']} - {row['Date'].strftime('%Y-%m-%d')}\n"
                    f"💰 Prix : {row['Close']:.2f} | Z: {row['Z_score']:.2f}\n"
                    f"{row['Signal']}"
                )
                messages.append(msg)
            full_msg = "📊 Signaux détectés aujourd’hui :\n\n" + "\n\n".join(messages)
            send_telegram_message(full_msg)
            send_telegram_image(image_path, caption="📈 Graphique multi-actions avec signaux")
        else:
            send_telegram_message("✅ Aucune anomalie détectée aujourd’hui (Ichimoku + Volatilité).")

    except Exception as e:
        send_telegram_message(f"❌ Erreur dans le script : {str(e)}")