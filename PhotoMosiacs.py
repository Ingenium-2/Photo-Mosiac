# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 09:55:26 2020                 @author: vishal
"""
size = 5 # 5 gives a bit more accurate , 10 gives a bit more pixelated 

def get_mean(img):
    r = b = g = total = 0
    for row in img:
        for pixel in row:
           r += pixel[2]
           g += pixel[1]
           b += pixel[0]
           
           total += 1
    return (b/total, g/total, r/total)

def get_square(pixel, corner, size):
    opposite = [corner[0]+size, corner[1]+size]
    square = pixel[corner[0]:opposite[0], corner[1]:opposite[1]]
    return square
def color_difference(p1, p2):
    tot = 0
    for c1, c2 in zip(p1, p2):
        tot += (c1-c2)**2
    dist = tot ** 0.5
    return dist
def pythogoras_theorem(target_rgb, mean_image_rgbs):
    match_dist = None
    match_img = None
    for image, rgbs in mean_image_rgbs:
       dis = color_difference(target_rgb, rgbs)
       if match_dist is None or dis < match_dist:
           match_img = image
           match_dist = dis
    return match_img

import cv2
import numpy as np
import os
path = '.\\source_images'
mean_image_rgbs = []
for image in os.listdir(path):
    if image.endswith(".jpg") or image.endswith(".png"):
        full = os.path.join(path, image)
        img = cv2.imread(full)
        img = cv2.resize(img, (size,size))
        mean = get_mean(img)
    mean_image_rgbs.append((img, mean))
        

img = cv2.imread('Messi.jpg')

pixel_img = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
mosiac = np.zeros((img.shape[0], img.shape[1], img.shape[2]), np.uint8)
for x in range(0, img.shape[1], size):
    for y in range(0, img.shape[0], size):
        x1 = y1 = size
        square = get_square(img, (y, x), size)
        target_rgb = get_mean(square)
        pic = pythogoras_theorem(target_rgb, mean_image_rgbs)
        if img.shape[1] - x <size:
            x1 = img.shape[1] - x
        if img.shape[0] - y <size:
            y1 = img.shape[0] - y
        pic = cv2.resize(pic, (x1, y1))
        mosiac[y:y+size, x:x+size] = pic
        pixel_img[y:y+size, x:x+size] = target_rgb


cv2.imshow('img', img)
cv2.imshow('pixel', pixel_img)
cv2.imshow('mosiac', mosiac)
cv2.waitKey(0)
cv2.destroyAllWindows()