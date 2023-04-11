# 2D Hand Animation

import numpy as np

from cv2 import bitwise_and
from cv2 import bitwise_not
from cv2 import add

import color as u8

colors = [u8.red, u8.green, u8.blue, u8.yellow, u8.purple]

# Mask Is The Best Way !
def a_3d2d_Finger_arrayMask_Generator(index, image_height_width):
    # 1 Mask of finger
    l = image_height_width[0] // 2

    if index != 0:
        # If not thumb
        # y : 1/8 of image -> 7/8 of image
        d = l // 2
        y0 = d // 2
        y1 = y0 + d
        y2 = y0 + d + d
        y3 = y0 + d + d + d
    else:
        # If is thumb
        # y : 1/2 of image -> 7/8 of image
        d = l // 4
        y0 = l
        y1 = y0 + d
        y2 = y0 + d + d
        y3 = y0 + d + d + d        

    # x
    w1 = int(image_height_width[1] / 8 / 2)
    w2 = int(image_height_width[1] / 7 / 2)
    w3 = int(image_height_width[1] / 6 / 2)
    x = int(image_height_width[1]*(index*2+2) / 12)
    mask = np.zeros(image_height_width, dtype=np.uint8)
    mask[y0:y1, x-w1:x+w1] = 255
    mask[y1:y2, x-w2:x+w2] = 255
    mask[y2:y3, x-w3:x+w3] = 255

    # 1.1 drawing location
    points = [[x, y0], [x, y1], [x, y2], [x, y3]]
    return points, mask
def apply_mask(index, image_height_width, color_image, mask):
    # 2 logical not
    mask_inv = bitwise_not(mask)
    color_image = bitwise_and(color_image, color_image, mask_inv)

    # 3 full a background with single color
    finger_color = colors[index]
    background = np.full(
        (image_height_width[0], 
        image_height_width[1], 
        3), 
        
        finger_color, 
        dtype = np.uint8)
    # 4 mask background with mask
    image1 = bitwise_and(background, background, mask = mask)
    # 5 add "original image" with "color finger image"
    color_image = add(color_image, image1)

    return color_image