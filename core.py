print("""
  __  __ _     _ _  ____                        
 |  \/  (_)   | (_)/ __ \                       
 | \  / |_  __| |_| |  | |_   _  ___ _   _  ___ 
 | |\/| | |/ _` | | |  | | | | |/ _ \ | | |/ _ \\
 | |  | | | (_| | | |__| | |_| |  __/ |_| |  __/
 |_|  |_|_|\__,_|_|\___\_\\__,_|\___|\__,_|\___|
                                                
""")
import mido
import time
import asyncio
i = 1
outputs = []
for v in mido.get_output_names():
    print(str(i)+" | "+v)
    i=i+1
    outputs.append(v)

global my_function

while True:
    MIDIOUTPUT = input("\nSelect an output (1-"+str(len(outputs))+")\n>")
    try:
        MIDIOUTPUT = int(MIDIOUTPUT)
    except:
        print("Invalid Option")
    if (MIDIOUTPUT >= 1) and (MIDIOUTPUT <= len(outputs)):
        MIDIOUTPUT = MIDIOUTPUT - 1
        MIDIOUTPUT = outputs[MIDIOUTPUT]
        break
    else:
        print("Invalid Option")
import discord
from discord.ext import commands
import requests, random
import os
import json
with open('settings.json', 'r') as file:
    settings = json.load(file)
from discord import ButtonStyle, Button

def remove_files_in_folder(folderPath):
        # loop through all the contents of folder
        for filename in os.listdir(folderPath):
            # remove the file
            os.remove(f"{folderPath}/{filename}")

remove_files_in_folder('files')

Queue = []
NowPlaying = False
RightNow = False
description = "N/A"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', description=description, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("System Ready!")
    global NPC
    NPC = bot.get_channel(settings["output_channel_discord"])
    embed = discord.Embed(title='Bot Online', color=discord.Color.random(), description="The bot is now ready to recieve commands.")
    embed.add_field(name="Output Port", value="`"+MIDIOUTPUT+"`", inline=False)
    await NPC.send(embed = embed)

@bot.command(pass_context=True)
async def setup(ctx, A=None, B=None):
    print(A, B)
    if A:
        if A == "output_port":
            # List
            i = 1
            outputs = []
            stringdisplay = ""
            for v in mido.get_output_names():
                stringdisplay = stringdisplay+(str(i)+" | "+v)+"\n"
                i=i+1
                outputs.append(v)
            if B:
                try:
                    OutputName = outputs[int(B)-1]
                    MIDIOUTPUT = OutputName
                    embed = discord.Embed(title='Updated', color=discord.Color.random(), description="Updated setting.")
                    embed.add_field(name = "New Port", value=MIDIOUTPUT)
                    await ctx.message.reply(embed = embed) 
                except Exception as Exc:
                    embed = discord.Embed(title=':x: Invalid', color=discord.Color.random(), description="Invalid argument #2.")
                    embed.add_field(name = "Error Type", value=Exc)
                    await ctx.message.reply(embed = embed) 
            else:
                stringdisplay = stringdisplay+"\nUse the numbers on the left. (`.setup output_port 4`)"
                embed = discord.Embed(title='Output Ports', color=discord.Color.random(), description=stringdisplay)
                await ctx.message.reply(embed = embed) 
        elif A == "now_playing":
            try:
                if B:
                    B = int(B)
                    BB = bot.get_channel(B)

                    if BB:
                        settings["output_channel_discord"] = B
                        NPC = BB

                        with open("settings.json", "w") as json_file:
                            json.dump(settings, json_file)
                        await BB.send("This channel has been set as the bot's output.")
                        await ctx.message.reply("Updated.")
                    else:
                        await ctx.message.reply("Invalid.")
                else:
                    settingstag = "<#"+settings["output_channel_discord"]+">"
                    await ctx.message.reply("Current channel -> "+settingstag+".")
            except Exception as Exc:
                embed = discord.Embed(title=':x: Invalid', color=discord.Color.random(), description="Invalid argument #2.")
                embed.add_field(name = "Error Type", value=Exc)
                await ctx.message.reply(embed = embed) 
        else:
            embed = discord.Embed(title=':x: Invalid Option', color=discord.Color.random(), description="Select an option from below.")
            embed.add_field(name=".setup output_port name", value="Overwrites the output_port. Not providing the `output_port` will list all ports.", inline=False)
            embed.add_field(name=".setup now_playing channelid", value="Overwrites the output channel for 'now playing' messages.", inline=False)
            await ctx.message.reply(embed = embed) 
    else:
        embed = discord.Embed(title='Setup Options', color=discord.Color.random(), description="Select an option from below.")
        embed.add_field(name=".setup output_port name", value="Overwrites the output_port. Not providing the `output_port` will list all ports.", inline=False)
        embed.add_field(name=".setup now_playing channelid", value="Overwrites the output channel for 'now playing' messages.", inline=False)
        await ctx.message.reply(embed = embed)
    

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Piotr Midi', color=discord.Color.random(), description="Hi! I'm a bot designed to accept Midi requests and play them. You can add a MIDI to my queue by saying `.add` and attaching the MIDI file.")
    embed.add_field(name=".add", value="Send this command with an attachment and it will be added to the queue.", inline=False)
    embed.add_field(name=".queue", value="View the queue and your position in it.", inline=False)
    await ctx.message.reply("<@"+str(ctx.message.author.id)+">", embed = embed)

