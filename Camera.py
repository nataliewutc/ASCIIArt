from PIL import Image
from colorama import Fore, Style
import cv2

#Fix colour in command prompt, invert brightness

max_pixel_value = 255
ascii_char = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
vid = cv2.VideoCapture(0)

def get_image_data(im):
    img = Image.open(im)
    img.thumbnail((200,100))
    pixel_matrix = list(img.getdata())
    return [pixel_matrix[i:i+img.width] for i in range(0, len(pixel_matrix), img.width)]

def get_brightness_matrix(pixel_matrix,map_type = "average"):
    brightness_matrix = []
    for row in pixel_matrix:
        brightness_row = []
        for j in row:
            if map_type == "average":
                brightness = (j[0] + j[1] + j[2]) /3
            elif map_type == "lightness":
                brightness = ( max(j) + min(j) ) /2
            elif map_type == "luminosity":
                brightness =  0.21*j[0] + 0.72*j[1] + 0.07*j[2]
            brightness_row.append(brightness)
        brightness_matrix.append(brightness_row)
    return brightness_matrix


def resize_brightness_matrix(brightness_matrix):
    resized_matrix = []
    max_pixel = max(map(max, brightness_matrix))
    min_pixel = min(map(min, brightness_matrix))
    for row in brightness_matrix:
        rescaled_row = []
        for p in row:
            r = max_pixel_value * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        resized_matrix.append(rescaled_row)
    return resized_matrix


def brightness_to_ascii(brightness_matrix, ascii_char):
    ascii_matrix = []
    for row in brightness_matrix:
        ascii_row = []
        for r in row:
            character = int( r / (max_pixel_value / len(ascii_char)))
            ascii_row.append(ascii_char[character-1])
        ascii_matrix.append(ascii_row)
    return ascii_matrix

def print_ascii_matrix(ascii_matrix, text_colour = Fore.):
    for row in ascii_matrix:
        #line = [p+p+p for p in row]
        print(text_colour + "".join(row))
    print(Style.RESET_ALL)

while(True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    pixels = get_image_data(frame)
    brightness_matrix = get_brightness_matrix(pixels, "average")
    brightness_matrix = resize_brightness_matrix(brightness_matrix)
    brightness_matrix = brightness_to_ascii(brightness_matrix, ascii_char)
    frame = print_ascii_matrix(brightness_matrix, Fore.RED)
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
















