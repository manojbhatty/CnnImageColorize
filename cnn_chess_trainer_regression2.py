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

allFileNumbers = []
for fileNumber in range(101):
    allFileNumbers.append(fileNumber)
index = 0
os.chdir("/Users/Manoj/Documents/Projects/MyProjects/MachineLearning/Keras/CnnChess")
while True:# and index == 0:
    #index += 1
#for fileNumber in range(101):
    fileNumber = random.choice(allFileNumbers)
    file_path = 'chess_data_without_mates/chess_scores_' + str(fileNumber) + '.txt'
    if(os.path.isfile(file_path) == False):
        print("FILE NUMBER Does not exist", fileNumber)
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

    checkpointFolder = "model_regre_checkpoints_without_mates2"
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpointFolder + "/cp.ckpt",
                                                    save_weights_only=True,
                                                    verbose=1)
    model = models.Sequential()

    model.add(layers.Conv2D(boardSize * boardSize, (8, 8), activation='relu', padding="same", input_shape=(boardSize, boardSize, 3)))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))
    
    model.add(layers.Conv2D(boardSize * boardSize, (7, 7), activation='relu', padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))
    
    model.add(layers.Conv2D(boardSize * boardSize, (5, 5), activation='relu', padding="same"))
    model.add(layers.BatchNormalization())
    #model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))
    
    model.add(layers.Conv2D(boardSize * boardSize, (3, 3), activation='relu', padding="same"))
    model.add(layers.BatchNormalization())
    #model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))

    model.add(layers.Conv2D(boardSize * boardSize, (3, 3), activation='relu', padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.25))

    model.add(layers.Flatten())
    model.add(layers.Dense(normalizeMax, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(units=1, activation='linear'))

    model.summary()

    model.compile(optimizer='adam',
                loss=tf.keras.losses.mean_absolute_error,#.losses.mean_squared_error,
                metrics=['mean_absolute_error'])
                #metrics=['mean_squared_logarithmic_error'])
    checkpoints = os.listdir(checkpointFolder)
    print("Checkpoints - ", checkpoints)
    if(len(checkpoints) > 0):
        print("LOADING CHECKPOINT LOADING CHECKPOINT LOADING CHECKPOINT")
        model.load_weights(checkpointFolder + "/cp.ckpt")
    else:
        print("MODEL NOT FOUND MODEL NOT FOUND MODEL NOT FOUND")
        exit()
    history = model.fit(trainData, trainLabels, epochs=50, 
                        validation_data=(testData, testLabels),
                        callbacks=[cp_callback])

    test_loss, test_acc = model.evaluate(testData,  testLabels, verbose=2)
    print(test_acc)

    model.save("model")

    print("\nPredictions...")
    testIndicesLoss = []
    predictionSize = 10
    for i in range(len(testLabels)):
        if(testLabels[i][0] < 0):
            testIndicesLoss.append(i)
        if(len(testIndicesLoss) > predictionSize):
            break
        i += 10
    for index in testIndicesLoss:
        prediction = model.predict(testData[index:index+1])
        print("Losses - ",  trainLabels[index] , " - ", prediction)

    testIndicesWin = []
    for i in range(len(testLabels)):
        if(testLabels[i][0] >= 0):
            testIndicesWin.append(i)
        if(len(testIndicesWin) > predictionSize):
            break
        i += 10
    for index in testIndicesWin:
        prediction = model.predict(testData[index:index+1])
        print("Wins - ",  trainLabels[index] , " - ",prediction)

    testIndicesRandom = random.choices(range(len(testData)), k = predictionSize)
    for index in testIndicesRandom * 2:
        prediction = model.predict(testData[index:index+1])
        print("Random - ",  trainLabels[index] , " - ", prediction)
    ##print(prediction)

engine.close()
exit()

