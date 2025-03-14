import asyncio

from flask import Flask, request, jsonify
from shazamio import Shazam
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor()


def run_async(func):
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@app.route('/recognize', methods=['GET'])
def recognize_song():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided', 'statusCode': 500, 'path': request.path}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected', 'statusCode': 400, 'path': request.path}), 400

    if file and file.filename.lower().endswith('.mp3'):
        # Read file data into memory
        file_data = file.read()

        # Run the asynchronous recognition
        result = executor.submit(
            run_async(recognize_song_async), file_data).result()

        if result and 'track' in result:
            return jsonify(result['track'])
        else:
            return jsonify({'error': 'Song not recognized', 'statusCode': 404, 'path': request.path}), 404
    else:
        return jsonify({'error': 'Invalid file format. Please upload an MP3 file.', 'statusCode': 400, 'path': request.path}), 400


@app.route('/search', methods=['GET'])
def search_song():
    if 'song' not in request.args:
        return jsonify({'error': 'No song provided', 'statusCode': 400, 'path': request.path}), 400

    song_name = request.args['song']
    if song_name == '':
        return jsonify({'error': 'No song selected', 'statusCode': 400, 'path': request.path}), 400

    # Run the asynchronous search
    result = executor.submit(run_async(search_song_async), song_name).result()

    if result and 'tracks' in result:
        return jsonify(result['tracks'])
    else:
        return jsonify({'error': 'Song not found', 'statusCode': 404, 'path': request.path}), 404


@app.route('/track', methods=['GET'])
def track_data():
    if 'id' not in request.args:
        return jsonify({'error': 'No track ID provided', 'statusCode': 400, 'path': request.path}), 400

    track_id = request.args['id']
    if track_id == '':
        return jsonify({'error': 'No track ID selected', 'statusCode': 400, 'path': request.path}), 400

    # Run the asynchronous track data retrieval
    result = executor.submit(run_async(track_data_async), track_id).result()
    print(result)

    if result and 'title' in result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Track not found', 'statusCode': 404, 'path': request.path}), 404


async def recognize_song_async(file_data):
    shazam = Shazam()
    return await shazam.recognize(file_data)


async def search_song_async(song_name):
    shazam = Shazam()
    return await shazam.search_track(query=song_name, limit=5)


async def track_data_async(track_id):
    shazam = Shazam()
    return await shazam.track_about(track_id=track_id)

if __name__ == '__main__':
    app.run(debug=False)
