import json
import os
from pathlib import Path

def yoink_necessary_images():
     folder_dir = "./Data"
     labels_f = ".\\labels"
     images_f = ".\\images"
     for file_name in os.listdir(folder_dir):
          label_name = "/" + Path(file_name).stem + ".txt"
          label_path = labels_f + label_name
          if(os.path.isfile(label_path)):
               print("copy .\\Data\\" + file_name + " " + images_f)
               os.system("copy .\\Data\\" + file_name + " " + images_f) 



def map_label_to_id(label):
    if(label=="Single Space Parking Meter"):
         return 0
    elif(label=="Multi Space Parking Meter"):
         return 1
    elif(label=="2 Hour Parking"):
         return 2
    elif(label=="No Parking Between"):
         return 3
    return -1

def map_id_to_label(id):
    if(id==0):
         return "Single Space Parking Meter"
    elif(id==1):
         return "Multi Space Parking Meter"
    elif(id==2):
         return  "2 Hour Parking"
    elif(id==3):
         return "No Parking Between"
    return -1

def retrieve_bounding_data(image):
    bounding_data = []
    label_object = image.get("Label")
    for obj in label_object.get("objects"):
         object_id = map_label_to_id(obj.get("title"))
         object_center_x_normal = (obj.get("bbox").get("left") + obj.get("bbox").get("width") * .5) / 640.0
         object_center_y_normal = (obj.get("bbox").get("top") - obj.get("bbox").get("height") * .5) / 640.0
         object_width_normal = obj.get("bbox").get("width") / 640.0
         object_height_normal = obj.get("bbox").get("height") / 640.0
         bounding_data.append((object_id, object_center_x_normal, object_center_y_normal, object_width_normal, object_height_normal))
    return bounding_data
 
# Opening JSON file
f = open('data.json')

data = json.load(f)

for i in data:
    # we need the following information
    image_name = Path(i.get("External ID")).stem + ".txt"
    image_data = retrieve_bounding_data(i)
    if(len(image_data)):
     f = open("./labels/" + image_name, "w")
     for row in image_data:
          string_to_write = str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3]) + ' ' + str(row[4]) +'\n'
          f.write(string_to_write)
     f.close()
 
# Closing file
f.close()

yoink_necessary_images()
    