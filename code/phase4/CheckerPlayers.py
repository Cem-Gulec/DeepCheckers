import numpy as np

class HumanCheckersPlayer():
    def __init__(self, game):
        self.game = game
        
    def play(self, board):
        valid = self.game.getValidMoves(board, 1)