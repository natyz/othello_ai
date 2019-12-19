import random, time
from Othello_Strategy import *

my_game = Othello_MinMax()
board = my_game.initial_board()
player = WHITE
comp = BLACK
comp_win = 0
count = 0
start = time.time()
while(True):
    #print('BLACK SCORE: ' + str(my_game.score(BLACK, board)))
    #print('WHITE SCORE: ' + str(my_game.score(WHITE, board)))
    if my_game.any_legal_move(BLACK, board) is False and my_game.any_legal_move(WHITE, board) is False:
        print(my_game.print_board(board))
        if my_game.score(BLACK, board) > my_game.score(WHITE, board):
            print "BLACK WINS"
            comp_win+=1
        else:
            print "WHITE WINS"
        print("GAME END")
        count += 1
        board = my_game.initial_board()
    #print(my_game.print_board(board))
    legal_moves = my_game.legal_moves(player, board)
    if len(legal_moves)!=0:
        #print(player + " legal moves: "+ str(legal_moves))
        if player is BLACK:
            move = my_game.min_max(board, player)
        elif player is WHITE:
            move = random_move(legal_moves)
        board = my_game.make_move(move, player, board)
        #print(my_game.print_board(board))
    player = my_game.opponent(player)
    if count==1:
        print("comp wins: " + str(comp_win))
        print(str(time.time()-start))
        break