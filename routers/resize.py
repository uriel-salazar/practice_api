from PIL import Image
from io import BytesIO

def image_resize_800(file):
    i = Image.open(BytesIO(file))
    
    i = i.resize((800, 800))
    return i
   
    