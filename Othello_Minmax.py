"""
Base class for Othello Core
Must be subclassed by student Othello solutions
"""

#
from OthelloCore import *
import random, copy
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
MAX = BLACK
MIN = WHITE
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}


# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

class Othello_MinMax(OthelloStudent):
    # def __init__(self):
    #     OthelloStudent.__init__(self)

    def random_move(list):
        return random.choice(list)

    def human(self):
        return int(raw_input("Enter index from list above: "))

    def minimax_strategy(self, m_depth=3):
        def strategy(board, player):
            v, move = min_max(board, player, 0, m_depth)
            return move

        return strategy
    def smart_move(self, player, legal_moves, board):
        best_move = None
        score = float("-inf")
        copy_board = copy.copy(board)
        for move in legal_moves:
            new_board = self.make_move(move, player, copy_board)
            if self.score(player, new_board) > score:
                score = self.score(player, new_board)
                best_move = move
            copy_board = copy.copy(board)
        print("best move: " + str(best_move))
        return best_move

    def min_max(self, board, player, c_depth=0, m_depth=3):
        if player == BLACK:
            #print("return: " + str(self.min_DFS(board, player, c_depth, m_depth)[1]))
            return self.min_DFS(board, player, c_depth, m_depth)[1]
        else:
            #print("return: " + str(self.max_DFS(board, player, c_depth, m_depth)[1]))
            return self.max_DFS(board, player, c_depth, m_depth)[1]

    def winner(self, board):
        if self.any_legal_move(BLACK, board) or self.any_legal_move(WHITE, board):
            return False
        return True

    def max_DFS(self, board, player, c_depth, m_depth):
        if self.winner(board)==True:
            return self.score(player, board), board
        if c_depth == m_depth:
            return self.eval(player, board)
        v = float('-inf')
        move = -1
        for m in self.legal_moves(player, board):
            new_value = self.min_DFS(self.assign(m, player, board), self.opponent(player), c_depth + 1, m_depth)[0]
            if new_value > v:
                v = new_value
                move = m
                if new_value == float('inf'):
                    break
        return v, move

    def min_DFS(self, board, player, c_depth, m_depth):
        if self.winner(board)==True:
            return self.score(player, board), board
        if c_depth == m_depth:
            return self.score(board), board
        v = float('inf')
        move = -1
        for m in self.legal_moves(player, board):
            print("player", player, "m", m)
            new_value = self.max_DFS(self.assign(m, player, board), self.opponent(player), c_depth + 1, m_depth)[0]
            if new_value < v:
                v = new_value
                move = m
                if new_value == float('-inf'):
                    break
        return v, move
    def assign(self, move, player, board):
        copy_board = board[:]
        copy_board[move] = self.make_move(move, player, copy_board)
        return copy_board

    def eval(self, player, board):
        return self.score(player, board)
