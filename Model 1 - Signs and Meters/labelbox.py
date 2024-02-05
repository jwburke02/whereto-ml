import json
import os
from pathlib import Path

def yoink_necessary_images():
     folder_dir = "../Data Collection"
     labels_f = "./labels"
     images_f = "./images"
     for file_name in os.listdir(folder_dir):
          label_name = "/" + Path(file_name).stem + ".txt"
          label_path = labels_f + label_name
          if(os.path.isfile(label_path)):
               os.system("cp ../Data\ Collection/" + file_name + " " + images_f) 



def map_label_to_id(label):
    if(label=="Residential Permit Sign"):
         return 0
    elif(label=="Tow Zone - No Stopping"):
         return 1
    elif(label=="Tow Zone - No Parking"):
         return 1
    elif(label=="Street Cleaning"):
         return 2
    elif(label=="Handicapped Parking"):
         return 3
    elif(label=="Parking Meter"):
         return 4
    elif(label=="2 Hour Parking"):
         return 5
    return -1

def map_id_to_label(id):
    if(id==0):
         return "Residential Permit Sign"
    elif(id==1):
         return "Tow Zone - No Parking"
    elif(id==2):
         return "Street Cleaning"
    elif(id==3):
         return "Handicapped Parking"
    elif(id==4):
         return "Parking Meter"
    elif(id==5):
         return "2 Hour Parking"
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
    