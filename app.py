from flask import Flask, request
import analyse_cloture 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run_script():
    try:
        print("🔄 Début de l’analyse automatique")
        analyse_cloture.run()  # Appelle ta fonction principale 
        print("✅ Analyse terminée avec succès")
        return "✅ Analyse exécutée avec succès", 200
    except Exception as e:
        print(f"❌ Erreur pendant l’analyse : {e}")
        return f"❌ Erreur pendant l’analyse : {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
