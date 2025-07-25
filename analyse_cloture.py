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
        send_telegram(error_message)
