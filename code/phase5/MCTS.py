import logging
import math
import random
import numpy as np

EPS = 1e-8

log = logging.getLogger(__name__)


class MCTS():
    """
    This class handles the MCTS tree.
    """

    def __init__(self, game, nnet, args, ZobTableArg):
        self.game = game
        self.nnet = nnet
        self.args = args
        self.Qsa = {}  # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}  # stores #times edge s,a was visited
        self.Ns = {}  # stores #times board s was visited
        self.Ps = {}  # stores initial policy (returned by neural net)

        self.Es = {}  # stores game.getGameEnded ended for board s
        self.Vs = {}  # stores game.getValidMoves for board s

        self.zobTable = np.copy(ZobTableArg)
        self.hashValue = 0
        self.hash_list = []
        self.totalNodeCount = 0
        self.repNodeCount = 0

    # Zobrsit table'da hangi piece kaçıncı indexte bilgisini bulmak için
    def indexing(self, piece):
        if (piece == -1):   # Siyah taşlar index0 de tutuluyor
            return 0
        if (piece == 1):    # Beyaz taşlar index1 de tutuluyor
            return 1
        if (piece == -3):   # Siyah dama taşları index2 de tutuluyor
            return 2
        if (piece == 3):    # Beyaz dama taşları index3 de tutuluyor
            return 3
        else:
            log.error("While indexing somethings went terribly wrong.")
            log.info("The piece is : %s", str(piece))
            return -1       # Test amaçlı?
            
    def computeHash(self, board):
        h = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    piece = self.indexing(board[i][j])
                    h = np.bitwise_xor(h, (self.zobTable[i][j][piece]))
        return h
    
    def getActionProb(self, canonicalBoard, temp=1):
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.
        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)
        """
        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)
            self.hash_list.clear()

        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        if temp == 0:
            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)
            probs[bestA] = 1
            return probs

        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        if counts_sum == 0:
            self.game.display(canonicalBoard)
        probs = [x / counts_sum for x in counts]
        return probs

    def search(self, canonicalBoard):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.
        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propagated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propagated up the search path. The values of Ns, Nsa, Qsa are
        updated.
        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.
        Returns:
            v: the negative of the value of the current canonicalBoard
        """

        #print("MCTS.search: ", self.depth, " size of map: ", len(self.Ps))
        s = self.game.stringRepresentation(canonicalBoard)
        #self.game.display(canonicalBoard)

        self.hashValue = self.computeHash(canonicalBoard)
       
        # Starting node dışındakilerin tekrarlı olmayacağını farz ettim
        if s not in self.Es:            
            self.Es[s] = self.game.getGameEnded(canonicalBoard, 1)

        if self.Es[s] != 0:
            # terminal node
            return -self.Es[s]
        
        if self.hashValue not in self.hash_list:
            self.hash_list.append(self.hashValue)
            #print(self.depth)
            #self.game.display(zobrist_board_temp)

        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(canonicalBoard)
            valids = self.game.getValidMoves(canonicalBoard, 1)
            non_zero = [i for i, e in enumerate(valids) if e != 0]
            self.Ps[s] = self.Ps[s] * valids  # masking invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s  # renormalize
            else:
                # if all valid moves were masked make all valid moves equally probable

                # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
                # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.   
                log.error("All valid moves were masked, doing a workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        self.totalNodeCount += 1
        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # pick the action with the highest upper confidence bound
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act

        next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)

        next_s = self.game.getCanonicalForm(next_s, next_player)

        temp_hash_val = self.computeHash(next_s)
        if temp_hash_val not in self.hash_list:
            
            v = self.search(next_s)
            # Repetition olmadı
            #if v:
            if (s, a) in self.Qsa:
                self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
                self.Nsa[(s, a)] += 1

            else:
                self.Qsa[(s, a)] = v
                self.Nsa[(s, a)] = 1

            self.Ns[s] += 1
            #print("END OF MCTS.search: ", self.depth, " size of map: ", len(self.Ps))
            return -v
        else:
            # TODO Hocanın bahsettiği şekilde bir sonraki en uygun hamleyi seç
            # Burada bütün hamleler repetitive hamle olursa ne olacak? Olabilir, beraberlik dön
            v = None
            while v is None:
                next_s_childs = [i for i, e in enumerate(self.game.getValidMoves(next_s, 1)) if e != 0]
                self.repNodeCount += len(next_s_childs)
                #log.info('Repetition found with action : %s', str((a)))
                non_zero = [i for i, e in enumerate(self.Vs[s]) if e != 0]
                #log.info("Numbers in valids are: {}".format(' '.join(map(str, non_zero))))
                    
                if a not in non_zero:
                    self.game.display(canonicalBoard)
                    log.error("Something terrible has happen")
                    
                self.Vs[s][a] = 0       # Valid move listesinden repetitive hamleyi kaldır
                non_zero = [i for i, e in enumerate(self.Vs[s]) if e != 0]
                #log.info("New nums in valids are: {}".format(' '.join(map(str, non_zero))))
                # Bütün hamleler masklandı oyun berabere
                if len(non_zero) == 0:
                    self.game.display(canonicalBoard) 
                    log.error("No valids move remaining..")
                    return next_player
                    
                v = self.search(canonicalBoard) # Yeni valids ve Qsa değerleriyle uygun hamleyi bul
            
            return -v