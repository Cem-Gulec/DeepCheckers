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
        self.conv18 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv19 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv20 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv21 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv22 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv23 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv24 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv25 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv26 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv27 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv28 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv29 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv30 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv31 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv32 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv33 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv34 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv35 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv36 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv37 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv38 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv39 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)
        self.conv40 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)



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
        self.bn20 = nn.BatchNorm2d(args.num_channels)
        self.bn21 = nn.BatchNorm2d(args.num_channels)
        self.bn22 = nn.BatchNorm2d(args.num_channels)
        self.bn23 = nn.BatchNorm2d(args.num_channels)
        self.bn24 = nn.BatchNorm2d(args.num_channels)
        self.bn25 = nn.BatchNorm2d(args.num_channels)
        self.bn26 = nn.BatchNorm2d(args.num_channels)
        self.bn27 = nn.BatchNorm2d(args.num_channels)
        self.bn28 = nn.BatchNorm2d(args.num_channels)
        self.bn29 = nn.BatchNorm2d(args.num_channels)
        self.bn30 = nn.BatchNorm2d(args.num_channels)
        self.bn31 = nn.BatchNorm2d(args.num_channels)
        self.bn32 = nn.BatchNorm2d(args.num_channels)
        self.bn33 = nn.BatchNorm2d(args.num_channels)
        self.bn34 = nn.BatchNorm2d(args.num_channels)
        self.bn35 = nn.BatchNorm2d(args.num_channels)
        self.bn36 = nn.BatchNorm2d(args.num_channels)
        self.bn37 = nn.BatchNorm2d(args.num_channels)
        self.bn38 = nn.BatchNorm2d(args.num_channels)
        self.bn39 = nn.BatchNorm2d(args.num_channels)
        self.bn40 = nn.BatchNorm2d(args.num_channels)


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
        s = F.relu(self.bn19(self.conv19(s)))
        s = F.dropout(F.relu(self.bn20(self.conv20(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn21(self.conv21(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn22(self.conv22(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.relu(self.bn23(self.conv23(s)))
        s = F.dropout(F.relu(self.bn24(self.conv24(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn25(self.conv25(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn26(self.conv26(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.relu(self.bn27(self.conv27(s)))
        s = F.dropout(F.relu(self.bn28(self.conv28(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn29(self.conv29(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn30(self.conv30(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.relu(self.bn31(self.conv31(s)))
        s = F.dropout(F.relu(self.bn32(self.conv32(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn33(self.conv33(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn34(self.conv34(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.relu(self.bn35(self.conv35(s)))
        s = F.dropout(F.relu(self.bn36(self.conv36(s))), p=self.args.dropout, training=self.training)
        s = F.relu(self.bn37(self.conv37(s)))  # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn38(self.conv38(s)))  # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.relu(self.bn39(self.conv39(s)))
        s = F.relu(self.bn40(self.conv40(s)))  # batch_size x num_channels x board_x x board_y
        
        # batch_size x num_channels x (board_x-4) x (board_y-4)
        s = s.view(-1, self.args.num_channels*(self.board_x-4)*(self.board_y-4))

        s = F.dropout(F.relu(self.fc_bn1(self.fc1(s))), p=self.args.dropout, training=self.training)  # batch_size x 1024
        s = F.dropout(F.relu(self.fc_bn2(self.fc2(s))), p=self.args.dropout, training=self.training)  # batch_size x 512

        pi = self.fc3(s)                                                                         # batch_size x action_size
        v = self.fc4(s)                                                                          # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)
