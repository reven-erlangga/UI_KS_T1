from flask import Flask, request, jsonify
import hashlib
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto import Random
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
        data.append({
            'title': 'Initialize',
            "description": "AES encryption processing"
        })

        passcode = req_data['crypt_key']
        data.append({
            'title': 'Crypt Key',
            "description": "Prepare crypt key to generate using fernet, your crypt key is [crypt_key]",
            "items": {
                "crypt_key": {
                    "type": "input",
                    "value": str(passcode)
                }
            }
        })

        key = gen_fernet_key(passcode.encode('utf-8'))
        data.append({
            'title': 'Generate',
            "description": "Generate hashing key using fernet library"
        })

        f = Fernet(key)
        data.append({
            'title': 'Key',
            "description": "Make a key using fernet library"
        })

        try:
            token = f.encrypt(value.encode('utf-8'))
            
            data.append({
                'title': 'Success',
                "description": "Encryption value using aes success, encrypt value is [encrypt]",
                "items": {
                    "encrypt": {
                        "type": "input",
                        "value": str((token).decode("utf-8"))
                    }
                }
            })
        except:
            data.append({
                'title': 'Failed',
                "description": "Encryption value using aes failed"
            })


    
    elif method == 'rsa':
        
        data.append({
            'title': 'Initialize',
            "description": "RSA encryption processing"
        })

        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator) #generate pub and priv key
        data.append({
            'title': 'Private Key',
            "description": "RSA generate private key"
        })

        publickey = key.publickey() # pub key export for exchange
        data.append({
            'title': 'Public Key',
            "description": "RSA generate public key",
        })

        f = open('tmp/private-rsa.pem', 'wb')
        f.write(key.exportKey('PEM'))
        f.close()
        data.append({
            'title': 'Export Key',
            "description": "RSA exporting key, download file [download]",
            "items": {
                "download": {
                    "type": "link",
                    "value": "http://127.0.0.1:5000/download/private-rsa.pem"
                }
            }
        })

        encryptor = PKCS1_OAEP.new(publickey)
        data.append({
            'title': 'PKCS OEAP',
            "description": "PKCS#1 OAEP is an asymmetric cipher based on RSA and the OAEP padding",
        })

        # value = b"Hello, this is a message to be encrypted."
        encrypted = encryptor.encrypt(value.encode('ascii'))
        data.append({
            'title': 'Generate',
            "description": "Generate encryption value using PKCS1_OAEP"
        })

        hex = (hexlify(encrypted))
        
        f = open('tmp/encryption-message.txt', 'wb')
        f.write(encrypted)
        f.close()
        data.append({
            'title': 'Export message',
            "description": "RSA exporting message, download file [download]",
            "items": {
                "download": {
                    "type": "link",
                    "value": "http://127.0.0.1:5000/download/encryption-message.txt"
                }
            }
        })
    
    return {
        'data': data,
        'status': '200',
        'msg': 'Success!',
    }
