import argparse
import logging
import threading
from flask import Flask, request, jsonify, abort

from kvs.kvs import KeyValueStore


app = Flask(__name__)
key_value_store = KeyValueStore()
lock = threading.RLock()

logging.basicConfig(level=logging.INFO)

@app.route('/api/ping')
def ping():
    return jsonify({'status': 'ok'})

@app.route('/api/<key>', methods=['GET'])
def get(key):
    with lock:
        result = key_value_store.get(key)

    result = result if result else 'null'
    return jsonify({'result': result})

@app.route('/api/<key>', methods=['POST'])
def set(key):
    if not request.json or not 'value' in request.json:
        abort(400)

    val = request.json.get('value')

    with lock:
        result = key_value_store.set(key, val)

    if result:
        result = f'{key}:{val} stored successfully'
    else:
        result = f'{key}:{val} error storing'

    return jsonify({'result': result})

@app.route('/api/<key>', methods=['DELETE'])
def delete(key):
    with lock:
        result = key_value_store.delete(key)

    if result:
        result = f'{key} deleted'
    else:
        result = f'{key} does not exist'

    return jsonify({'result': result})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1', type=str,
                        help='hostname/IP to run the server on. Default: 127.0.0.1')
    parser.add_argument('-p', '--port', default=25552, type=int,
                        help='port to run the server on. Default: 25552')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)

if __name__ == "__main__":
    main()