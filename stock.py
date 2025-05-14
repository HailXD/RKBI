import numpy as np
import requests
from io import BytesIO
from PIL import Image

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def process_image(img):
    img_array = np.array(img)

    lower_bound = np.array([230, 220, 120])
    upper_bound = np.array([255, 255, 160])

    height, _, _ = img_array.shape

    first_yellow_row = -1
    last_yellow_row = -1
    for i in range(height):
        first_pixel = img_array[i, 0]
        last_pixel = img_array[i, -1]
        if (np.all(first_pixel >= lower_bound) and np.all(first_pixel <= upper_bound)) or \
           (np.all(last_pixel >= lower_bound) and np.all(last_pixel <= upper_bound)):
            if first_yellow_row == -1:
                first_yellow_row = i
            last_yellow_row = i

    color_above_first_yellow_row = [24,25,30]

    for i in range(first_yellow_row - 2, last_yellow_row + 3):
        img_array[i] = color_above_first_yellow_row

    result_img = Image.fromarray(img_array)
    return result_img

image_url = "https://cdn.discordapp.com/attachments/1352311755682091111/1372250245307564274/IMG_1490.png?ex=68261721&is=6824c5a1&hm=8e5a3fcbdf14b689538ff1464a7f4a3e714cec19940466c80cf28dfa7967461a&"
img = load_image_from_url(image_url)
processed_img = process_image(img)

processed_img.show()
processed_img.save("processed_image.png", format="PNG")
