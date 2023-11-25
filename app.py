import os
from pathlib import Path
import discord
from dotenv import load_dotenv
from datetime import datetime

from ai.gpt import gptBot
from ai.image import imageBot
from ai.pollen import pollenBot
from ai.power import powerBot
from ai.picture import pictureBot
from logger.logger import Logger


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
logger = Logger()


gpt_bot = gptBot(api_key=OPENAI_API_KEY)
image_bot = imageBot(api_key=OPENAI_API_KEY)
pollen_bot = pollenBot() 
power_bot = powerBot()
picture_bot = pictureBot()

# discord intents 
intents = discord.Intents.default()
intents.message_content = True

# Set up the Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Connected to Discord!')




async def send_anwser(message: discord.Message, anwser: str, name:str='reply'):

    if str(message.channel.type) == 'public_thread':
        await message.channel.send(anwser)
        reply_to = message.channel
        
    else:
    #    thread = await message.create_thread(name=name)
        await message.channel.send(anwser)
        reply_to = message.channel
        
    return reply_to

@client.event
async def on_message(message: discord.Message):
    # don't react to own messages
    if message.author == client.user:
        return

    channel = client.get_channel(message.channel.id)
    channel_name = message.channel
    

    user = str(message.author).split("#")[0].lower()

    # hlep
    if message.content == '!hlep':
        
        anwser = """
        ```
        !gpt What is the sun?           - ask gpt a question
        !gptmode                        - see what "mode" gpt chat is running on
        !gptmode you are a robot        - set a new mode for gpt
        !image A thing                  - generate an image
        !pollen                         - get a pollen report for Stocholm
        !pollen list                    - lists cities that there is current pollen reports for
        !pollen Umeå                    - get a pollen report for another city
        !power                          - returns a power cost prognosis
        ```
        """
        await send_anwser(message, anwser)
        
    # chatgpt
    elif message.content.startswith('!gpt '):
        logger.info(f"{message.channel} - {message.author}: {message.content}")
        prompt = message.content[9:].strip()

        try:
            anwser = gpt_bot.get_response(prompt=prompt, user=user)

            logger.info(f'chatGPT model:{anwser["model"]}, total_tokens: {anwser["tokens"]}, reply: "{anwser["reply"]}", finish_reason: {anwser["finish_reason"]}')

        except Exception as e:
            logger.error(f"Could not get an anwser from GPT")
            logger.error(e)
            raise

        await send_anwser(message, anwser['reply'])

    # check what gpt mode is
    elif message.content == ('!gptmode'):
        await send_anwser(message, f'Current gpt mode: "{gpt_bot.system_prompt}". write !gptmode [new mode] to set new mode')        
        
    # change gpt mode
    elif message.content.startswith('!gptmode'):
        gpt_bot.system_prompt = message.content[8:].strip()
        await send_anwser(message, "Mode changed")
        
    # making an image
    elif message.content.startswith('!image '):

        wait_time = image_bot.get_wait_time(user=user)

        if wait_time > 0:
            anwser = f"a bit too fast, please wait {wait_time} seconds"

        else:
            thread = await send_anwser(message, "Generating, please wait...")

            logger.info(f"{message.channel} - {message.author}: {message.content}")        
            prompt = message.content[7:].strip()
            img_path = image_bot.get_image(prompt=prompt, user=user)
            
            image_bot.delete_old(user)

            await thread.send(file=discord.File(img_path))

    ## pollen rapport
    elif message.content == '!pollen':

        try:
            answer = pollen_bot.get_message()
        except Exception as e:
            logger.error("Something went wrong getting pollen data")
            answer = 'Something went wrong getting pollen data. Punch Mazrim to fix it'
            logger.error(e)

        await send_anwser(message, answer)

    # list cities with reports
    elif message.content == '!pollen list':
        
        cities = pollen_bot.list_cities()
        if cities:
            answer = "Cities with current reports: ```\n" + "\n".join(cities) + "```"
        else:
            answer = 'No current pollen reports'
            
        await send_anwser(message, answer)

    # pollen for other city
    elif message.content.startswith('!pollen '):
        city = message.content[7:].strip()
        
        try:
            answer = pollen_bot.get_message(city=city)

        except Exception as e:
            logger.error("Something went wrong getting pollen data")
            answer = 'Something went wrong getting pollen data. Punch Mazrim to fix it'
        
        await send_anwser(message, answer)        
        
    # get power prognosis
    elif message.content == ('!power'):
        
        thread = await send_anwser(message, "Checking power prognosis, please wait...")

        logger.info(f"{message.channel} - {message.author}: {message.content}")        

        power_bot.get_power()

        img_path = f"{Path(__file__).parent.joinpath('images/power')}/power.png"

        await thread.send(file=discord.File(img_path))
        
    # take a picture
    elif message.content == ('!picture'):
        
        thread = await send_anwser(message, "Taking a picture, please wait...")

        logger.info(f"{message.channel} - {message.author}: {message.content}")        

        picture_path = picture_bot.take_picture()

        await thread.send(file=discord.File(picture_path))
        
                    
client.run(DISCORD_TOKEN)



