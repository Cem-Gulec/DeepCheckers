import numpy as np



class RandomPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a 


class HumanCheckersPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print(int(i/self.game.n), int(i%self.game.n))
        while True:
            print("I am here and I was stuck all the time")
            break
        