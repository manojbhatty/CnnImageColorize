import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
import random
import math
import os.path
from os import listdir
from os.path import isfile, join
from PIL import Image

np.seterr(divide = 'ignore') 
boardSize = 100
normalizeMax = 50

allFileNumbers = []
for fileNumber in range(30):
    allFileNumbers.append(fileNumber)
index = 0
os.chdir("/Users/Manoj/Documents/Projects/MyProjects/MachineLearning/Keras/CnnImageColorize")
allData = []
allLabels = []
while True and index <= 50:
    index += 1
#for fileNumber in range(50):
    fileNumber = random.choice(allFileNumbers)
    file_path1 = 'Grayscaled/resized_' + str(fileNumber) + '.jpg'
    file_path2 = 'Resized/resized_' + str(fileNumber) + '.jpg'
    if(os.path.isfile(file_path1) == False):
        print("FILE NUMBER Does not exist", file_path1)
        continue
    elif(os.path.isfile(file_path2) == False):
        print("FILE NUMBER Does not exist", file_path2)
        continue
    else:
        print("STARTING FILE NUMBER ", file_path1)
    lineCount = 0
    image1 = Image.open(file_path1).convert('RGB')
    pix1 = image1.load()
    image2 = Image.open(file_path2).convert('RGB')
    pix2 = image2.load()
    width, height = image1.size
    row1 = []
    row2 = []
    for rowIndex in range(width):
        col1 = []
        col2 = []
        for colIndex in range(height):
            col1.append(pix1[rowIndex, colIndex])
            col2.append(pix2[rowIndex, colIndex])
            #(r, g, b) = pix2[rowIndex, colIndex]
            #print("row - ", rowIndex, ", col -", colIndex, ", ", pix2[rowIndex, colIndex])
            #print("row - ", rowIndex, ", col -", colIndex, ", ", r1, ", ", g1, ", ", b1)
        row1.append(col1)
        row2.append(col2)
    allData.append(row1)
    allLabels.append(row2)
    lineCount += 1
    #if(lineCount > 10000):
    #    break
    #exit()
totalRecordCount = len(allData)
trainDataCount = int(totalRecordCount * .8)
testDataCount = int(totalRecordCount * .2)
#print(allData)
allData = np.array(allData)
print('allData.shape ', allData.shape)    
allLabels = np.array(allLabels)
print('allLabels.shape ', allLabels.shape)   

trainData = allData[0:trainDataCount]
trainLabels = allLabels[0:trainDataCount]
testData = allData[0:testDataCount]
testLabels = allLabels[0:testDataCount]

print('trainData.shape ', trainData.shape)               
print('trainLabels.shape ', trainLabels.shape)               
print('testData.shape ', testData.shape)               
print('testLabels.shape ', testLabels.shape)   

checkpointFolder = "model"
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpointFolder + "/cp.ckpt", save_weights_only=True, verbose=1)
model = models.Sequential()

model.add(layers.Conv2D(boardSize, (2, 2), activation='relu', padding="same", input_shape=(boardSize, boardSize, 3)))
#model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(boardSize * 2, (3, 3), activation='relu', padding="same"))
#model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(boardSize * 4, (3, 3), activation='relu', padding="same"))

#model.add(layers.Flatten())
#model.add(layers.Dense(normalizeMax, activation='relu'))
model.add(layers.Dense(units=3, activation='linear'))

model.summary()

model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=[tf.keras.metrics.MeanSquaredError()])
            #metrics=['mean_squared_logarithmic_error'])
checkpoints = os.listdir(checkpointFolder)
print("Checkpoints - ", checkpoints)
if(len(checkpoints) > 0):
    print("LOADING CHECKPOINT LOADING CHECKPOINT LOADING CHECKPOINT")
    model.load_weights(checkpointFolder + "/cp.ckpt")
else:
    print("MODEL NOT FOUND MODEL NOT FOUND MODEL NOT FOUND")
    #exit()
history = model.fit(trainData, trainLabels, epochs=10, validation_data=(testData, testLabels), callbacks=[cp_callback])

#test_loss, test_acc = model.evaluate(testData,  testLabels, verbose=2)
#print(test_acc)

model.save("model")

print("\nPredictions...")
testIndices = []
predictionSize = 10
for i in range(len(testLabels)):
    testIndices.append(i)
    if(len(testIndices) > predictionSize):
        break
    i += 1
for index in testIndices:
    prediction = model.predict(testData[index:index+1])
    print('prediction.shape ', prediction[0].shape)   
    #IMIR = prediction[0].reshape(boardSize, boardSize)  #For dense unit 1
    #imgP = Image.fromarray(IMIR).convert('RGB')#For dense unit 1
    random_array = prediction[0].astype(np.uint8)  #For dense unit 3
    imgP = Image.fromarray(random_array)#.convert('RGB')
    imgP.save("prediction/" + str(index) + "_colorized.jpg")
    #imgP = Image.fromarray(random_array).convert('RGB')
    #imgP.save(str(index) + "_rgb.jpg")

    #temp = testData[index:index+1]
    #temp = temp[0].astype(np.uint8)  #For dense unit 3    
    #print(temp.shape)
    #imgP = Image.fromarray(temp)
    #imgP.save("prediction/" + str(index) + "_original.jpg")

    temp = testLabels[index:index+1]
    temp = temp[0].astype(np.uint8)  #For dense unit 3    
    print(temp.shape)
    imgP = Image.fromarray(temp)
    imgP.save("prediction/" + str(index) + "_original_color.jpg")
exit()

