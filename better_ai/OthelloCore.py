"""
Base class for Othello Core
Must be subclassed by student Othello solutions
"""

#
import random
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
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
# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

class OthelloCore:
    def squares(self):
        """List all the valid squares on the board."""
        return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


    def initial_board(self):
        """Create a new board with the initial black and white positions filled."""
        board = [OUTER] * 100
        for i in self.squares():
            board[i] = EMPTY
        # The middle four squares should hold the initial piece positions.
        board[44], board[45] = WHITE, BLACK
        board[54], board[55] = BLACK, WHITE
        return board


    def print_board(self,board):
        """Get a string representation of the board."""
        rep = ''
        rep += '  %s\n' % ' '.join(map(str, list(range(1, 9))))
        for row in range(1, 9):
            begin, end = 10 * row + 1, 10 * row + 9
            rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
        return rep


    def is_valid(self, move):
        """Is move a square on the board?"""
        if (self.squares().count(move) > 0):
            return True
        return False

    def opponent(self, player):
        """Get player's opponent piece."""
        if player is WHITE: return BLACK
        return WHITE

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found

        Logic: start with "square", go to the next square in the direction
        if it is opposite, go to the next square, and mark found one opposite
        if it is player, return the index
        else (i.e. either it is player or it hits border, return None
        """
        found = False
        nextS = square + direction
        while board[nextS] is self.opponent(player):
            found = True
            nextS += direction
        if found and board[nextS] is player: return nextS
        return None

    def is_legal2(self, move, player, board):
        """Is this a legal move for the player?"""
        # """
        # Without using find_bracket: for all directions, move to direction, if opponent, keep going
        # if the last one is player return true; otherwise try another direction. Return false in the end
        # """
        for d in DIRECTIONS:
            s = move
            moved = False
            while self.is_valid(s+d) and board[s+d] is self.opponent(player):
                s += d
                moved = True
            if self.is_valid(s+d) and board[s+d] is player and moved: return True
        return False

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        for d in DIRECTIONS:
            if self.find_bracket(move,player,board,d) != None: return True
        return False

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player.
        Logic: change move to player. Go through all directions and make flips
        """
        board[move]=player
        for d in DIRECTIONS:
            board = self.make_flips(move,player,board,d)
        return board

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player.
        Logic: Start with move, step at direction,
            if opponent, add to brac_list; keep moving
            if player: flip all brac_list pieces to player
            else: do nothing
        """
        brac_list = []
        nextS = move + direction
        while board[nextS] is self.opponent(player):
            brac_list.append(nextS)
            nextS += direction
        if len(brac_list) > 0:
            if board[nextS] is player:
                for p in brac_list: board[p] = player
        return board


    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        moves = []
        for s in self.squares():
            if board[s] is EMPTY and self.is_legal(s, player, board): moves.append(s)
        random.shuffle(moves)
        return moves



    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        return len(self.legal_moves(player, board)) > 0

    def next_player(self,board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if self.any_legal_move(board.opponent(prev_player), board):
            return self.opponent(prev_player)
        elif self.any_legal_move(prev_player, board):
            return prev_player
        return None

    def score(self,player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        score = 0
        opponent = self.opponent(player)
        for s in self.squares():
            if board[s] is player: score += 1
            if board[s] is opponent: score -= 1
        return score

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)




