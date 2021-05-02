import Arena
from arraygame.CheckersGame import CheckersGame
from arraygame.CheckersPlayer import *

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

# mini_checkers = False  # Play in 6x6 instead of the normal 8x8.
human_vs_random = True

g = CheckersGame(8)

# all players
rp = RandomPlayer(g).play
hp = HumanCheckersPlayer(g).play


# nnet players
""" n1 = NNet(g)
if mini_othello:
    n1.load_checkpoint('./temp/','checkpoint_2.pth.tar')
else:
    n1.load_checkpoint('./pretrained_models/othello/pytorch/','8x8_100checkpoints_best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0)) """

if human_vs_random:
    player2 = hp
""" else:
    n2 = NNet(g)
    n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu. """

arena = Arena.Arena(rp, player2, g, display=CheckersGame.display)

print(arena.playGame(verbose=True))
