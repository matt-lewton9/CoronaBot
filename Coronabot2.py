import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
from icecream import ic
from coronaHelper import *
import os
from dotenv import load_dotenv

ANDROIDS = 11 #channel # for androids

load_dotenv() #load env file
TOKEN = os.getenv("TOKEN") #get token from .env file

bot = commands.Bot(command_prefix="$") #create bot client

@bot.event # Log in
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) #print load message
    await bot.change_presence(activity=discord.Game("with dangerous buttons")) #set status
    
    for file in os.listdir('cogs.'): #iterate through cogs and load them
        if '.py' in file:
            bot.load_extension(f"cogs.{file[:-3]}") #load extension

@bot.command(brief='Pull a random quote form #quotations-for-blackmail') #pull random quote
async def rando(ctx):

    messages = [] #empty messages array
    message_limit = 500 #message get limit

    channel = ctx.guild.text_channels[4] #get quotes channel (4)
    async for message in channel.history(limit=message_limit): #get messages
        messages.append(message)

    await ctx.channel.send(f'Remember "{messages[random.randint(0, len(messages)-1)].content}"???') #send random message

@bot.command(hidden = True) #Manual mode, have the bot say whatever I say
async def m(ctx, *args):
    tgt_channel = int(args[0]) #channel to send message to
    text = makeString(args[1:]) #make text string
    await ctx.guild.channels[tgt_channel].send(text) #send message

@bot.event
async def on_message(message): #scan message
    
    if message.author == bot.user: #do not respond to self
        return

    guild = message.channel.guild #get guild

    ### No :Heart: ###
    if "?" in message.content:
        await message.channel.send('no :heart:')

    ### Bad Ellie... ###
    if message.author.discriminator == "0773":
            if ellieChecker(message):
                await ctx.channel.send("Dear FBI, Consider this a disclamer that we are fully aware Ellie is a minor and any implications that may have.")
    
    ### Dadbot ###
    dad_joke = dad(message.content)
    if dad_joke != None:
        await message.reply(dad_joke)

    await bot.process_commands(message)

bot.run(TOKEN) #run bot