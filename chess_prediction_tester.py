import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
import random
import chess
import chess.engine
from stockfish import Stockfish
import math
import os.path

stockfishPath = "/Users/Manoj/Documents/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2"
engine = chess.engine.SimpleEngine.popen_uci(stockfishPath)
boardSize = 8
normalizeMax = 50
for fileNumber in range(50):
    file_path = 'chess_data/chess_scores_' + str(fileNumber) + '.txt'
    if(os.path.isfile(file_path) == False):
        continue
    else:
        print("STARTING FILE NUMBER ", fileNumber)
    board = chess.Board()
    allData = []
    allLabels = []
    lineCount = 0
    with open(file_path, 'r') as the_file:
        for line in the_file:
            splitted = line.split("|")
            if(len(splitted) < 3):
                continue
            #print("Number - ", splitted[0], " , Board - ", splitted[1], " , Score - ", splitted[2])
            board = chess.Board(splitted[1])
            #print(board)
            row = []
            for rowIndex in range(boardSize):
                col = []
                for colIndex  in range(boardSize):
                    pieceAt = board.piece_at(rowIndex * boardSize + colIndex)
                    if(pieceAt == None):
                        squareColor = 1 if ((rowIndex % 2 != 0) and (colIndex % 2 != 0)) or ((rowIndex % 2 == 0) and (colIndex % 2 == 0)) else 2
                        col.append([0, 0, squareColor]) #piece type, color of the piece, color of the square
                    if(pieceAt != None):
                        pieceType = pieceAt.piece_type
                        pieceColor = 0
                        if(pieceAt.color == True):
                            pieceColor = 1
                        elif(pieceAt.color == False):
                            pieceColor = 2
                        #board.sq
                        squareColor = 1 if ((rowIndex % 2 != 0) and (colIndex % 2 != 0)) or ((rowIndex % 2 == 0) and (colIndex % 2 == 0)) else 2
                        col.append([pieceType, pieceColor, squareColor]) #piece type, color of the piece, color of the square
                    #print("row - ", rowIndex, ", col -", colIndex, ", ", rowIndex * boardSize + colIndex, " type - ", pieceType, ", color - ", pieceColor)
                row.append(col)
            allData.append(row)
            allLabels.append([int(splitted[2])]) #score
            lineCount += 1
            #if(lineCount > 10000):
            #    break

    min = 9999
    max = -9999
    for label in allLabels:
        if(label[0] < min and label[0] != -9999):
            min = label[0]
        if(label[0] > max and label[0] != 9999):
            max = label[0]
    print(min)
    print(max)
    #print(allLabels)
    print("Applying stuff...")
    for i in range(len(allLabels)):
        #allLabels[i][0] = (allLabels[i][0]-min)/(max-min)
        if(allLabels[i][0] < 0):
            if(allLabels[i][0] <= -9999):
                allLabels[i][0] = 0
            else:
                #print("HEHEHE ", i, " ", allLabels[i][0], "  ", min, "  ", normalizeMax * allLabels[i][0]/min)
                allLabels[i][0] = int((math.log(-allLabels[i][0])/math.log(-min)) * normalizeMax)
        elif(allLabels[i][0] > 0):
            if(allLabels[i][0] >= 9999):
                allLabels[i][0] = (2 * normalizeMax)
            else:
                allLabels[i][0] = int(((math.log(allLabels[i][0])/math.log(max)) * normalizeMax) + normalizeMax)
            if(allLabels[i][0] >= (2 * normalizeMax)):
                allLabels[i][0] = (2 * normalizeMax) - 1
    #print(allLabels)
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

    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath="model_checkpoints/model_cp.ckpt",
                                                    save_weights_only=True,
                                                    verbose=1)
    model = models.Sequential()

    model.add(layers.Conv2D(boardSize, (3, 3), activation='relu', input_shape=(boardSize, boardSize, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(boardSize * 2, (2, 2), activation='relu'))
    #model.add(layers.MaxPooling2D((2, 2)))
    #model.add(layers.Conv2D(boardSize * 2, (1, 1), activation='relu'))

    model.add(layers.Flatten())
    model.add(layers.Dense(normalizeMax * 4, activation='relu'))
    model.add(layers.Dense(normalizeMax * 2))

    model.summary()

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
                #metrics=['mean_squared_logarithmic_error'])
    if(os.path.isfile('model_checkpoints/model_cp.ckpt.index') == True):
        model.load_weights("model_checkpoints/model_cp.ckpt")
    else:
        print("MODEL NOT FOUND MODEL NOT FOUND MODEL NOT FOUND")
        #exit()
#    history = model.fit(trainData, trainLabels, epochs=10, 
#                        validation_data=(testData, testLabels),
#                        callbacks=[cp_callback])

#    test_loss, test_acc = model.evaluate(testData,  testLabels, verbose=2)
#    print(test_acc)

#    model.save("model")

    print("\nPredictions...")
    testIndicesLoss = []
    predictionSize = 10
    for i in range(len(testLabels)):
        if(testLabels[i][0] < normalizeMax):
            testIndicesLoss.append(i)
        if(len(testIndicesLoss) > predictionSize):
            break
        i += 10
    for index in testIndicesLoss:
        prediction = model.predict(testData[index:index+1])
        print("Losses - ",  trainLabels[index] , " - ", np.argmax(prediction))

    testIndicesWin = []
    for i in range(len(testLabels)):
        if(testLabels[i][0] > normalizeMax):
            testIndicesWin.append(i)
        if(len(testIndicesWin) > predictionSize):
            break
        i += 10
    for index in testIndicesWin:
        prediction = model.predict(testData[index:index+1])
        print("Wins - ",  trainLabels[index] , " - ", np.argmax(prediction))

    testIndicesRandom = random.choices(range(len(testData)), k = predictionSize)
    for index in testIndicesRandom * 2:
        prediction = model.predict(testData[index:index+1])
        print("Random - ",  trainLabels[index] , " - ", np.argmax(prediction))
    ##print(prediction)

engine.close()
exit()

