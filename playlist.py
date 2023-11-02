import json
from yt_dlp import YoutubeDL

names = []
urls = []
full_url = "https://www.youtube.com/watch?v="

with open('music.json') as data_file:
	for item in json.load(data_file):
		names.append(item["song_name"])
		urls.append(full_url + item["song_id"])

songs = zip(names, urls)

for (name, url) in songs:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
        }],
        'outtmpl': f"~/Music/{name}.%(ext)s"
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
