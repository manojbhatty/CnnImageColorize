import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
import random

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()


print('train_images.shape ', train_images.shape)               
print('test_images.shape ', test_images.shape)               
print('train_labels.shape ', train_labels.shape)
print('test_labels.shape ', test_labels.shape)
print('len(train_labels) ', len(train_labels))
print('len(test_labels) ', len(test_labels))
print('--------------')
print('train_images.shape values - ', train_images[0].shape)               
print('train_labels.shape values - ', train_labels[0])               

boardSize = 8
totalRecordCount = 300000
trainDataCount = int(totalRecordCount * .8)
testDataCount = int(totalRecordCount * .2)
allData = []
zeroes = 0
total = 0
for dataSize in range(totalRecordCount):
    row = []
    for i in range(boardSize):
        col = []
        for j in range(boardSize):
            #col.append([float(i*j)/(boardSize*boardSize), random.random(), random.random()])
            #value = float((i+1)*(j+1)) + random.randint#+((boardSize+1)*(boardSize+1))
            value = random.randint(0, 63)
            col.append([value])
            total = total + 1
            if(value == 0):
                zeroes = zeroes + 1
            #col.append([.5])
        row.append(col)
    allData.append(row)
#print(allData)
allData = np.array(allData)
print("zeroes in training data - ", zeroes, " /", total)
print('allData.shape ', allData.shape)               

allLabels = []
zeroes = 0
for dataSize in range(totalRecordCount):
    average = 0
    for i in range(boardSize):
        #for j in range(boardSize):
            #average = (float(sum(allData[dataSize][i][j])))/len(allData[dataSize][i][j])
            #average = allData[dataSize][4][4][0]
        average = (float(sum(allData[dataSize][i])))/len(allData[dataSize][i])
    if(average == 1):
        zeroes = zeroes + 1
    allLabels.append([average])
#print(allLabels)
allLabels = np.array(allLabels)
print("zeroes in test data - ", zeroes)
print('allLabels.shape ', allLabels.shape)               

trainData = allData[0:trainDataCount]
trainLabels = allLabels[0:trainDataCount]
testData = allData[0:testDataCount]
testLabels = allLabels[0:testDataCount]

print('trainData.shape ', trainData.shape)               
print('trainLabels.shape ', trainLabels.shape)               
print('testData.shape ', testData.shape)               
print('testLabels.shape ', testLabels.shape)               

#exit()

# Normalize pixel values to be between 0 and 1
#train_images, test_images = train_images / 255.0, test_images / 255.0
trainData, testData = trainData / float(boardSize * boardSize), testData / float(boardSize * boardSize)
#trainLabels, testLabels = trainLabels / float(boardSize * boardSize), testLabels / float(boardSize * boardSize)


model = models.Sequential()
model.add(layers.Conv2D(boardSize, (3, 3), activation='relu', input_shape=(boardSize, boardSize, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(boardSize * 2, (2, 2), activation='relu'))
#model.add(layers.MaxPooling2D((2, 2)))
#model.add(layers.Conv2D(boardSize * 2, (1, 1), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(boardSize * 2, activation='relu'))
model.add(layers.Dense(boardSize * boardSize))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(trainData, trainLabels, epochs=10, 
                    validation_data=(testData, testLabels))

test_loss, test_acc = model.evaluate(testData,  testLabels, verbose=2)

print(test_acc)

print("\nPredictions...")
for index in range(64):
    prediction = model.predict(testData[index:index+1])
    print( trainLabels[index] , " - ", np.argmax(prediction))
##print(prediction)