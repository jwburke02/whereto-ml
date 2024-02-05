import os
from pathlib import Path
import random

'''
This file will take (relative to the file) images as well as labels and turn them
into seperate sets of different probability, placing them in a preorganized
data_root folder
'''

images_folder = "./images"
labels_folder = "./labels"
for image_name in os.listdir(images_folder):
    label = labels_folder + "/" + Path(image_name).stem + ".txt"
    image = images_folder + "/" + image_name
    r_val = random.uniform(0, 1)
    if r_val < .85:
        os.system("cp " + label + " ./data_root/train/labels") 
        os.system("cp " + image + " ./data_root/train/images") 
    elif r_val < .95:
        os.system("cp " + label + " ./data_root/valid/labels") 
        os.system("cp " + image + " ./data_root/valid/images") 
    elif r_val < 1:
        os.system("cp " + label + " ./data_root/test/labels") 
        os.system("cp " + image + " ./data_root/test/images") 
