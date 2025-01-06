from flask import Flask, send_file, jsonify, request
from werkzeug.utils import secure_filename
from flask_talisman import Talisman
from dotenv import load_dotenv
import logging
import os
import re
import json
from flask import Response

load_dotenv()

DEBUG = os.getenv("DEBUG")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
URL = os.getenv("URL")

app = Flask(__name__)

Talisman(app)

IMAGE_DIR = "/app/api/images"
MOBS_DIR = "/app/api/mobs"
DEATHS_DIR = "/app/api/deaths"

logging.basicConfig(filename='api.log', level=logging.INFO)


@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.url}")

@app.route('/images', methods=['GET'])
def list_images():
    """Retorna a lista de images disponíveis."""
    try:
        images = os.listdir(IMAGE_DIR)
        image_list = [{"filename": image, "name": re.sub(r'([a-z])([A-Z])', r'\1 \2', image.split('.')[0])} for image in images]
        return jsonify({"images": image_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/png/<filename>', methods=['GET'])
def get_image(filename):
    """Retorna a imagem especificada."""
    filename = secure_filename(filename)
    file_path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Imagem não encontrada."}), 404

    try:
        return send_file(file_path, mimetype='image/png'), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_image_mapping():
    """Gera um mapeamento entre nomes amigáveis e nomes reais."""
    images = os.listdir(IMAGE_DIR)
    mapping = {}
    for image in images:
        friendly_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', image.split('.')[0])
        no_space_friendly_name = friendly_name.replace(" ", "").lower()
        mapping[friendly_name.lower()] = image
        mapping[no_space_friendly_name] = image
    return mapping


@app.route('/images/<name>', methods=['GET'])
def get_image_by_name(name):
    """Retorna o link da imagem e o nome, dado o nome amigável."""
    try:
        mapping = get_image_mapping()
        filename = mapping.get(name.lower())
        if not filename:
            filename = mapping.get(name.replace(" ", "").lower())
        if not filename:
            return jsonify({"error": "Imagem não encontrada."}), 404
        image_url = filename
        return jsonify({"name": name, "url": f"{URL}{image_url}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mobs', methods=['GET'])
def list_mobs():
    """Retorna o JSON com a lista de mobs."""
    try:

        json_file_path = os.path.join(MOBS_DIR, 'mobs.json')

        if not os.path.exists(json_file_path):
            return jsonify({"error": "Arquivo JSON de mobs não encontrado."}), 404

        with open(json_file_path, 'r', encoding='utf-8') as file:
            mobs_data = json.load(file)

        response_data = json.dumps(mobs_data, ensure_ascii=False, indent=4)
        return Response(response_data, content_type="application/json; charset=utf-8"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deaths', methods=['GET'])
def list_deaths():
    try:

        json_file_path = os.path.join(DEATHS_DIR, 'deaths.json')

        if not os.path.exists(json_file_path):
            return jsonify({"error": "Arquivo JSON de mobs nao encontrado."}), 404

        with open(json_file_path, 'r', encoding='utf-8') as file:
            mobs_data = json.load(file)

        response_data = json.dumps(mobs_data, ensure_ascii=False, indent=4)
        return Response(response_data, content_type="application/json; charset=utf-8"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)