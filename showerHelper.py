import discord
from discord.utils import get
from icecream import ic
import youtube_dl
import json

#format options are global
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
        'nooverwrites': True
        }

def get_song(query):
    
    tmpFormat = ytdl_format_options.copy()
    tmpFormat['noplaylist'] = True #no playlists in search results options

    if "https" in query: #remove playlist from url
        query = query[0:query.find('&')]

    ytdl = youtube_dl.YoutubeDL(tmpFormat)
    info = ytdl.extract_info(query, download=False)
    
    url = {} #make url object to store info abt video

    ic(query)

    try:
        song = info['entries'][0]
    except:
        song = info['entries']

    url['audio'] =  song['url'] #get vid url
    url['title'] =  song['title'] #get vid title
    url['webpage'] = song['webpage_url'] #get vid title
    url['duration'] = song['duration'] #get vid duration

    return url #return url with vid info

def getPlaylistItems(input_url, qLen, songNums):

    #format song numbers
    if "-" not in songNums: #if only starting number is given 
        songNums = int(songNums)
        songNums = f"{songNums}-{songNums+qLen-1}"
    
    tmp = songNums.split("-") #adjusts range to max at q length limit
    start, end = [int(tmp[0]), int(tmp[1])]
    if end-start > qLen:
        songNums = f"{start}-{start+qLen-1}"

    tmpFormat = ytdl_format_options.copy()
    tmpFormat['playlist_items'] = songNums #add song numbers to format options
    tmpFormat['noplaylist'] = False #no playlists in search results options

    ytdl = youtube_dl.YoutubeDL(tmpFormat) #api request
    info = ytdl.extract_info(input_url, download=False)
    
    playlist = info['entries']#[0:qLen]  #list of song dicts with info

    try:
        playlistTitle = info['title']
    except:
        playlistTitle = "No Title"

    playlist_Items = [] #playlist items to be returned
    
    for song in playlist:
        item = {} #temp item to be copied into playlist items
        item['audio'] =  song['url'] #get vid url
        item['title'] =  song['title'] #get vid title
        item['webpage'] = song['webpage_url'] #get vid title
        item['duration'] = song['duration'] #get vid duration

        playlist_Items.append(item)

    return playlist_Items, playlistTitle
    

def makeString(args):
    text = "" #get text string from args
    for arg in args: 
        text = text + " " + arg #add to text string
    return text

def embedBuilder(title = None, description = None, fields = None, colour = 0x00D31F, image = None, url = None, type = 'rich'):
    
    embed = discord.Embed( #make embed object
            title = title, #set title
            type = type, #set type
            colour=colour) #set color
    if description != None: #if there is a description, add it
        embed.description = description

    if url != None: #if there is a url, add it
        embed.url=url

    if fields != None: #if there are fields add them
        for entry in fields: #for each field
            embed.add_field(name=entry[0], value=entry[1], inline=entry[2]) #title, value, inline? (T/F)
    return embed #return embed

def timeFormat(sec): #format seconds to HH:MM:SS
    timeObjects = [sec / 3600, sec / 60, sec % 60]

    timeObjects = [sec / 3600, sec / 60, sec % 60]

    for idx in range(3):  #add zeros to time objects and save as strings
        time = timeObjects[idx]
        if time < 10: #if less than 10, add 0 in front
            timeObjects[idx] = "0" + str(int(time))
        else: 
            timeObjects[idx] = str(time)

    if int(timeObjects[0]) > 0: # if there are hours include them, otherwise omit
        format = f'{timeObjects[0]}:{timeObjects[1]}:{timeObjects[2]}'
    else:
        format = f'{timeObjects[1]}:{timeObjects[2]}'

    return format #return formatted time string