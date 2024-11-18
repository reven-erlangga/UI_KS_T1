from flask import Flask, request, jsonify
import hashlib
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify
from utils.encryption_utils import gen_fernet_key

def process_encryption(method, value, passcode):
    req_data = request.get_json()
    method = req_data['method']
    value = req_data['value']
    data = []

    data.append({
        'title': 'Initialize',
        "description": "System will be convert " + str(value)
    })

    
    if method == 'sha':
        hash_object = hashlib.sha256(value.encode('utf-8'))
        data.append({
            'title': 'Hash using hashlib',
            "description": "Hashing value using hashlib"
        })

        hex_dig = hash_object.hexdigest()
        data.append({
            'title': 'Value already hashing',
            "description": "Hashing object success to sha256, hash value is [encrypt]",
            "items": {
                "encrypt": {
                    "type": "input",
                    "value": str(hex_dig)
                }
            }
        })

        
    elif method == 'aes':
        key = gen_fernet_key(passcode.encode('utf-8'))
        f = Fernet(key)
        try:
            token = f.encrypt(value.encode('utf-8'))
            data.append({
                'title': 'Encryption using AES',
                'description': f'Encrypted value: {token.decode("utf-8")}',
            })
        except Exception as e:
            data.append({'title': 'Error', 'description': f'Error: {str(e)}'})
    
    elif method == 'rsa':
        key = RSA.generate(1024)
        publickey = key.publickey()
        encryptor = PKCS1_OAEP.new(publickey)
        encrypted = encryptor.encrypt(value.encode('utf-8'))
        encrypted_hex = hexlify(encrypted).decode()
        data.append({
            'title': 'RSA Encryption',
            'description': f'Encrypted value: {encrypted_hex}',
        })
    
    return {
        'data': data,
        'status': '200',
        'msg': 'Success!',
    }
