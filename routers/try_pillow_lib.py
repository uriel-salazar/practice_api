
import requests
h = { 'User-Agent': 'Neo'}
r = requests.get("https://cdn.pixabay.com/blog/content/soultrain-moscow-8183118.jpg", headers=h)

from PIL import Image
from io import BytesIO

image= Image.open(BytesIO(r.content))

width, height = image.size
print(width, height)
i = image.resize((800,800))
print(i)