import chess
import chess.engine
from stockfish import Stockfish
import random

stockfishPath = "/Users/Manoj/Documents/stockfish_13_win_x64_bmi2/stockfish_13_win_x64_bmi2"

engine = chess.engine.SimpleEngine.popen_uci(stockfishPath)
board = chess.Board()

turn = 0
index = 0
infoBest = engine.analyse(board, chess.engine.Limit(time=0.1))
while not board.is_game_over():
    legal_moves = list(board.legal_moves)
    if(bool(legal_moves)):
        if(board.turn == chess.WHITE):
            bestScore = -9999
            bestMove = ""
            for move in legal_moves:
                board.push(chess.Move.from_uci(str(move)))
                info = engine.analyse(board, chess.engine.Limit(time=0.1))
                #if(info["score"].relative.score() == None):
                if(info["score"].is_mate() == True):
                    #if(True or bestScore < info["score"].pov(chess.WHITE).mate()):
                        print("Ive MATED")
                        bestScore = 9999#info["score"].pov(chess.WHITE).mate()
                        bestMove = move
                        infoBest = info
                        board.pop()
                        break
                elif(hasattr(info["score"], "mate") == True):
                    #if(True or bestScore < info["score"].pov(chess.WHITE).mate()):
                        print("IM MATING")
                        bestScore = 9999#info["score"].pov(chess.WHITE).mate()
                        bestMove = move
                        infoBest = info
                        board.pop()
                        break
                elif(bestScore < info["score"].pov(chess.WHITE).cp):
                    bestScore = info["score"].pov(chess.WHITE).cp
                    bestMove = move
                    infoBest = info
                index += 1
                #print("Move ", index+1, ": ", str(move), " - Score:", info["score"], " cp = ", info["score"].pov(chess.WHITE).cp)
                board.pop()
            print("Move white ", index+1, ": ", str(bestMove), " - Score:", bestScore, ", infoBest=", infoBest["score"])
            board.push(chess.Move.from_uci(str(bestMove)))
        else:
             board.push(chess.Move.from_uci(str(random.choice(legal_moves))))
             info2 = engine.analyse(board, chess.engine.Limit(time=0.1))
             print("Move black ", index+1, ": ", legal_moves[0], " - Score:", info2["score"])
        if(index % 2 == 0):
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