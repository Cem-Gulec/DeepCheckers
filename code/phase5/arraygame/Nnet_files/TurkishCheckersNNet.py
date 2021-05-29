import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

class TurkishCheckersNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(TurkishCheckersNNet, self).__init__()
        self.conv1 = nn.Conv2d(1, args.num_channels, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv5 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv6 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv7 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv8 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv9 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv10 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv11 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv12 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv13 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv14 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv15 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv16 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv17 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv18 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)
        self.conv19 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)



        self.bn1 = nn.BatchNorm2d(args.num_channels)
        self.bn2 = nn.BatchNorm2d(args.num_channels)
        self.bn3 = nn.BatchNorm2d(args.num_channels)
        self.bn4 = nn.BatchNorm2d(args.num_channels)
        self.bn5 = nn.BatchNorm2d(args.num_channels)
        self.bn6 = nn.BatchNorm2d(args.num_channels)
        self.bn7 = nn.BatchNorm2d(args.num_channels)
        self.bn8 = nn.BatchNorm2d(args.num_channels)
        self.bn9 = nn.BatchNorm2d(args.num_channels)
        self.bn10 = nn.BatchNorm2d(args.num_channels)
        self.bn11 = nn.BatchNorm2d(args.num_channels)
        self.bn12 = nn.BatchNorm2d(args.num_channels)
        self.bn13 = nn.BatchNorm2d(args.num_channels)
        self.bn14 = nn.BatchNorm2d(args.num_channels)
        self.bn15 = nn.BatchNorm2d(args.num_channels)
        self.bn16 = nn.BatchNorm2d(args.num_channels)
        self.bn17 = nn.BatchNorm2d(args.num_channels)
        self.bn18 = nn.BatchNorm2d(args.num_channels)
        self.bn19 = nn.BatchNorm2d(args.num_channels)


        self.fc1 = nn.Linear(args.num_channels*(self.board_x-4)*(self.board_y-4), 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)

        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)

        self.fc3 = nn.Linear(512, self.action_size)

        self.fc4 = nn.Linear(512, 1)

    def forward(self, s):
        #                                                           s: batch_size x board_x x board_y
        s = s.view(-1, 1, self.board_x, self.board_y)                # batch_size x 1 x board_x x board_y
        s = F.relu(self.bn1(self.conv1(s)))                          # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn2(self.conv2(s)))                          # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn3(self.conv3(s)))                          # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.dropout(F.relu(self.bn4(self.conv4(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn5(self.conv5(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn6(self.conv6(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn7(self.conv7(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.dropout(F.relu(self.bn8(self.conv8(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn9(self.conv9(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn10(self.conv10(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn11(self.conv11(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.dropout(F.relu(self.bn12(self.conv12(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn13(self.conv13(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn14(self.conv14(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn15(self.conv15(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.dropout(F.relu(self.bn16(self.conv16(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn17(self.conv17(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn18(self.conv18(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        #s = F.relu(self.bn19(self.conv19(s)))
        # batch_size x num_channels x (board_x-4) x (board_y-4)
        s = s.view(-1, self.args.num_channels*(self.board_x-4)*(self.board_y-4))

        s = F.dropout(F.relu(self.fc_bn1(self.fc1(s))), p=self.args.dropout, training=self.training)  # batch_size x 1024
        s = F.dropout(F.relu(self.fc_bn2(self.fc2(s))), p=self.args.dropout, training=self.training)  # batch_size x 512

        pi = self.fc3(s)                                                                         # batch_size x action_size
        v = self.fc4(s)                                                                          # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)
