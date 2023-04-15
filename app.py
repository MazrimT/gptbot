import os
from pathlib import Path
import discord
from dotenv import load_dotenv
from datetime import datetime

from ai.chat import chatBot
from ai.image import imageBot
from logger.logger import Logger


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
logger = Logger()


chat_bot = chatBot(api_key=OPENAI_API_KEY)
image_bot = imageBot(api_key=OPENAI_API_KEY)

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

    # talking to chatgpt
    elif message.content.startswith('!chatgpt'):
        logger.info(f"{message.channel} - {message.author}: {message.content}")
        prompt = message.content[9:].strip()
        
        user = str(message.author).split("#")[0].lower()
        anwser = chat_bot.get_response(prompt=prompt, user=user)

        logger.info(f'chatGPT model:{anwser["model"]}, total_tokens: {anwser["tokens"]}, reply: "{anwser["reply"]}", finish_reason: {anwser["finish_reason"]}')

        await message.reply(anwser['reply'])

    ## making an image
    elif message.content.startswith('!image'):

        user = str(message.author).split("#")[0].lower()
        wait_time = image_bot.get_wait_time(user=user)

        if wait_time > 0:
            await message.reply(f"a bit too fast, please wait {wait_time} seconds")

        else:
            await message.reply("Generating, please wait...")

            logger.info(f"{message.channel} - {message.author}: {message.content}")        
            prompt = message.content[7:].strip()
            img_path = image_bot.get_image(prompt=prompt, user=user)

            await message.reply(file=discord.File(img_path))



client.run(DISCORD_TOKEN)



