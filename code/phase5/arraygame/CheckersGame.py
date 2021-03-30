from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .CheckersLogic import Board
import numpy as np
import copy

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
        return b
        #return np.array(b.pieces)
 
    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)
 
    def getActionSize(self):
        # return number of actions
        return 256
 
    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b = copy.copy(board)
        b.execute_move(action, player)
        self.display(b)
        return (b.pieces, -player)
 
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b = copy.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)
 
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        
        b = Board(self.n)
        b = copy.copy(board)
        
        result = b.get_game_result(player)        
        
        return result
 
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board
 
    def getSymmetries(self, board, pi):
        # mirror, rotational
        return
 
    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s


    @staticmethod
    def display(board):
        #display 
        n = len(board.pieces)
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                print(CheckersGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")


""" x = Board(8)
asd = CheckersGame()
asd.display(x)
print("Legal moves on board : ", x.get_legal_moves(1))
#x1, t1 = asd.getNextState(x, 1, 225)  # Sola ye
#x1, t1 = asd.getNextState(x, 1, 165)  # Sağa ye
x1, t1 = asd.getNextState(x, 1, 34)
 """