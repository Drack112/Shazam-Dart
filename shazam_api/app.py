import asyncio

from shazamio import Shazam
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor()


def run_async(func):
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@app.route("/search", methods=["GET"])
def search_song():
    if 'song' not in request.args:
        return jsonify({'error': 'No song provided', 'statusCode': 400, 'path': request.path}), 400

    song_name = request.args["song"]
    if song_name == '':
        return jsonify({'error': 'No song selected', 'statusCode': 400, 'path': request.path}), 400

    result = executor.submit(run_async(search_song_async), song_name).result()
    if result and 'tracks' in result:
        return jsonify(result['tracks'])
    else:
        return jsonify({'error': 'No song found', 'statusCode': 404, 'path': request.path}), 404


async def search_song_async(song_name):
    shazam = Shazam()
    return await shazam.search_track(query=song_name, limit=5)

if __name__ == '__main__':
    app.run(debug=False)
