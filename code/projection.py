import os
import sys
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt


def projection(img, focal_len):
    height, width, RGB = img.shape
    projection_result =  np.zeros(shape=img.shape, dtype=np.uint8)

    print("......projection......")

    for x in range(0, width):
        for y in range(0, height):
            x_offset = x - int(width/2)
            y_offset = y - int(height/2)
            new_x = focal_len*math.atan(x_offset/focal_len)
            new_y = focal_len*(y_offset/((x_offset**2+focal_len**2)**0.5))

            new_x = round(new_x + width/2)
            new_y = round(new_y + height/2)

            if (new_x >= 0) & (new_x < width) & (new_y >= 0) & (new_y < height):
                projection_result[new_y][new_x] = img[y][x]
    cv2.imwrite("projection_result.jpg",projection_result)
    _, thresh = cv2.threshold(cv2.cvtColor(projection_result, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY)
    x, y, w, h = cv2.boundingRect(thresh)

    return projection_result[y:y+h,x:x+w]