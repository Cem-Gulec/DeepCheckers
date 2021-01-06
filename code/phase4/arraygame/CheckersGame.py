from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .CheckersLogic import Board
import numpy as np

class CheckersGame(Game):
    
    @staticmethod
    def getSquarePiece(piece):
 
    def __init__(self, n):
 
    def getInitBoard(self):
        # return initial board (numpy board)
 
    def getBoardSize(self):
        # (a,b) tuple
 
    def getActionSize(self):
        # return number of actions
 
    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
 
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
 
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
 
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
 
    def getSymmetries(self, board, pi):
        # mirror, rotational
 
    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    @staticmethod
    def display(board):
        #display