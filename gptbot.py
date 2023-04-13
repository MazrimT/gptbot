import os
import discord
import openai
from dotenv import load_dotenv
from logger.logger import Logger

logger = Logger()

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Configure the ChatGPT API client
openai.api_key = OPENAI_API_KEY

# intents 
intents = discord.Intents.default()
intents.message_content = True
# Set up the Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    # don't react to own messages
    if message.author == client.user:
        return

    #if message.content.startswith('hello'):
    logger.info(f"{message.channel} - {message.author}: {message.content}")

    if message.content.startswith('!chatgpt'):
        prompt = message.content[9:].strip()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",#"text-davinci-003",
            messages=[
                {"role": "system", "content": "you are a 1700's pirate"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            #temperature=0.5,
            #top_p=1,
            #frequency_penalty=0,
            #presence_penalty=0
        )
        chatgpt_reply = response['choices'][0]['message']['content']
        finish_reason = response['choices'][0]['finish_reason']

        logger.info(f'chatGPT model:{response["model"]}, total_tokens: {response["usage"]["total_tokens"]}, reply: "{chatgpt_reply}", finish_reason: {finish_reason}')

        await message.reply(chatgpt_reply)

client.run(DISCORD_TOKEN)