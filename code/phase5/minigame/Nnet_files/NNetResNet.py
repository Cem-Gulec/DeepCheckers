from .TurkishCheckersNNetResNet import TurkishCheckersNNetResNet as onnet
import coloredlogs
import logging
from NeuralNet import NeuralNet
from utils import *
import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
sys.path.append('../..')

log = logging.getLogger(__name__)


args = dotdict({
    'lr': 0.1,
    'dropout': 0.25,
    'epochs': 10,
    'batch_size': 128,
    'cuda': True,
    'num_channels': 128,
    'num_residual_layers': 40
})


class NNetWrapperResNet(NeuralNet):
    def __init__(self, game):
        self.nnet = onnet(game, args)
        self.nnet.model.summary()
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        history_callback = self.nnet.model.fit(x=input_boards, y=[
                            target_pis, target_vs], batch_size=args.batch_size, epochs=args.epochs)
        
        total_loss = history_callback.history['loss']
        pi_loss   = history_callback.history['pi_loss']
        v_loss  = history_callback.history['v_loss']

        with open("out.txt", "a") as myfile:
            myfile.write(f'total_loss: {total_loss} \npi_loss: {pi_loss} \nv_loss: {v_loss}')

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict(board)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print(
                "Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        # if not os.path.exists(filepath):
        #raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)
        log.info('Loading Weights...')