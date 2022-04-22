import os
import cv2
import numpy as np

OFFSET = 0

NUM_SINGLE = 2972
NUM_DOUBLE = 2723
NUM_QUADRO = 3168

max_range = NUM_SINGLE + NUM_DOUBLE + NUM_QUADRO
stitched_images_path = '..\\data\\images\\stitched'

if not os.path.exists(stitched_images_path):
    os.mkdir(stitched_images_path)

single_images_0_list = sorted([img for img in os.listdir('..\\data\\images\\images_single')])
double_images_0_list = sorted([img for img in os.listdir('..\\data\\images\\images_double\\0')])
double_images_1_list = sorted([img for img in os.listdir('..\\data\\images\\images_double\\1')])
quadro_images_0_list = sorted([img for img in os.listdir('..\\data\\images\\images_quadro\\0')])
quadro_images_1_list = sorted([img for img in os.listdir('..\\data\\images\\images_quadro\\1')])
quadro_images_2_list = sorted([img for img in os.listdir('..\\data\\images\\images_quadro\\2')])
quadro_images_3_list = sorted([img for img in os.listdir('..\\data\\images\\images_quadro\\3')])

def stitch_images(i):
    if i < NUM_SINGLE:
        image = cv2.imread(os.path.join('..\\data\\images\\images_single', single_images_0_list[i]))
        image = np.concatenate((image, 255*np.ones(image.shape, dtype=np.uint8)), axis=0)
        image = np.concatenate((image, 255*np.ones(image.shape, dtype=np.uint8)), axis=1)
        cv2.imwrite(f'{stitched_images_path}\\{i}.png', image)
    elif i < NUM_SINGLE + NUM_DOUBLE:
        image_0 = cv2.imread(os.path.join('..\\data\\images\\images_double\\0', double_images_0_list[i - NUM_SINGLE]))
        image_1 = cv2.imread(os.path.join('..\\data\\images\\images_double\\1', double_images_1_list[i - NUM_SINGLE]))
        image = np.concatenate((image_0, image_1), axis=1)
        image = np.concatenate((image, 255*np.ones(image.shape, dtype=np.uint8)), axis=0)
        cv2.imwrite(f'{stitched_images_path}\\{i}.png', image)
    elif i < NUM_SINGLE + NUM_DOUBLE + NUM_QUADRO:
        image_0 = cv2.imread(os.path.join('..\\data\\images\\images_quadro\\0', quadro_images_0_list[i - NUM_SINGLE - NUM_DOUBLE]))
        image_1 = cv2.imread(os.path.join('..\\data\\images\\images_quadro\\1', quadro_images_1_list[i - NUM_SINGLE - NUM_DOUBLE]))
        image_2 = cv2.imread(os.path.join('..\\data\\images\\images_quadro\\2', quadro_images_2_list[i - NUM_SINGLE - NUM_DOUBLE]))
        image_3 = cv2.imread(os.path.join('..\\data\\images\\images_quadro\\3', quadro_images_3_list[i - NUM_SINGLE - NUM_DOUBLE]))
        image_top = np.concatenate((image_0, image_1), axis=1)
        image_bottom = np.concatenate((image_2, image_3), axis=1)
        image = np.concatenate((image_top, image_bottom), axis=0)
        cv2.imwrite(f'{stitched_images_path}\\{i}.png', image)

for i in range(OFFSET, max_range):
    stitch_images(i)
    if i % 100 == 0:
        print(f'Stitching {i} of {max_range}...')

print('Stitching done.\n')
