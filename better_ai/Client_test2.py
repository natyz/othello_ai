import random, time

import core
from OthelloStrategy import *
obj = core.myCore()
myGame = OthelloStrategy()
board = myGame.initial_board()
print(myGame.print_board(board))
compPlay = [WHITE, BLACK]
strategyPlay = BLACK
randomPlay = WHITE
player = WHITE
count = 0
tie = 0
win = 0
start = time.time()
while count != 10:
    if myGame.terminal(board)[0]:
        count+=1
        if myGame.terminal(board)[1] == 'Black':
            win+=1
        elif myGame.terminal(board)[1] == 'TIE':
            tie+=1
        board = myGame.initial_board()
    if myGame.any_legal_move(player, board):
        legal_moves = myGame.legal_moves(player, board)
        if player is randomPlay:
            #move = legal_moves[0]
            move = obj.random_move(player, board)
        if player is strategyPlay:
            move = myGame.minimax_strategy(board, player, 1)
            #print("black move:", move)
            #print (str(time.time()-start))
        if move != -1:
            board = myGame.make_move(move, player, board)
        else:   #if move is -1, skip a turn
            print (PLAYERS[player], "lose a turn.")
        player = myGame.opponent(player)
    elif myGame.any_legal_move(myGame.opponent(player), board):
        #print(PLAYERS[player], "has no legal move, lose a turn")
        player = myGame.opponent(player)
    else: break

print("winner is", myGame.terminal(board)[1])
theScore = myGame.score(BLACK, board)
# if theScore > 0: print ("Black won by", theScore)
# elif theScore < 0: print ("White won by", -theScore)
# else: print ("It's a TIE!")
print('time: ' + str(time.time()-start))
print(str(count))
print(str(win))
print(str(tie))

