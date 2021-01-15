from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .CheckersLogic import Board
import numpy as np

class CheckersGame(Game):
    
    square_content = {
        3:"O",          # Beyaz Dama Taşları
        1:"o",          # Beyaz Pawn Taşları
        0:"-",          # Boş Square
        -1:"x",         # Siyah Pawn Taşları
        -3:"X"          # Siyah Dama Taşları
    }
    
    @staticmethod
    def getSquarePiece(piece):
        return CheckersGame.square_content[piece]
 
    def __init__(self, n):
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
        return self.n * self.n * self.n
 
    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n * self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)
 
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        
 
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        # Beyaz dama yapma yerine ilk ulaştı
        if 1 in pieces[0]:
            return 1
        # Siyah dama yapma yerine ilk ulaştı
        if -1 in pieces[self.n-1]:
            return -1
        # Oyun devam ediyor
        return 0
 
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board
 
    def getSymmetries(self, board, pi):
        # mirror, rotational
 
    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    @staticmethod
    def display(board):
        #display
        board.display()