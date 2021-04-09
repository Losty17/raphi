import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

def image1test(image, text):
    response = requests.get(f'{image}')
    img = Image.open(BytesIO(response.content))
    font = ImageFont.truetype('./media/Lazer84.ttf', 80)
    escrever = ImageDraw.Draw(img)
    escrever.text(
        xy=(100,100),
        text=f'{text}',
        fill=(100, 140, 80),
        font=font
    )
    return img.save('./media/img.png')

if __name__ == "__main__":
    img = image1test('./media/filo.png', 'Teste')
    img.show()