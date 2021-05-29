from __future__ import print_function
import copy
import numpy as np
from .CheckersLogic import Board
from Game import Game
import sys
sys.path.append('..')


class CheckersGame(Game):

    square_content = {
        -3: "B",
        -1: "b",
        +0: "-",
        +1: "w",
        +3: "W"
    }

    def __init__(self, n=8):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return 512 # 256 

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.getActionSize():
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.execute_move(action, player)
        return (b.pieces, -player)

        # return a fixed size binary vector
    def getValidMoves(self, board, player):
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        """ if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids) """
        for i in legalMoves:
            valids[i] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1

        b = Board()
        b.pieces = board
        result = b.get_game_result(player)

        return result

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        b = np.copy(board)
        if player == 1:
            return b
        else:
            b *= player
            rotate_1 = list(zip(*b[::-1]))
            rotate_2 = list(zip(*rotate_1[::-1]))
            return np.asarray(rotate_2)

    def getSymmetries(self, board, pi):
        # mirror, rotational
        return [(board, pi)]#, (self.getCanonicalForm(board, -1), pi[::-1])]

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square]
                          for row in board for square in row)
        return board_s

    @staticmethod
    def display(board):
        # display
        n = len(board)
        print("\n   ", end="")
        print("a b c d e f g h", end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y+1, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                print(CheckersGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")
