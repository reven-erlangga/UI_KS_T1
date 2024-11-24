import base64, hashlib
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from utils.encryption_utils import gen_fernet_key
from binascii import unhexlify
import ast


def process_decryption(method, hash_key, encrypted):
    req_data = request.get_json()
    method = req_data['method']
    hash_key = req_data['hash_key']
    encrypted = req_data['encrypted']
    data = []
    
    if method == 'sha':
        data.append({
            'title': 'Initialize',
            "description": "SHA decryption processing"
        })

        hash_object = hashlib.sha256(hash_key.encode('utf-8'))
        data.append({
            'title': 'Hash',
            "description": "Hashing value using hashlib library"
        })

        hex_dig = hash_object.hexdigest()
        data.append({
            'title': 'Hashing',
            "description": "Hashing object success to sha256, hash value is " + hex_dig
        })

        data.append({
            'title': 'Compare',
            "description": "Original value '" + hash_key + "' will be compare with hashing value"
        })

        if hex_dig == encrypted:
            data.append({
                'title': 'Success',
                "description": "Encryption value using sha success, value and hashing value matched"
            })
        else:
            data.append({
                'title': 'Failed',
                "description": "Encryption value using sha failed, value and hashing value not matched"
            })
    
    elif method == 'aes':
        data.append({
            'title': 'Initialize',
            "description": "AES decryption processing"
        })

        passcode = req_data['hash_key']
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
            decrypt = f.decrypt(encrypted).decode("utf-8")

            data.append({
                'title': 'Success',
                "description": "Encryption value using aes success, encrypt value is " + str(decrypt)
            })
        except:
            data.append({
                'title': 'Failed',
                "description": "Encryption value using aes failed"
            })
    
    elif method == 'rsa':
        data.append({
            'title': 'Initialize',
            "description": "RSA decryption processing"
        })

        private_key = base64.b64decode(hash_key)
        data.append({
            'title': 'Private Key',
            "description": "Decode private key from base64"
        })
        
        encrypted = base64.b64decode(encrypted)
        data.append({
            'title': 'Encryption Message',
            "description": "Decode encryption message from base64"
        })

        mykey = RSA.importKey(private_key)
        data.append({
            'title': 'Import Key',
            "description": "Import private key to RSA key"
        })

        try:
            decryptor = PKCS1_OAEP.new(mykey)
            data.append({
                'title': 'Decrypt Key',
                "description": "Decryption private rsa key"
            })

            decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
            data.append({
                'title': 'Decryption',
                "description": "Decryption message using private rsa key"
            })

            decrypt = (decrypted).decode('ascii')
            data.append({
                'title': 'Decode',
                "description": "Decode message to ascii to make sure message can readable!"
            })

            data.append({
                'title': 'Success',
                "description": "Encryption value using aes success, encrypt value is '" + str(decrypt) + "'"
            })
        except:
            data.append({
                'title': 'Failed',
                "description": "Encryption value using aes failed"
            })

    
    return {
        'data': data,
        'status': '200',
        'msg': 'Success!',
    }
