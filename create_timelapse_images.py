import numpy as np
import dask.dataframe as dd
import cv2
import os

TIMESTAMP_MAX = 300589892
OFFSET_MS = 0
DELTA = 40000

ddf = dd.read_parquet('data\\data_split-coords', engine='pyarrow')
out_img_path = 'data\\images_timelapse'

if not os.path.exists(out_img_path):
    os.mkdir(out_img_path)

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

    cv2.imwrite(f'{out_img_path}\\{frame_no}.png', img)
    frame_no += 1