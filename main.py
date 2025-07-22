import string
import random
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
url_db = {}

def gerar_chave(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

@app.route('/encurtar', methods=['POST'])
def encurtar_url():
    dados = request.get_json()
    url_original = dados.get('url')

    if not url_original:
        return jsonify({'erro': 'URL não fornecida'}), 400

    chave = gerar_chave()
    while chave in url_db:
        chave = gerar_chave()

    url_db[chave] = url_original
    return jsonify({'url_encurtada': f'http://localhost:5000/{chave}'})

@app.route('/<chave>')
def redirecionar(chave):
    url = url_db.get(chave)
    if url:
        return redirect(url)
    return jsonify({'erro': 'URL não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
