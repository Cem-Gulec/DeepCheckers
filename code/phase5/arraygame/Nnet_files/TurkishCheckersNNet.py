import sys
sys.path.append('..')
from utils import *


import tensorflow as tf


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
        self.conv3 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)
        self.conv4 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)

        self.bn1 = nn.BatchNorm2d(args.num_channels)
        self.bn2 = nn.BatchNorm2d(args.num_channels)
        self.bn3 = nn.BatchNorm2d(args.num_channels)
        self.bn4 = nn.BatchNorm2d(args.num_channels)

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
        s = F.relu(self.bn4(self.conv4(s)))                          # batch_size x num_channels x (board_x-4) x (board_y-4)
        s = s.view(-1, self.args.num_channels*(self.board_x-4)*(self.board_y-4))

        s = F.dropout(F.relu(self.fc_bn1(self.fc1(s))), p=self.args.dropout, training=self.training)  # batch_size x 1024
        s = F.dropout(F.relu(self.fc_bn2(self.fc2(s))), p=self.args.dropout, training=self.training)  # batch_size x 512

        pi = self.fc3(s)                                                                         # batch_size x action_size
        v = self.fc4(s)                                                                          # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)
    
   
class ResNet():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.graph = tf.Graph()
        with self.graph.as_default(): 
            self.input_boards = tf.placeholder(tf.float32, shape=[None, self.board_x, self.board_y])    # s: batch_size x board_x x board_y
            self.dropout = tf.placeholder(tf.float32)
            self.isTraining = tf.placeholder(tf.bool, name="is_training")

            x_image = tf.reshape(self.input_boards, [-1, self.board_x, self.board_y, 1])                    # batch_size  x board_x x board_y x 1
            x_image = tf.layers.conv2d(x_image, args.num_channels, kernel_size=(3, 3), strides=(1, 1),name='conv',padding='same',use_bias=False)
            x_image = tf.layers.batch_normalization(x_image, axis=1, name='conv_bn', training=self.isTraining)
            x_image = tf.nn.relu(x_image)

            residual_tower = self.residual_block(inputLayer=x_image, kernel_size=3, filters=args.num_channels, stage=1, block='a')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=2, block='b')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=3, block='c')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=4, block='d')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=5, block='e')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=6, block='g')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=7, block='h')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=8, block='i')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=9, block='j')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=10, block='k')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=11, block='m')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=12, block='n')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=13, block='o')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=14, block='p')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=15, block='q')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=16, block='r')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=17, block='s')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=18, block='t')
            residual_tower = self.residual_block(inputLayer=residual_tower, kernel_size=3, filters=args.num_channels, stage=19, block='u')

            policy = tf.layers.conv2d(residual_tower, 2,kernel_size=(1, 1), strides=(1, 1),name='pi',padding='same',use_bias=False)
            policy = tf.layers.batch_normalization(policy, axis=3, name='bn_pi', training=self.isTraining)
            policy = tf.nn.relu(policy)
            policy = tf.layers.flatten(policy, name='p_flatten')
            self.pi = tf.layers.dense(policy, self.action_size)
            self.prob = tf.nn.softmax(self.pi)

            value = tf.layers.conv2d(residual_tower, 1,kernel_size=(1, 1), strides=(1, 1),name='v',padding='same',use_bias=False)
            value = tf.layers.batch_normalization(value, axis=3, name='bn_v', training=self.isTraining)
            value = tf.nn.relu(value)
            value = tf.layers.flatten(value, name='v_flatten')
            value = tf.layers.dense(value, units=256)
            value = tf.nn.relu(value)
            value = tf.layers.dense(value, 1)
            self.v = tf.nn.tanh(value) 
                                                              
            self.calculate_loss()

    def residual_block(self,inputLayer, filters,kernel_size,stage,block):
        conv_name = 'res' + str(stage) + block + '_branch'
        bn_name = 'bn' + str(stage) + block + '_branch'

        shortcut = inputLayer

        residual_layer = tf.layers.conv2d(inputLayer, filters,kernel_size=(kernel_size, kernel_size), strides=(1, 1),name=conv_name+'2a',padding='same',use_bias=False)
        residual_layer = tf.layers.batch_normalization(residual_layer, axis=3, name=bn_name+'2a', training=self.isTraining)
        residual_layer = tf.nn.relu(residual_layer)
        residual_layer = tf.layers.conv2d(residual_layer, filters,kernel_size=(kernel_size, kernel_size), strides=(1, 1),name=conv_name+'2b',padding='same',use_bias=False)
        residual_layer = tf.layers.batch_normalization(residual_layer, axis=3, name=bn_name+'2b', training=self.isTraining)
        add_shortcut = tf.add(residual_layer, shortcut)
        residual_result = tf.nn.relu(add_shortcut)
        
        return residual_result

    def calculate_loss(self):
        self.target_pis = tf.placeholder(tf.float32, shape=[None, self.action_size])
        self.target_vs = tf.placeholder(tf.float32, shape=[None])
        self.loss_pi =  tf.losses.softmax_cross_entropy(self.target_pis, self.pi)
        self.loss_v = tf.losses.mean_squared_error(self.target_vs, tf.reshape(self.v, shape=[-1,]))
        self.total_loss = self.loss_pi + self.loss_v
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            self.train_step = tf.train.AdamOptimizer(self.args.lr).minimize(self.total_loss)
