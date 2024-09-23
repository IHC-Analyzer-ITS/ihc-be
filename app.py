from flask import Flask, jsonify
from routes import setup_routes  # Import fungsi untuk men-setup routes

app = Flask(__name__)
# Setup routes dari file routes.py
setup_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
