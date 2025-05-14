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

    lower_bound = np.array([75, 75, 0])
    upper_bound = np.array([255, 255, 140])

    height, _, _ = img_array.shape
    rows_deleted = 0
    rows_to_delete = []

    for i in range(height):
        first_pixel = img_array[i, 0]
        last_pixel = img_array[i, -1]

        if (np.all(first_pixel >= lower_bound) and np.all(first_pixel <= upper_bound)) or \
           (np.all(last_pixel >= lower_bound) and np.all(last_pixel <= upper_bound)):
            rows_to_delete.append(i)

    img_array = np.delete(img_array, rows_to_delete, axis=0)
    rows_deleted = len(rows_to_delete)

    start_row = int(0.7 * img_array.shape[0])
    consecutive_row_color = None

    for i in range(start_row, height - 1):
        if np.array_equal(img_array[i, 0], img_array[i + 1, 0]):
            consecutive_row_color = img_array[i, 0]
            break

    insert_row = 607
    img_array = np.insert(img_array, insert_row, [171, 170, 175], axis=0)

    for _ in range(8):
        img_array = np.insert(img_array, insert_row + 1, [24, 25, 30], axis=0)

    img_array = np.insert(img_array, insert_row + 9, [70, 71, 77], axis=0)

    img_array = np.delete(img_array, slice(start_row + 1, start_row + 11), axis=0)

    for i in range(rows_deleted):
        img_array = np.insert(img_array, start_row + i, consecutive_row_color, axis=0)

    result_img = Image.fromarray(img_array)
    return result_img


image_url = "https://cdn.discordapp.com/attachments/1352311755682091111/1372248573240021022/IMG_1489.png?ex=68261593&is=6824c413&hm=59996942ff469693536152dc6e51eb2a6d24778027d63ec252d2bffaa11444d7&"
img = load_image_from_url(image_url)
processed_img = process_image(img)

processed_img.show()
processed_img.save("processed_image.png", format="PNG")