@bot.command()
async def current(ctx):
    embed = discord.Embed(title='Now Playing', color=discord.Color.random())
    
    TrackName = NowPlaying["trackname"] or "N/A"
    RequestedBy = NowPlaying["filename"] or "N/A"
    RequestedByTag = "<@"+RequestedBy+">"

    embed.add_field(name="Track Name", value=TrackName, inline=False)

    if RequestedBy == "AutoMaestro":
        embed.add_field(name="Requested By", value="Auto Maestro (Autoplay)")
        RequestedByTag = "Auto Maestro"
    else:
        embed.add_field(name="Requested By", value=RequestedByTag)

    await ctx.message.reply(RequestedByTag, embed = embed)

@bot.command()
async def queue(ctx):
    embed = discord.Embed(title='Queue', color=discord.Color.random())
    Position = "N/A"
    i = 1
    for v in Queue:
        if v["filename"] == str(ctx.message.author.id):
            Position = str(i)
            break
        i = i + 1
    embed.add_field(name="Total", value=str(len(Queue)))
    embed.add_field(name="Your Position", value=Position)
    await ctx.message.reply(embed = embed)
from urllib.parse import urlparse

@bot.command()
async def add(ctx):
    try:
        for v in Queue:
            if str(ctx.message.author.id) == v["filename"]:
                embed = discord.Embed(title=':x: ERROR', description = "You already have a track waiting.\nRun `.queue`",color=discord.Color.random())
                await ctx.message.reply(embed = embed)
                return
        if len(ctx.message.attachments) != 1:
            embed = discord.Embed(title=':x: ERROR', description = "Provide exactly one attachment!",color=discord.Color.random())
            await ctx.message.reply(embed = embed)
        else:
            url = ctx.message.attachments[0].url
            parsed_url = urlparse(url)
            
            # Check if the URL points to a MIDI file
            print(parsed_url.path)
            if not parsed_url.path.endswith(('.mid', '.midi')):
                embed = discord.Embed(title=':x: ERROR', description = "Invalid File Type",color=discord.Color.random())
                await ctx.message.reply(embed = embed)
                return
            folder_path = os.getcwd()+"\\files"
 
            # Extract the filename from the URL
            filename = str(ctx.message.author.id)

            # Define the complete file path
            file_path = os.path.join(folder_path, filename)

            trackname = parsed_url.path.split("/")
            trackname = trackname[len(trackname)-1]
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Save the file to the specified folder
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                embed = discord.Embed(title='Success', description = "Added your file to the queue.\nRun `.queue` to view it's position.",color=discord.Color.random())
                embed.add_field(name="Track Name", value=trackname)
                await ctx.message.reply(embed = embed)
                Queue.append({
                    "filename": filename,
                    "trackname": trackname
                })
                mid = mido.MidiFile("files\\"+filename, clip=True)
            else:
                embed = discord.Embed(title=':x: ERROR', description = "Download Failed",color=discord.Color.random())
    except Exception as Exc:
        await ctx.message.reply(Exc)
        print(Exc)

import asyncio
import concurrent.futures

def playtrack(filetoplay, jukebox = False, tracknom = "No Name"):
    if jukebox:
        embed = discord.Embed(title='Now Playing...', color=discord.Color.random(), description="A track requested by <@"+jukebox+">.")
        embed.add_field(name = "Track Name", value = tracknom)
        asyncio.run_coroutine_threadsafe(NPC.send("<@"+jukebox+">", embed = embed), loop=bot.loop)
    else:
        embed = discord.Embed(title='Now Playing...', color=discord.Color.random(), description="A random song from autoplay.")
        embed.add_field(name = "Track Name", value = tracknom)
        asyncio.run_coroutine_threadsafe(NPC.send(embed = embed), loop=bot.loop)
    
    try:
        # Open the MIDI output port
        output_port = mido.open_output(MIDIOUTPUT)
    
        # Load the MIDI file
        mid = mido.MidiFile(filetoplay)
        if jukebox:
            os.remove(filetoplay)

        # Get the ticks per beat value from the MIDI file
        ticks_per_beat = mid.ticks_per_beat

        # Iterate over each message in the MIDI file
        for message in mid.play():
            output_port.send(message)

        # Close the MIDI output port
        output_port.close()
        print("Finished Track")

    except Exception as e:
        print(e)
        asyncio.run_coroutine_threadsafe(NPC.send(f"Error: {e}"), loop=bot.loop)

randoms = os.listdir("maestro")
randoms = [file for file in randoms if os.path.isfile(os.path.join("maestro", file))]
async def my_function():
    while True:
        await asyncio.sleep(1)
        if len(Queue) != 0:
            global NowPlaying
            NowPlaying = Queue[0]
            Queue.pop(0)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                def x():
                    playtrack("files\\"+NowPlaying["filename"], jukebox=NowPlaying["filename"], tracknom=NowPlaying["trackname"])
                await bot.loop.run_in_executor(executor, x)
                #await bot.loop.run_in_executor(executor, playtrack, "files\\"+NowPlaying["filename"], jukebox=NowPlaying["filename"], tracknom=NowPlaying["trackname"])
        else:
            try:
                # Random Maestro


                folder_path = 'maestro'
                file_list = os.listdir(folder_path)
                file_list = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file))]
                random_track = random.choice(file_list)

                NowPlaying = {
                    "filename": "AutoMaestro",
                    "trackname": random_track
                }

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    def x():
                        playtrack("maestro\\"+random_track, tracknom=random_track)
                    await bot.loop.run_in_executor(executor, x)
            except Exception as Exc:
                print("! Auto Maestro - Failed.\nPerhaps the bot has not loaded yet.")
                print(Exc)


async def run_bot():
    await bot.start(settings["token"])

# Create the event loop
loop = asyncio.get_event_loop()

# Schedule the tasks
tasks = [my_function(), run_bot()]

# Run the event loop
loop.run_until_complete(asyncio.gather(*tasks))