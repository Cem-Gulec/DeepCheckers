
import sys
sys.path.append('../..')
from utils import *

import tensorflow as tf

class TurkishCheckersNNet():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Renaming functions
        Relu = tf.nn.relu
        Tanh = tf.nn.tanh
        BatchNormalization = tf.layers.batch_normalization
        Dropout = tf.layers.dropout
        Dense = tf.layers.dense

        # Neural Net
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.input_boards = tf.placeholder(tf.float32, shape=[None, self.board_x, self.board_y])    # s: batch_size x board_x x board_y
            self.dropout = tf.placeholder(tf.float32)
            self.isTraining = tf.placeholder(tf.bool, name="is_training")

            x_image = tf.reshape(self.input_boards, [-1, self.board_x, self.board_y, 1])                    # batch_size  x board_x x board_y x 1
            h_conv1 = Relu(BatchNormalization(self.conv2d(x_image, args.num_channels, 'same'), axis=3, training=self.isTraining))     # batch_size  x board_x x board_y x num_channels
            h_conv2 = Relu(BatchNormalization(self.conv2d(h_conv1, args.num_channels, 'same'), axis=3, training=self.isTraining))     # batch_size  x board_x x board_y x num_channels
            h_conv3 = Relu(BatchNormalization(self.conv2d(h_conv2, args.num_channels, 'same'), axis=3, training=self.isTraining))    # batch_size  x (board_x-2) x (board_y-2) x num_channels
            h_conv4 = Relu(BatchNormalization(self.conv2d(h_conv3, args.num_channels, 'same'), axis=3, training=self.isTraining))    # batch_size  x (board_x-4) x (board_y-4) x num_channels
            h_conv5 = Relu(BatchNormalization(self.conv2d(h_conv4, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv6 = Relu(BatchNormalization(self.conv2d(h_conv5, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv7 = Relu(BatchNormalization(self.conv2d(h_conv6, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv8 = Relu(BatchNormalization(self.conv2d(h_conv7, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv9 = Relu(BatchNormalization(self.conv2d(h_conv8, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv10 = Relu(BatchNormalization(self.conv2d(h_conv9, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv11 = Relu(BatchNormalization(self.conv2d(h_conv10, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv12 = Relu(BatchNormalization(self.conv2d(h_conv11, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv13 = Relu(BatchNormalization(self.conv2d(h_conv12, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv14 = Relu(BatchNormalization(self.conv2d(h_conv13, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv15= Relu(BatchNormalization(self.conv2d(h_conv14, args.num_channels,  'same'), axis=3, training=self.isTraining))
            h_conv16 = Relu(BatchNormalization(self.conv2d(h_conv15, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv17 = Relu(BatchNormalization(self.conv2d(h_conv16, args.num_channels, 'same'), axis=3, training=self.isTraining))
            h_conv18 = Relu(BatchNormalization(self.conv2d(h_conv17, args.num_channels, 'valid'), axis=3, training=self.isTraining))
            h_conv19 = Relu(BatchNormalization(self.conv2d(h_conv18, args.num_channels, 'valid'), axis=3, training=self.isTraining))
            h_conv19_flat = tf.reshape(h_conv19, [-1, args.num_channels*(self.board_x-4)*(self.board_y-4)])
            s_fc1 = Dropout(Relu(BatchNormalization(Dense(h_conv19_flat, 1024), axis=1, training=self.isTraining)), rate=self.dropout) # batch_size x 1024
            s_fc2 = Dropout(Relu(BatchNormalization(Dense(s_fc1, 512), axis=1, training=self.isTraining)), rate=self.dropout)         # batch_size x 512
            self.pi = Dense(s_fc2, self.action_size)                                                        # batch_size x self.action_size
            self.prob = tf.nn.softmax(self.pi)
            self.v = Tanh(Dense(s_fc2, 1))                                                               # batch_size x 1

            self.calculate_loss()

    def conv2d(self, x, out_channels, padding):
      return tf.layers.conv2d(x, out_channels, kernel_size=[3,3], padding=padding)

    def calculate_loss(self):
        self.target_pis = tf.placeholder(tf.float32, shape=[None, self.action_size])
        self.target_vs = tf.placeholder(tf.float32, shape=[None])
        self.loss_pi =  tf.losses.softmax_cross_entropy(self.target_pis, self.pi)
        self.loss_v = tf.losses.mean_squared_error(self.target_vs, tf.reshape(self.v, shape=[-1,]))
        self.total_loss = self.loss_pi + self.loss_v
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            self.train_step = tf.train.AdamOptimizer(self.args.lr).minimize(self.total_loss)