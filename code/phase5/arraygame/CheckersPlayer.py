import numpy as np

positions = [
        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'
        ]

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a

class RandomPlayer2():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, -1)
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a

class HumanCheckersPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        direction = None
        valid = self.game.getValidMoves(board, -1)
        for i in range(len(valid)):
            if valid[i]:
                binary_move = self.get_bin(i, 8)
                square = int(binary_move[2:], 2)
                direction = [binary_move[0], binary_move[1]]
                print("Possible move: ", positions[square], i, binary_move)
        # örneğin 24 indexli a4 için 
        # 24ü binary'e çevir bu 6 bitlik kısım
        # başına directionın bitlerini ekle
        while True:
            move = input("Enter moves as an integer :")
            parsed_move = positions.index(move)
            move_square = self.get_bin(parsed_move, 6)
            move_square = ''.join(direction) + move_square
            return int(move_square, 2)
    
    def get_bin(self, x, n):
        """
        Get the binary representation of x.

        Parameters
        ----------
        x : int
        n : int
            Minimum number of digits. If x needs less digits in binary, the rest
            is filled with zeros.

        Returns
        -------
        str
        """
        return format(x, 'b').zfill(n)
