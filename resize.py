from PIL import Image
from resizeimage import resizeimage

with open('Logos/logo_transparent.png', 'r+b') as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_width(image, 36)
        cover = resizeimage.resize_height(image, 36)
        cover.save('Logos/brand.png', image.format)