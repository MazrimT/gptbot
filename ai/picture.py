from picamera2 import Picamera2
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class pictureBot(object):

    def __init__(self):
        
        pass    
    
    def take_picture(self):
        
        t = datetime.now().strftime('%Y%m%d%H%M%S')
        picture_dir = Path(__file__).parent.parent.joinpath(f'images/picture')
        picture_path = picture_dir.joinpath(f'picture_{t}.png')
        font_path = Path(__file__).parent.parent.joinpath(f'resources/arial.ttf')
 
        print('setting up camera')
        picam2 = Picamera2()
        print('setup done')
        #picam2.start_and_capture_file(picture_path.as_posix(), delay=1, show_preview=False)
        
        camera_config = picam2.create_still_configuration()
        picam2.configure(camera_config)
        picam2.start()
        img = picam2.capture_image()
        picam2.close()

        # add text
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path.as_posix(), 100)
        #font = ImageFont.load_default()
        text_position = (0, 0)        # (x, y) tuple for where the text starts
        text_color = (255, 255, 255)    # RGB tuple
        draw.text(text_position, t, font=font, fill=text_color)

        img.save(picture_path.as_posix(), format='PNG')


        



        for file in picture_dir.glob('*.png'):
            if file != picture_path:
                file.unlink()

        return picture_path
    
if __name__ == '__main__':

    picture_bot = pictureBot()
    
    picture_path = picture_bot.take_picture()
    print(picture_path)
    