import os
#import discord
import openai
from dotenv import load_dotenv
from logger.logger import Logger
import requests
from pathlib import Path
from datetime import datetime

base_path = Path(__file__).parent

logger = Logger()

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

#prompt = "the cover picture of a scientific thesis about LA-MRSA"
prompt = "a normal and realistic looking human"

response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
)

url = response["data"][0]["url"]
r = requests.get(url, allow_redirects=True)
file_name = prompt.replace(' ', '_')[:230]
ts = datetime.now().strftime('%Y%m%d%H%M%S')

with open(f"{base_path}/images/{ts}_{file_name}.png", 'wb') as f:
    f.write(r.content)

logger.info(f"prompt: '{prompt}', url: {response['data'][0]['url']}")
