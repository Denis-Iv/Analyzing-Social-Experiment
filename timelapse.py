import os
import cv2
from datetime import datetime 
import re

FRAME_TO_USE = 6 # 1 - no skip, 2 - use every second frame, 3 - use every third frame, etc
FPS = 15

NUM_SINGLE = 2972
NUM_DOUBLE = 2723
NUM_QUADRO = 3168

max_range = NUM_SINGLE + NUM_DOUBLE + NUM_QUADRO
now = datetime.now().strftime('%d%H%M')
video_path =f'output\\TL-{FPS}-{FRAME_TO_USE}-{now}.mp4' 
stitched_images_path = 'data\\images\\stitched'

if not os.path.exists('output'):
    os.mkdir('output')

frame = cv2.imread(f'{stitched_images_path}\\0.png')
height, width, _ = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_path, fourcc, FPS, (width,height))

def num_sort(string):
    return list(map(int, re.findall(r'\d+', string)))[0]

def create_timelapse(video, images_path):
    image_list = sorted([img for img in os.listdir(images_path)], key=num_sort)

    i = 0
    for image in image_list:
        if FRAME_TO_USE < 2 or i % FRAME_TO_USE == 0:
            image_frame = cv2.imread(f'{images_path}\\{image}')
            video.write(image_frame)                    
            if i % 100 == 0:
                print(f'Creating timelapse {int(i/FRAME_TO_USE)} of {int(max_range/FRAME_TO_USE)}...')
        i+=1

    print(f'Timelapse completed.')
          
create_timelapse(video, stitched_images_path)

video.release()
cv2.destroyAllWindows()