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
        # return np.array(b.pieces)

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
        #b.__dict__.update(board.__dict__)
        b.pieces = np.copy(board)
        b.execute_move(action, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        #b.__dict__.update(board.__dict__)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        #setattr(board, 'capture', b.capture)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
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

    # TODO This method is not called anymore !?
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        #b = Board()
        #x = copy.copy(board)
        #b.__dict__.update(board.__dict__)
        """ self.display(board) """
        """ x.pieces = [[j*player for j in i] for i in board] """
        """ self.display(x) """
        return board * player

    def getSymmetries(self, board, pi):
        # mirror, rotational
        return [(board, pi), (board[:, ::-1], pi[::-1])]

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
