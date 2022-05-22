import youtube_dl

ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'key': 'FFmpegExtractAudio',
        'extractaudio': True,
        'audioformat': 'mp3',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
        'nooverwrites': True,
        }

input_url = "https://www.youtube.com/watch?v=8jN8K79IiVE&list=PLyz7gy-MCAPlB4rsaMIIusUXtkrlPtfZa&index=9"

ytdl_format_options['playlist_items'] = "5-10"

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
info = ytdl.extract_info(input_url, download=False)

for song in info['entries']:
    print(song['title'])
