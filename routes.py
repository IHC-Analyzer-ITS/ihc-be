from flask import request, jsonify, send_from_directory, render_template
from utils import process_data, get_data_from_json, capture_image, projects_image  # Import fungsi yang dibutuhkan

def setup_routes(app):
    @app.route('/', methods=['GET'])
    def documentation():
        return render_template('documentation.html')
    
    @app.route('/data', methods=['POST'])
    def submit_data():
        # Ambil data JSON yang dikirim melalui POST
        data = request.json

        # Cek apakah data ada
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Proses data menggunakan fungsi dari utils.py
        response, status_code = process_data(data)

        # Kembalikan respon yang sesuai
        return jsonify(response), status_code
    
    # Perbaikan pada methods (harus dalam bentuk list)
    @app.route('/data', methods=['GET'])
    def get_data():
        # Mengambil data dari JSON file menggunakan fungsi dari utils.py
        data, status_code = get_data_from_json()

        # Kembalikan data yang diambil dan status code
        return jsonify(data), status_code

    @app.route('/capture/<name>', methods=['POST'])
    def get_image_by_user(name):
        data = request.json
        # name = data.get('name')
        if not name:
            return jsonify({"error": "Name is required"}), 400

        data_1, status_code = capture_image(user_name=name)
        return jsonify(data_1), status_code
    
    @app.route('/images/<path:filename>')
    def custom_static(filename):
        return send_from_directory('projects/', filename)
    
    @app.route('/projects/<name>', methods=['GET'])
    def get_projects_image(name):
        # Contoh data gambar
        data, response = projects_image(name)

        return jsonify(data), response