### Generate markers
import cv2
from cv2 import aruco
import os

### --- parameter --- ###

# Save location
dir_mark = os.getcwd()

# Parameter
num_mark = 20 #Number of markers
size_mark = 500 #Size of markers

### --- marker images are generated and saved --- ###
# Call marker type
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)

for count in range(num_mark) :

    id_mark = count
    img_mark = aruco.drawMarker(dict_aruco, id_mark, size_mark)

    if count < 10 :
        img_name_mark = 'mark_id_0' + str(count) + '.jpg'
    else :
        img_name_mark = 'mark_id_' + str(count) + '.jpg'
    path_mark = os.path.join(os.path.join(os.getcwd(), "aruco/markers",img_name_mark))

    cv2.imwrite(path_mark, img_mark)
    print('saving marker', path_mark)

#%%
# print(os.path.join(os.getcwd(), "markers","img.png"))