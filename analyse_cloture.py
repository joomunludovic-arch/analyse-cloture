import requests
from datetime import datetime

# 📬 CONFIGURATION TELEGRAM
TELEGRAM_TOKEN = "8415756245:AAHaU2KBRsC3q05eLld2JjMt_V7S9j-o4ys"  # << Remplace par ton token
TELEGRAM_CHAT_ID = "5814604646"  # << Remplace par ton ID de chat perso ou de canal

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erreur d’envoi Telegram : {e}")

def run():
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("📊 Début de l’analyse à", now)

        # 🧠 TA LOGIQUE D'ANALYSE ICI
        # Par exemple :
        resultat = sum(range(100))
        print("Résultat calculé :", resultat)

        # ✅ Succès
        message = f"✅ Analyse clôture réussie à {now}\nRésultat : {resultat}"
        send_telegram(message)
        print("📤 Notification Telegram envoyée.")

    except Exception as e:
        error_message = f"❌ Erreur dans l’analyse à {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n{str(e)}"
        print(error_message)
        send_telegram(error_import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import os

# === CONFIG TELEGRAM ===
TELEGRAM_TOKEN = "8415756245:AAHaU2KBRsC3q05eLld2JjMt_V7S9j-o4ys"
CHAT_ID = "5814604646"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def send_telegram_image(image_path, caption="📈 Analyse graphique"):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID, 'caption': caption}
        requests.post(url, files=files, data=data)

def run():
    try:
        # === 1. Simulation de données ===
        np.random.seed(42)
        dates = pd.date_range(end=datetime.today(), periods=90)
        prices = np.cumsum(np.random.randn(90)) + 100
        df = pd.DataFrame({
            'Date': dates,
            'Close': prices,
            'Open': prices - np.random.rand(90),
            'Volume': np.random.randint(50000, 500000, size=90)
        })

        # === 2. Analyse de la volatilité ===
        df['Volatility'] = df['Close'].rolling(window=10).std()
        vol_mean = df['Volatility'].mean()
        vol_std = df['Volatility'].std()
        df['Z_score'] = (df['Volatility'] - vol_mean) / vol_std

        # === 3. Détection de signaux ===
        df['Signal'] = np.where(
            (df['Z_score'] > 2) & (df['Close'] > df['Open']),
            "⚠️ Volatilité haussière (Breakout possible)",
            np.where(
                (df['Z_score'] > 2) & (df['Close'] < df['Open']),
                "🔻 Volatilité baissière (Correction possible)",
                ""
            )
        )

        alerts = df[df['Signal'] != ""]

        # === 4. Génération du graphique ===
        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['Close'], label='Prix de clôture', color='blue', alpha=0.6)
        plt.plot(df['Date'], df['Volatility'], label='Volatilité (10j)', color='orange')
        plt.scatter(alerts['Date'], alerts['Close'], color='red', label='⚠️ Signal', zorder=5)
        plt.title('Analyse de la Volatilité avec Signaux')
        plt.xlabel('Date')
        plt.ylabel('Valeur')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        image_path = "/tmp/volatilite_signaux.png"
        plt.savefig(image_path)
        plt.close()

        # === 5. Envoi des alertes ===
        if not alerts.empty:
            last_alerts = alerts.tail(3).copy()
            messages = []
            for _, row in last_alerts.iterrows():
                messages.append(
                    f"📊 {row['Date'].strftime('%Y-%m-%d')} - Prix : {row['Close']:.2f}\n"
                    f"{row['Signal']} (Z-score: {row['Z_score']:.2f})"
                )
            full_message = "\n\n".join(messages)
            send_telegram_message(full_message)
            send_telegram_image(image_path, caption="📈 Graphique des signaux détectés")
        else:
            send_telegram_message("✅ Aucune anomalie de volatilité détectée aujourd’hui.")
    except Exception as e:
        send_telegram_message(f"❌ Erreur dans le script : {str(e)}")
