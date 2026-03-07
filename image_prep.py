from os import listdir
from os.path import isfile, join
# Importing Image class from PIL module
from PIL import Image
import os
import os.path

inputFolder = "images\\original"
inputFolder = r"C:\Users\Manoj\Documents\Stuff\pics"
outputResized = "images\\resized"
outputGrayscaled = "images\\grayscaled"

onlyfiles = []

for dirpath, dirnames, filenames in os.walk(inputFolder):
    print(dirpath)
    print(dirnames)
    for filename in [f for f in filenames if f.endswith(".jpg")]:
        #print(os.path.join(dirpath, filename))
        onlyfiles.append(os.path.join(dirpath, filename))
        #print(len(onlyfiles))

#for file in onlyfiles:
    #print(file)
print(len(onlyfiles))
#exit()

#onlyfiles = [f for f in listdir('TestImage') if isfile(join('TestImage', f))]
#print(onlyfiles)

count = 0
errors = 0
for file in onlyfiles:
    try:
        im = Image.open(file)
        width, height = im.size
        left = 4
        top = height / 5
        right = 154
        bottom = 3 * height / 5
        newsize = (100, 100)
        im1 = im.resize(newsize)
        im1.save(outputResized + "\\resized_" + str(count) + ".jpg")
        img2 = im1.convert('L')
        img2.save(outputGrayscaled + "\\grayscaled_" + str(count) + ".jpg")
    except Exception as e: 
        errors += 1
        print(e)
        print("Total Errors - ", errors)
    finally:
        count = count + 1
        if(count % 50 == 0):
            print("Count - ", count)
