import os, signal, time, random
from multiprocessing import Process, Value
time_limit = 5
from OthelloCore import *

MAX = BLACK
MIN = WHITE
TIE = "TIE"
SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
class OthelloStrategy(OthelloCore):
    # def __init__(self):
    #     OthelloCore.__init__(self)
    def best_strategy(self, board, player, best_move, still_running):
        """
        :param board: a length 100 list representing the board state
        :param player: WHITE or BLACK
        :param best_move: shared multiptocessing.Value containing an int of
                the current best move
        :param still_running: shared multiprocessing.Value containing an int
                that is 0 iff the parent process intends to kill this process
        :return: best move as an int in [11,88] or possibly 0 for 'unknown'
        """
        while (still_running.value > 0 and best_move.value < 1000):
            time.sleep(1)
            best_move.value += 100
        def strategy(self, board, player):
            return self.minimax_strategy(self, board, player)
    def random_move(self, board, player):
        return random.choice(self.legal_moves(player,board))

    def minimax_strategy(self, board, player, m_depth=5):
        move = self.min_max(board, player, 0, m_depth)
        return move

    def terminal(self, board):
        """
        Test is the game board over, return False if not, else the winner/tie
        """
        win = self.winner(board)
        if win is not None: return True, win
        else: return False, None

    def winner(self, board):
        """
        return the winner of the winning board, or None if no winner
        """
        if self.any_legal_move(BLACK, board) or self.any_legal_move(WHITE,board):
            return None
        scoreBlack = self.score(BLACK, board)
        scoreWhite = self.score(WHITE, board)
        if scoreBlack > scoreWhite: return PLAYERS[BLACK]
        elif scoreBlack < scoreWhite: return PLAYERS[WHITE]
        else: return TIE

    def min_max(self, board, player, c_depth=0, m_depth=3):
        alpha = float('-inf')
        beta = float('inf')
        if player == BLACK:
            return self.min_DFS(board, player, alpha, beta, c_depth, m_depth)[1]
        else:
            return self.max_DFS(board, player, alpha, beta, c_depth, m_depth)[1]

    def max_DFS(self, board, player, alpha, beta, c_depth, m_depth):
        if self.terminal(board)[0]:
            return self.score(player, board), None
        if c_depth == m_depth:
            return self.score(player, board), None
        # terminal state where black gets to move 2+ times in a row
        v = float('-inf')
        move = -1
        for m in self.legal_moves(player, board):
            new_value = self.min_DFS(self.assign(m, player, board), self.opponent(player), alpha, beta, c_depth + 1, m_depth)[0]
            if new_value > v:
                if new_value >= beta: return new_value, m
                v = new_value
                move = m
                alpha = max(alpha, v)
        return v, move

    def min_DFS(self, board, player, alpha, beta, c_depth, m_depth):
        if self.terminal(board)[0]:
            return self.score(player, board), None
        if c_depth == m_depth:
            return self.score(player, board), None
        # terminal state where white moves 2+ times in a row
        v = float('inf')
        move = -1
        for m in self.legal_moves(player, board):
            new_value = self.max_DFS(self.assign(m, player, board), self.opponent(player), alpha, beta, c_depth + 1, m_depth)[0]
            if new_value < v:
                if new_value <= alpha: return new_value, m
                v = new_value
                move = m
                beta = min(beta, v)
        return v, move

    def assign(self, pos, player, board):
        copyBoard = board[:]
        copyBoard = self.make_move(pos, player, copyBoard)
        return copyBoard

    def eval(self, player, board):
        black_sum = opp_sum = 0
        for m in range(len(SQUARE_WEIGHTS)):
            if board[m] is BLACK:
                black_sum += SQUARE_WEIGHTS[m]
            elif board[m] is WHITE:
                opp_sum += SQUARE_WEIGHTS[m]
        return black_sum - opp_sum

    # def sort_weights(self):
