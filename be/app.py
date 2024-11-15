from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import hashlib
from cryptography.fernet import Fernet
import base64, hashlib
import Crypto 
from Crypto.PublicKey import RSA 
from Crypto import Random
import ast
from Crypto.Cipher import PKCS1_OAEP
from os import chmod
import rsa
from flask import send_file
from binascii import hexlify, unhexlify

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/crypt", methods=['POST'])
def crypt():
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

        return jsonify({
            'data': data,
            'status': '200',
            'msg': 'Success creating a new book!👍😀'
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

        return jsonify({
            'data': data,
            'status': '200',
            'msg': 'Success creating a new book!👍😀'
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
        # decryptor = PKCS1_OAEP.new(key)
        # decrypted = decryptor.decrypt(ast.literal_eval(str(unhexlify(hex))))

        return jsonify({
            'data': data,
            'status': '200',
            'msg': 'Success creating a new book!👍😀'
        })
    
    return jsonify({
        # 'error': '',
        'data': f'Error ⛔❌!',
        'status': '404'
    })

@app.route("/decrypt", methods=['POST'])
def decrypt():
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

        return jsonify({
            'data': data,
            'status': '200',
            'msg': 'Success decrypt sha!👍😀'
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
        

        return jsonify({
            'data': data,
            'status': '200',
            'msg': 'Success decrypt aes!👍😀'
        })
    
    elif 'rsa':
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

        return jsonify({
            'data': data,
            'status': '200',
            'msg': 'Success decrypt rsa!👍😀'
        })


    return jsonify({
        'data': f'Error ⛔❌!',
        'status': '404'
    })


@app.route('/download/<file>', methods=['GET', 'POST'])
def download_link(file):
    assert file == request.view_args['file']
    path = "tmp/" + file

    return send_file(path, as_attachment=True)

def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

if __name__ == '__main__':
    app.run(debug=True)
