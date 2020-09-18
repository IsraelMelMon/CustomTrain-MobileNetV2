#new_autocsvplusyamls

import csv
#from os import listdir
#from os.path import isfile, join
import yaml
import argparse
import os
import sys

parser = argparse.ArgumentParser(description= \
    'Path to the directory where all the categories are.')
parser.add_argument("--path", type=str, \
    help='path to the directory where all categories exist',\
         default='/content/drive/My Drive/CustomTrain-MobileNetV2/classes/')
parser.add_argument("--epochs", type=int, \
    help='number of epochs for training', default=50)
parser.add_argument("--learningR", help='learning rate', default=0.0001)
parser.add_argument("--BS", type=int, help='batch size', default=2)
parser.add_argument("--MN", type=str, help='output model filename without .h5', \
    default="mbnv2")

#parse the arguments
args = parser.parse_args()
mypath =  args.path
e = args.epochs
lr = args.learningR
bs = args.BS
mn= args.MN

# Get directory paths
names1 = [x[1] for x in os.walk(mypath) ]
#print(names1)
# delete null lists, get classes list
classes = [x for x in names1 if x != []][0]

#extracts all image names from all categories
names = [x[2] for x in os.walk(mypath) ]
del names[0]
# cleans the previous so just the images names remain
names_clean = [names[x][i] for x in range(len(names)) for i in range(len(names[x])) 
if names[x][i] != ".DS_Store"]

#print(names_clean)

#if the image name contains the category the binary row is created
new_column=[]

for x in classes: 
    new_set =[]
    for i in names_clean:
        
        if x in i:
            new_set.append(1)
            #print(1)
        else:
            new_set.append(0)
            #print(0) 
    new_column.append(new_set)

# insert csv columns headers
new_column.insert(0, names_clean)
classes2 = classes
classes2.insert(0,'name')
classes2 = [classes2]
#print(classes2)
# make columns rows
rows = zip(*new_column)

#check if folder for config files exists (to not create another one)
if not os.path.exists('config_files'):
    os.makedirs('config_files')

#writes csv
with open('config_files/data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(classes2)
    for row in rows:
        writer.writerow(row)
# writes yaml config file
dict_config = {'input_shape':'[null, null, 3]', 'resize_shape': '[224, 224]', \
    'images_base_path':"'"+mypath+"'", \
        'targets':str(classes[1:]),'image_name_col':"'name'"}
text_file = open("config_files/data_config.yaml", "w")
for k,v in dict_config.items():
  # write line to output file
    text_file.write(k+": "+ v)
    text_file.write("\n")
text_file.close()

#writes training configuraton yaml
dict_training = {'use_augmentation': 'true', 'batch_size': str(bs),'epochs': str(e), \
    'initial_learning_rate': str(lr),'model_path': "'"+mn+".h5'"}

text_file = open("config_files/training_config.yaml", "w")
for k,v in dict_training.items():
  # write line to output file
    text_file.write(k+": "+ v)
    text_file.write("\n")
text_file.close()

# writes prediction configuration yaml
dict_predict = {'resize_shape': '[224, 224]','targets': str(classes[1:]), \
    'model_path':"'"+mn+".h5'"}
text_file = open("config_files/predictor_config.yaml", "w")
for k,v in dict_predict.items():
  # write line to output file
    text_file.write(k+": "+ v)
    text_file.write("\n")
text_file.close()
