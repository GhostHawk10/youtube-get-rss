from yt_dlp import YoutubeDL
import os
import pickle
downloaded = []
download_queue = []
cached_urls = {}

def main():
    user_input()

def user_input():
    content = input("Enter content file name: ")
    path = input("Enter path: ")
    mode = input("0 - Download as video\n1 - Download as music\nEnter download mode: ")
    prepare_download(content, path, int(mode))
    return

def save_cache(cache, filename):
    with open(filename, 'wb') as file:
        pickle.dump(cache, file)
    
def load_cache(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def manage_cache(url, path):
    global cached_urls
    if not cached_urls:
        cached_urls = load_cache("cache.pkl")
        
    if url not in cached_urls:
        cached_urls[url] = path
        return False
    else:
        return True

def download_video(video_template):
    ydl_opts = {
        'outtmpl': video_template,
        'overwrites': False,
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True
    }
    return ydl_opts

def download_music(music_template):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
        }],
        'outtmpl': music_template,
        'overwrites': False,
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True
    }
    return ydl_opts

def download_content(queue, ydl_opts):
    if not queue:
        print("Nothing to download!")
        return

    print("Downloading content...")
    for entry in queue:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(entry)

def prepare_template(path, mode):
    if "~" in path:
        path = path.replace("~", os.path.expanduser("~"))

    video_template = f'{path}/%(channel)s/%(playlist_title)s/%(playlist_index)s %(title)s.%(ext)s'
    music_template = f'{path}/%(title)s.ogg'
    template = ""

    if mode == 0:
        template = video_template
    elif mode == 1:
        template = music_template

    return template

def prepare_download(content, path, mode):
    ydl_opts = {}
    urls = []

    template = prepare_template(path, mode)
    if mode == 0:
        ydl_opts = download_video(template)
    elif mode == 1:
        ydl_opts = download_music(template)
    
    with open(content, 'r') as f:
        print("Checking for existing files...")
        for line in f:
            url = line.split('#')[0].strip()
            urls.append(url)
        
    for url in urls:    
        if not manage_cache(url, path):
            download_queue.append(url)

    download_content(download_queue, ydl_opts)

    print("Saving cache...")
    save_cache(cached_urls, "cache.pkl")

if __name__ == '__main__':
    main()
