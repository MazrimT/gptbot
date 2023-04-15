import openai
import requests
from pathlib import Path
from datetime import datetime

class imageBot(object):

    def __init__(self, api_key):

        self.openai = openai
        self.openai.api_key = api_key
        self.image_path = Path(__file__).parent.parent.joinpath("images").resolve()
        self.wait_time = 30


    def get_image(self, prompt, user, size=1024):
        
        response = self.openai.Image.create(
            prompt=prompt,
            n=1,
            size=f"{size}x{size}",
            user=user,
        )

        url = response["data"][0]["url"]
        r = requests.get(url, allow_redirects=True)
        file_name = prompt.replace(' ', '_')[:230].lower()
        ts = datetime.now().strftime('%Y%m%d%H%M%S')

        img_path = Path(f"{self.image_path}/{ts}_{user}_{file_name}.png").resolve()
        with open(img_path, 'wb') as f:
            f.write(r.content)

        return img_path

    def get_wait_time(self, user):
        images = self.image_path.glob(f"*_{user}_*.png")
        if images:
            latest = max([int(i.stem[:14]) for i in images])
            time_to_wait = latest + self.wait_time - int(datetime.now().strftime('%Y%m%d%H%M%S'))            
        else:
            time_to_wait = 0

        return time_to_wait


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    image_bot = imageBot(api_key=api_key)
    image = image_bot.get_image(prompt='lalala', user='mazrim')
    print(image)
