from os import listdir
from os.path import isfile, join
# Importing Image class from PIL module
from PIL import Image

onlyfiles = [f for f in listdir('TestImage') if isfile(join('TestImage', f))]
print(onlyfiles)

count = 1
for file in onlyfiles:
    # Opens a image in RGB mode
    im = Image.open("TestImage/" + file)
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
    # Setting the points for cropped image
    left = 4
    top = height / 5
    right = 154
    bottom = 3 * height / 5
    # Cropped image of above dimension
    # (It will not change original image)
    #im1 = im.crop((left, top, right, bottom))
    newsize = (100, 100)
    im1 = im.resize(newsize)
    # Shows the image in image viewer
    print("here")
    im1.save('Resized/resized_' + str(count) + ".jpg")
    #im1.show()
    img2 = im1.convert('L')
    img2.save('Grayscaled/resized_' + str(count) + ".jpg")
    count = count + 1
