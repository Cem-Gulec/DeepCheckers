import numpy as np

positions = [
        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'
        ]

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

    def get_new_valids(self, valids):
        # Bu method pi değerlerinin nerelerde 0 olmadığını bulup,
        # yeni action valuelarını hesaplayarak pi güncelleyecek
        #num_zeros = 9 if mini else 10
        non_zero_indexes = [i for i,e in enumerate(valids) if e!=0]
        for old_index in non_zero_indexes:
            bin_old_index = format(old_index, 'b').zfill(10)
            bin_new_index = ''.join('1' if x=='0' else '0' for x in bin_old_index[2:])
            bin_index = bin_old_index[:2] + bin_new_index
            new_action = int(bin_index, 2)
            valids[old_index], valids[new_action] = valids[new_action], valids[old_index]
    
    def get_source_square(self, dest_square, binary_move):
        capture = int(binary_move[1], 2)
        old_direction = int(binary_move[2:4], 2)
        direction_dict = {0:[-1, -1], 1:[-1, 1], 2:[1, -1], 3:[1, 1]}
        direction = direction_dict[old_direction]
        if capture:
            new_square = dest_square + (direction[0] * 16 + 2 * direction[1])
        else:
            new_square = dest_square + (direction[0] * 8 + direction[1])
        return positions[new_square]



    def play(self, board):
        direction = None
        valid = self.game.getValidMoves(board, 1)
        self.get_new_valids(valids=valid)
        move_dict = {}
        for i in range(len(valid)):
            if valid[i]:
                binary_move = self.get_bin(i, 10)
                capture = int(binary_move[1], 2)
                square = int(binary_move[4:], 2)
                source_sq = self.get_source_square(square, binary_move)
                if capture:
                    print("Possible capture(s): {}x{}:{}".format(source_sq, positions[square], i))
                    s = str(source_sq) + 'x' + positions[square]
                    move_dict[s] = i
                else:
                    print("Possible move(s): {}-{}:{}".format(source_sq, positions[square], i))
                    s = str(source_sq) + '-' + positions[square]
                    move_dict[s] = i
        # örneğin 24 indexli a4 için 
        # 24ü binary'e çevir bu 6 bitlik kısım
        # başına directionın bitlerini ekle
        while True:
            inpt = input("Enter move : ")
            move = move_dict[inpt]
            bin_old_index = format(int(move), 'b').zfill(10)
            bin_new_index = ''.join('1' if x=='0' else '0' for x in bin_old_index[2:])
            bin_index = bin_old_index[:2] + bin_new_index
            new_action = int(bin_index, 2)
            return int(new_action)
    
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
