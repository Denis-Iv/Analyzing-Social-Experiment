import os
import cv2
from moviepy.editor import VideoFileClip
import re

if not os.path.exists('output'):
    os.mkdir('output')

if not os.path.exists('output\\temp'):
    os.mkdir('output\\temp')

def num_sort(string):
    return list(map(int, re.findall(r'\d+', string)))[0]

video_path = 'output\\temp\\timelapse_original.mp4' 
source_images_path = 'data\\images_timelapse'

# Приготвяне на VideoWriter
fps = 60
frame = cv2.imread(f'{source_images_path}\\0.png')
height, width, _ = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, fourcc, fps, (width,height))

# Зареждане на изображенията
image_list = sorted([img for img in os.listdir(source_images_path)], key=num_sort)

# Създаване на видеото
for image in image_list:      
    image_frame = cv2.imread(f'{source_images_path}\\{image}')
    video.write(image_frame) 

video.release()
cv2.destroyAllWindows()

clip = VideoFileClip(video_path)
clip.write_videofile('output\\timelapse_optimized.mp4')