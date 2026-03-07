from os import listdir
from os.path import isfile, join
# Importing Image class from PIL module
from PIL import Image
import os
import os.path
import shutil
import random

inputFolder = "images\\original"
inputFolder = r"C:\Users\Manoj\Documents\Stuff\pics"
outputResized = "images\\resized"
outputGrayscaled = "images\\grayscaled"

fileNumbers = []

allFilesCount = 10787
for index in range(allFilesCount):
    fileNumbers.append(index)

testDataSize = 1000


os.chdir(r"C:\Users\Manoj\Documents\Projects\MyProjects\MachineLearning\Keras\CnnImageColorize\images")

randomIndices = random.choices(fileNumbers, k = testDataSize)

print(randomIndices)
errors = 0
for index in range(allFilesCount):
    try:
        if(index in randomIndices):
            shutil.copy2("color_all\\resized_" + str(index) + ".jpg", "color_testdata")
            shutil.copy2("grayscaled_all\\grayscaled_" + str(index) + ".jpg", "grayscaled_testdata")
        else:
            shutil.copy2("color_all\\resized_" + str(index) + ".jpg", "color_traindata")
            shutil.copy2("grayscaled_all\\grayscaled_" + str(index) + ".jpg", "grayscaled_traindata")
        if(index % 100 == 0):
            print(index)
    except Exception as e: 
        errors += 1
        print(e)
        print("Total Errors - ", errors)
exit()
