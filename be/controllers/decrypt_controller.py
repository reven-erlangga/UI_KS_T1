from flask import request, jsonify
from services.decrypt_service import process_decryption

def decrypt():
    req_data = request.get_json()
    method = req_data['method']
    hash_key = req_data['hash_key']
    encrypted = req_data['encrypted']
    
    response = process_decryption(method, hash_key, encrypted)
    
    return jsonify(response)
