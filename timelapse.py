import os
from datetime import datetime 
import cv2
import re

FPS = 60

now = datetime.now().strftime('%d%H%M')
video_path = f'output\\temp\\timelapse_original.mp4' 
source_images = 'data\\images_from_points'

if not os.path.exists('output'):
    os.mkdir('output')

frame = cv2.imread(f'{source_images}\\0.png')
height, width, _ = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, fourcc, FPS, (width,height))

def num_sort(string):
    return list(map(int, re.findall(r'\d+', string)))[0]

def create_timelapse(video, images_path):
    image_list = sorted([img for img in os.listdir(images_path)], key=num_sort)

    for image in image_list:      
        image_frame = cv2.imread(f'{images_path}\\{image}')
        video.write(image_frame) 
          
create_timelapse(video, source_images)

video.write_videofile(video_path)
cv2.destroyAllWindows()