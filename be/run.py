from flask import Flask
from flask_cors import CORS
from controllers.crypt_controller import crypt
# from controllers.decrypt_controller import decrypt

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Register routes
app.add_url_rule('/crypt', 'crypt', crypt, methods=['POST'])
# app.add_url_rule('/decrypt', 'decrypt', decrypt, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
