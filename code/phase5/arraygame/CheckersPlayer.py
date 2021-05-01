import numpy as np


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
        valid = self.game.getValidMoves(board, -1)
        for i in range(len(valid)):
            if valid[i]:
                print("Printing moves ", i, self.get_bin(i, 8))
        while True:
            a = input("Enter moves as an integer :")
            return int(a)

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
