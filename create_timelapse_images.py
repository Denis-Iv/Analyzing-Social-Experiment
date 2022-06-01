import numpy as np
import dask.dataframe as dd
import cv2
import os

TIMESTAMP_MAX = 300589892
OFFSET_MS = 0
DELTA = 40000

def images_difference(images):
    mask = np.zeros((images[0].shape[0], images[0].shape[1]), dtype=np.uint8)
    prev = images[0]

    for i in range(1, len(images)):
        mask = cv2.bitwise_or(mask, image_difference_mask(prev, images[i]))
        prev = images[i]

    return map_by_layer(images[-1], lambda x: x // 3, np.logical_not(mask))

def image_difference_mask(prev, curr):
    difference = cv2.subtract(prev, curr)
    b, g, r = cv2.split(difference)
    (_, mask) = cv2.threshold(cv2.bitwise_or(b, cv2.bitwise_or(g, r)), 1, 255, cv2.THRESH_BINARY)

    return mask

def map_by_layer(image, f, mask):
    mask_3d = np.zeros((mask.shape[0], mask.shape[1], 3))

    mask_3d[:, :, 0] = mask
    mask_3d[:, :, 1] = mask
    mask_3d[:, :, 2] = mask

    return np.where(mask_3d, f(image), image)

def image_difference(prev, curr):
    mask = image_difference_mask(prev, curr)

    return cv2.bitwise_and(curr, curr, mask=mask)

ddf = dd.read_parquet('data\\data_split-coords', engine='pyarrow')
out_raw_path = 'data\\images\\timelapse_raw'
out_masked_path = 'data\\images\\timelapse_masked'

if not os.path.exists('data\\images'):
    os.mkdir('data\\images')

if not os.path.exists(out_raw_path):
    os.mkdir(out_raw_path)

if not os.path.exists(out_masked_path):
    os.mkdir(out_masked_path)

colors_dict = {
    0: (0, 0, 0),     
    1: (111, 117, 0),  
    2: (170, 158, 0), 
    3: (104, 163, 0),  
    4: (120, 204, 0),  
    5: (192, 204, 0),  
    6: (164, 80, 36),  
    7: (234, 144, 54),
    8: (193, 58, 73), 
    9: (82, 82, 81),  
    10: (244, 233, 81),
    11: (255, 92, 106), 
    12: (26, 0, 109),   
    13: (47, 72, 109),  
    14: (86, 237, 126), 
    15: (159, 30, 129), 
    16: (144, 141, 137),
    17: (255, 179, 148),
    18: (38, 105, 156), 
    19: (192, 74, 180), 
    20: (57, 0, 190),   
    21: (217, 215, 212),
    22: (127, 16, 222),
    23: (255, 171, 228),
    24: (129, 56, 255), 
    25: (0, 69, 255),  
    26: (170, 153, 255),
    27: (0, 168, 255),  
    28: (112, 180, 255),
    29: (53, 214, 255), 
    30: (184, 248, 255),
    31: (255, 255, 255),
}

img = np.full((2000, 2000, 3), 255, dtype=np.uint8)
row_iterator = ddf.itertuples()
row = next(row_iterator)

frame_no = 0
next_img = []
for ms in range(OFFSET_MS, TIMESTAMP_MAX, DELTA):
    while row.timestamp <= ms:
        img[row.y, row.x] = colors_dict[row.pixel_color]
        try:
            row = next(row_iterator)
        except StopIteration:
            break

    cv2.imwrite(f'{out_raw_path}\\{frame_no}.png', img)

    next_img.append(img)

    if len(next_img) == 5:        
        masked_img = images_difference(next_img)
        cv2.imwrite(f'{out_masked_path}\\{frame_no}.png', masked_img)
        del next_img[0]

    frame_no += 1