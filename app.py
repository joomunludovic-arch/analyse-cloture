from flask import Flask
import analyse_cloture

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def lancer():
    analyse_cloture.run()
    return "✅ Analyse exécutée."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
