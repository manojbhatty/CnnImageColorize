import chess
import chess.engine
from stockfish import Stockfish
import random
import os.path
import os

stockfishPath = "/Users/Manoj/Documents/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2"

engine = chess.engine.SimpleEngine.popen_uci(stockfishPath)

turn = 0
index = 0

for fileNumber in range(50):
    file_path = 'chess_data_without_mates/chess_scores_' + str(fileNumber) + '.txt'
    if(os.path.isfile(file_path) == True):
        size = os.path.getsize(file_path) / (1024 * 1024)
        if(size > 2):
            print(file_path, " exists, Size - ", size, " . SKIPPING")
            continue
    for gameNumber in range(5):
        print("STARTING GAME ", gameNumber)
        board = chess.Board()
        infoBest = engine.analyse(board, chess.engine.Limit(time=0.1))
        while not board.is_game_over():
            legal_moves = list(board.legal_moves)
            if(bool(legal_moves)):
                if(board.turn == chess.WHITE):
                    for move in legal_moves:
                        bestScore = -99999
                        board.push(chess.Move.from_uci(str(move)))
                        info = engine.analyse(board, chess.engine.Limit(time=0.1))
                        if(info["score"].is_mate() == True):
                            print("Ive MATED")
                            #bestScore = 99999#info["score"].pov(chess.WHITE).mate()
                        elif(hasattr(info["score"], "mate") == True):
                            print("IM MATING")
                            #bestScore = 99999#info["score"].pov(chess.WHITE).mate()
                        else:#if(bestScore < info["score"].pov(chess.WHITE).cp):
                            bestScore = info["score"].pov(chess.WHITE).cp
                        index += 1
                        #print("Move ", index+1, ": ", str(move), " - Score:", info["score"], " cp = ", info["score"].pov(chess.WHITE).cp)
                        data = str(index) + "|" + board.fen() + "|" + str(bestScore)
                        if(bestScore != -99999):
                            if(index % 20 == 0):
                                print("File - ", fileNumber, ", Game number - ", gameNumber, " - ",  data)
                            with open(file_path, 'a') as the_file:
                                the_file.write(data + '\n')
                        else:
                            print("ZERO SCORE SKIPPED: ", data)
                        board.pop()
                        #print("Move white ", index+1, ": ", str(bestMove), " - Score:", bestScore, ", infoBest=", infoBest["score"])
                    board.push(chess.Move.from_uci(str(random.choice(legal_moves))))
                else:
                    board.push(chess.Move.from_uci(str(random.choice(legal_moves))))
                    #info2 = engine.analyse(board, chess.engine.Limit(time=0.1))
                    #print("Move black ", index+1, ": ", legal_moves[0], " - Score:", info2["score"])
                if(index % 3 == 0):
                    print(board)

#board.push(chess.Move.from_uci("e2e4"))
#board.push(chess.Move.from_uci("e7e6"))

#print(legal_moves)
#info = engine.analyse(board, chess.engine.Limit(time=0.1))
#print("Score:", info["score"])
#print("Info:", info)
print(board.piece_at(0))
print(board)

engine.close()
exit()