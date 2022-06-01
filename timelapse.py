import os
import cv2
from moviepy.editor import VideoFileClip
import re

fps = 60
video_path = 'output\\temp\\timelapse_original.mp4' 
source_images = 'data\\images_timelapse'

if not os.path.exists('output'):
    os.mkdir('output')

if not os.path.exists('output\\temp'):
    os.mkdir('output\\temp')

frame = cv2.imread(f'{source_images}\\0.png')
height, width, _ = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, fourcc, fps, (width,height))

def num_sort(string):
    return list(map(int, re.findall(r'\d+', string)))[0]

def create_timelapse(video, images_path):
    image_list = sorted([img for img in os.listdir(images_path)], key=num_sort)

    for image in image_list:      
        image_frame = cv2.imread(f'{images_path}\\{image}')
        video.write(image_frame) 
          
create_timelapse(video, source_images)

video.release()
cv2.destroyAllWindows()

clip = VideoFileClip(video_path)
clip.write_videofile('output\\timelapse_optimized.mp4')