import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os
import requests

# === CONFIGURATION ===
TELEGRAM_TOKEN = "8415756245:AAHaU2KBRsC3q05eLld2JjMt_V7S9j-o4ys"
CHAT_ID = "5814604646"
TICKERS = ["TSLA", "AAPL", "NVDA"]  # 👈 Personnalise ici les actions à suivre
DAYS = 90

# === FONCTIONS TELEGRAM ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[❌] Erreur Telegram : {e}")

def send_telegram_image(image_path, caption="📊 Graphique"):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': caption}
        try:
            requests.post(url, files=files, data=data)
        except Exception as e:
            print(f"[❌] Erreur envoi image : {e}")

# === ICHIMOKU ===
def calculate_ichimoku(df):
    df['Tenkan_sen'] = df['Close'].rolling(window=9).mean()
    df['Kijun_sen'] = df['Close'].rolling(window=26).mean()
    return df

# === DONNÉES SIMULÉES (à remplacer par Yahoo Finance si tu veux du vrai) ===
def generate_fake_data(ticker):
    np.random.seed(hash(ticker) % 99999)
    base_price = np.random.uniform(100, 300)
    dates = pd.date_range(end=datetime.today(), periods=DAYS)
    close = base_price + np.cumsum(np.random.randn(DAYS))
    open_ = close - np.random.uniform(0.5, 2.0, DAYS)
    volume = np.random.randint(100_000, 1_000_000, DAYS)
    return pd.DataFrame({
        'Date': dates,
        'Ticker': ticker,
        'Open': open_,
        'Close': close,
        'Volume': volume
    })

# === ANALYSE COMPLÈTE ===
def run_analysis():
    try:
        all_signals = []
        for ticker in TICKERS:
            df = generate_fake_data(ticker)
            df = df.sort_values("Date")
            df = calculate_ichimoku(df)

            # Volatilité & Z-score
            df['Volatility'] = df['Close'].rolling(window=10).std()
            vol_mean = df['Volatility'].mean()
            vol_std = df['Volatility'].std()
            df['Z_score'] = (df['Volatility'] - vol_mean) / vol_std

            # Signaux
            df['Signal'] = np.where(
                (df['Z_score'] > 2) & (df['Close'] > df['Tenkan_sen']) & (df['Close'] > df['Kijun_sen']),
                "📈 Signal haussier Ichimoku + Volatilité",
                np.where(
                    (df['Z_score'] > 2) & (df['Close'] < df['Tenkan_sen']) & (df['Close'] < df['Kijun_sen']),
                    "📉 Signal baissier Ichimoku + Volatilité",
                    ""
                )
            )

            recent_signals = df[df['Signal'] != ""].tail(1)
            if not recent_signals.empty:
                for _, row in recent_signals.iterrows():
                    msg = (
                        f"📌 {ticker} - {row['Date'].strftime('%Y-%m-%d')}\n"
                        f"💰 Prix : {row['Close']:.2f} | Z : {row['Z_score']:.2f}\n"
                        f"{row['Signal']}"
                    )
                    send_telegram_message(msg)

            # Graphique
            plt.figure(figsize=(12, 6))
            plt.plot(df['Date'], df['Close'], label='Clôture', color='blue')
            plt.plot(df['Date'], df['Tenkan_sen'], label='Tenkan', linestyle='--')
            plt.plot(df['Date'], df['Kijun_sen'], label='Kijun', linestyle='--')
            plt.scatter(recent_signals['Date'], recent_signals['Close'], color='red', label='Signal', zorder=5)
            plt.title(f'{ticker} - Analyse Ichimoku & Volatilité')
            plt.xlabel('Date')
            plt.ylabel('Prix')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            image_path = f"/tmp/{ticker}_graph.png"
            plt.savefig(image_path)
            plt.close()
            send_telegram_image(image_path, caption=f"📉 {ticker} - Tendance actuelle")

        if not all_signals:
            send_telegram_message("✅ Aucune alerte détectée sur les actions suivies.")

    except Exception as e:
        send_telegram_message(f"❌ Erreur dans l’analyse : {str(e)}")

# === EXÉCUTION PRINCIPALE ===
if __name__ == "__main__":
    run_analysis()