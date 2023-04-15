import os
from pathlib import Path
import discord
from dotenv import load_dotenv
from datetime import datetime

from ai.chat import chatBot
from ai.image import imageBot
from ai.pollen import pollenBot
from logger.logger import Logger


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
logger = Logger()


chat_bot = chatBot(api_key=OPENAI_API_KEY)
image_bot = imageBot(api_key=OPENAI_API_KEY)
pollen_bot = pollenBot() 

# discord intents 
intents = discord.Intents.default()
intents.message_content = True

# Set up the Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Connected to Discord!')


@client.event
async def on_message(message):
    # don't react to own messages
    if message.author == client.user:
        return

    channel = client.get_channel(message.channel.id)
    channel_name = message.channel

    user = str(message.author).split("#")[0].lower()

    # chatgpt
    if message.content.startswith('!gpt'):
        logger.info(f"{message.channel} - {message.author}: {message.content}")
        prompt = message.content[9:].strip()

        anwser = chat_bot.get_response(prompt=prompt, user=user)

        logger.info(f'chatGPT model:{anwser["model"]}, total_tokens: {anwser["tokens"]}, reply: "{anwser["reply"]}", finish_reason: {anwser["finish_reason"]}')

        await message.reply(anwser['reply'])


    ## making an image
    elif message.content.startswith('!image'):

        wait_time = image_bot.get_wait_time(user=user)

        if wait_time > 0:
            await message.reply(f"a bit too fast, please wait {wait_time} seconds")

        else:
            await message.reply("Generating, please wait...")

            logger.info(f"{message.channel} - {message.author}: {message.content}")        
            prompt = message.content[7:].strip()
            img_path = image_bot.get_image(prompt=prompt, user=user)
            
            image_bot.delete_old(user)

            await channel.send(file=discord.File(img_path))#message.reply(file=discord.File(img_path))

    ## pollen rapport
    elif message.content.startswith('!pollen'):

        try:
            answer = pollen_bot.get_message()

        except Exception as e:
            logger.error("Something went wrong getting pollen data")
            answer = 'Something went wrong getting pollen data. Punch Mazrim to fix it'

        await channel.send(answer)


client.run(DISCORD_TOKEN)



