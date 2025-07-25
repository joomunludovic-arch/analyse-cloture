from flask import Flask, request
import analyse_cloture
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run_script():
    try:
        print("🔄 Début de l’analyse automatique")
        analyse_cloture.run()
        print("✅ Analyse terminée avec succès")
        return "✅ Analyse exécutée avec succès"
    except Exception as e:
        print(f"❌ Erreur pendant l’analyse : {e}")
        return f"❌ Erreur pendant l’analyse : {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render impose cette variable
    app.run(host='0.0.0.0', port=port)
