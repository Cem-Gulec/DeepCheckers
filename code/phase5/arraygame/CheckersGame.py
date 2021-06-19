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
        # 10 bits total 
        # First bit dictates there is a multi-capture move
        # Second bit dictates there is a capture move
        # Thirdth and foruth bit dictates the direction of the move
        # Rest of the bits used to coordinates on the board
        return 1024

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        b.pieces = np.copy(board)

        # Çok tekrara düştü ancak hamle kalmadı, oyuncunun taşları siliniyor
        if action == -1:
            b.pieces[b.pieces > 0] = 0
            return (b.pieces, -player)

        b.execute_move(action, player)
        multi_capture_flag = (action >> 9) & 1
        return (b.pieces, player) if multi_capture_flag else (b.pieces, -player)

        # return a fixed size binary vector
    def getValidMoves(self, board, player):
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        
        legalMoves = b.get_legal_moves(player)
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
        new_pi = pi.copy()
        
        # Dikey simetriye uygun olarak, pi değerlerinin değişmesi gerekiyor
        non_zero = [i for i, e in enumerate(new_pi) if e != 0]
        for old_index in non_zero:
            bin_old = format(old_index, 'b').zfill(10)
            # İlk üç bitimiz yine aynı, multi_capture flag, capture_flag, direction[0]
            bin_new = bin_old[:3]
            # Sağ - sol hareketlerinde ise hareket yönüde değişmeli
            if bin_old[2] == '1':
                bin_new += '0' if bin_old[3] == '1' else '1'
                bin_new += bin_old[4:7]
                # Hareket yönüne ek olarak, square bilgiside değişmeli
                bin_new_square = ''.join('1' if x=='0' else '0' for x in bin_old[7:])
                bin_new += bin_new_square
                new_index = int(bin_new, 2)
                new_pi[old_index], new_pi[new_index] = new_pi[new_index], new_pi[old_index]
            # Aşağı - yukarı hareketlerde yön değişmiyecek
            else:
                bin_new += bin_old[3:7]
                # Sadece square bilgisi değişmeli
                bin_new_square = ''.join('1' if x=='0' else '0' for x in bin_old[7:])
                bin_new += bin_new_square
                new_index = int(bin_new, 2)
                new_pi[old_index], new_pi[new_index] = new_pi[new_index], new_pi[old_index]
        
        return [(board, pi), (np.flip(board, axis=1), new_pi)]

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
