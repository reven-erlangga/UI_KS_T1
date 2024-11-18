from flask import request, jsonify
from services.crypt_service import process_encryption

def crypt():
    req_data = request.get_json()
    method = req_data['method']
    value = req_data['value']
    passcode = req_data.get('crypt_key', '')
    
    response = process_encryption(method, value, passcode)
    
    return jsonify(response)
