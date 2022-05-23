import discord
from discord.utils import get
from icecream import ic
import pyttsx3
import youtube_dl

#declare voice keys
en_uk_F = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
en_au_F = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_enAU_CatherineM'
en_uk_M = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'
en_us_F = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'
en_ir_F = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_SusanM'

#ellie Checker
def ellieChecker(message): 
    words = ['ill', "i'll", 'ur', 'your'] #flag words
    punctuations = '''!()[]{};:'",<>./?@#$%^&*~''' #punctuation to remove from strings
    w = 0 # init word counter to 0
    for word in message.content.lower().split(): #split message into list of words
        for char in word: #check each word
            if char in punctuations: #reset for each punctuation
                w = 0
        if word.lower() in words: #add to counter for each flag word
            w += 1
    if w == 2: #if two flag words in a sentence, return true
        return True

#retrieve random message for rando command
def troll(ctx):
    quotes = 4
    messages = [] #empty messages array
    message_limit = 500 #message get limit

    channel = ctx.guild.text_channels[quotes] #get quotes channel
    ic(ctx.channel.history(limit=message_limit))
    for message in ctx.channel.history(limit=message_limit): #get messages
        messages.append(message)
    return messages[random.randint(0, len(messages)-1)].content #return random message

#save text as audiofile
def tts(input, filename):
    engine = pyttsx3.init() #init engine
    engine.setProperty('rate', 150) #set speaking rate
    engine.setProperty('voice', en_au_F) #set voice
    engine.save_to_file(input, filename) #save to filke
    engine.runAndWait()    

#run dadbot
def dad(msg):
    #scan message
    punctuations = '''!()[]{};:'",<>./?@#$%^&*~'''
    output = None
    no_punct = ""
    for char in msg:
        if char not in punctuations:
            no_punct = no_punct + char   

    msg = no_punct.lower()

    words = msg.lower().split()
    im = ["i'm", 'im']
    for i in words:
        if i in im:
            im_int = words.index(i)
            if words[im_int+1] in ['a', 'an', 'the']: 
                output = "Hi " + words[im_int+2] + ", I'm dad."
            elif words[im_int+1] == "not":
                output = "Hi not " + words[im_int+2] + ", I'm dad."
            else:
                output = "Hi " + words[im_int+1] + ", I'm dad."
    return output

def makeString(args):
    text = "" #get text string from args
    for arg in args: 
        text = text + " " + arg #add to text string
    return text