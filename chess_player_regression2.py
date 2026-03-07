import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
import random
import chess
import chess.engine
from stockfish import Stockfish
import math
import os.path
from collections import OrderedDict

boardSize = 8
normalizeMax = 50

def getArrayForBoard(board):
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
    return row

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
checkpointFolder = "model_regre_checkpoints_without_mates2"                
checkpoints = os.listdir(checkpointFolder)
print("Checkpoints - ", checkpoints)
if(len(checkpoints) > 0):
    print("LOADING CHECKPOINT LOADING CHECKPOINT LOADING CHECKPOINT")
    model.load_weights(checkpointFolder + "/cp.ckpt")
else:
    print("MODEL NOT FOUND MODEL NOT FOUND MODEL NOT FOUND")
    exit()

stockfishPath = "/Users/Manoj/Documents/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2"
engine = chess.engine.SimpleEngine.popen_uci(stockfishPath)
board = chess.Board()
while not board.is_game_over():
    print(board)
    if(board.turn == chess.BLACK):
        val = input("Enter your black move: ")
        if(val == "exit"):
            break
        board.push_uci(val)
        print("black moved - ")
        print(board)
        if(board.is_game_over()):
            break
    else:
        legal_moves = list(board.legal_moves)
        if(bool(legal_moves)):
            orderedMoves = {}
            for move in legal_moves:
                board.push(move)
                moveInput = getArrayForBoard(board)
                prediction = model.predict([moveInput])
                #print("Move - ", move, ", Prediction - ", prediction)
                orderedMoves[prediction[0][0]] = move
                board.pop()
            print("orderedMoves")
            for key in sorted(orderedMoves.keys()):
                print(key, " - ", orderedMoves[key])
            valBlack = input("Enter white's move: ")
            if(valBlack == "exit"):
                break
            board.push_uci(valBlack)
            print("white moved - ")
        if(board.is_game_over()):
            break

engine.quit()

