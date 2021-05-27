# Sol taraf row, Sağ taraf column gösterecek şekilde tasarlandı

# Taşların değerleriyse şöyle:
# 3     : Dama olmuş Beyaz renkli taş
# 1     : Normal Beyaz renkli taş
# 0     : Boş alan
# -1    : Normal Siyah renkli taş
# -3    : Dama olmuş Siyah renkli taş
from numpy.lib.utils import safe_eval


class Board():
    EMPTY = 0
    WHITE_PIECE = 1
    BLACK_PIECE = -1
    WHITE_KINGS = 3
    BLACK_KINGS = -3

    # Hamlelerimizin yönlerinin tutulduğu yer
    #
    #  1, 1     ==>  Sağ aşağı tarafa hamle yönü
    #  1,-1     ==>  Sol aşağı tarafa hamle yönü
    # -1, 1     ==>  Sağ yukarı tarafa hamle yönü
    # -1,-1     ==>  Sol yukarı tarafa hamle yönü
    __directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    # N burada boardın size'ını belirlemek için, default olarak 8
    def __init__(self, n=8):

        self.n = n
        self.captureList = list()
        self.multi_capture_list = list()

        # Board kurulumu
        self.pieces = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n

        # Artık elimizde self.pieces 'de 8x8lik boş bir board var

        #               Initial case:
        #       8 . b . b . b . b
        #       7 b . b . b . b .
        #       6 . b . b . b . b
        #       5 . . . . . . . .
        #       4 . . . . . . . .
        #       3 w . w . w . w .
        #       2 . w . w . w . w
        #       1 w . w . w . w .
        #         a b c d e f g h
        
        # Siyah taşlar
        self.pieces[0][1], self.pieces[0][3], self.pieces[0][5], self.pieces[0][7] = -1, -1, -1, -1
        self.pieces[1][0], self.pieces[1][2], self.pieces[1][4], self.pieces[1][6] = -1, -1, -1, -1
        self.pieces[2][1], self.pieces[2][3], self.pieces[2][5], self.pieces[2][7] = -1, -1, -1, -1

        # Beyaz taşlar
        self.pieces[5][0], self.pieces[5][2], self.pieces[5][4], self.pieces[5][6] = 1, 1, 1, 1
        self.pieces[6][1], self.pieces[6][3], self.pieces[6][5], self.pieces[6][7] = 1, 1, 1, 1
        self.pieces[7][0], self.pieces[7][2], self.pieces[7][4], self.pieces[7][6] = 1, 1, 1, 1

    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self, color):
        # returns all the legal moves

        moves = set()
        for x in range(self.n):
            for y in range(self.n):
                # empty kareleri ele
                if self[x][y] * color > 0:
                    newmoves = self.get_moves_for_square((x, y))
                    moves.update(newmoves)

        if len(self.multi_capture_list) > 0:
            moves.clear()
            moves.add(self.multi_capture_list[-1])
            return moves

        if len(self.captureList) > 0:
            moves.clear()
            moves = self.captureList.copy()
            return moves

        return moves

    def get_moves_for_square(self, square):
        """Returns all the legal moves that ue the given square as a base.
        """
        # Square koordinatlarını aldı
        (x, y) = square

        # color hangisi
        color = self[x][y]

        # Eğer square boşsa return et
        if color == self.EMPTY:
            return None

        # Beyaz taşlarda hamle yönü yukarıya doğru, siyahlarda aşağıya doğru
        move_direction = 1 if color == 1 else -1
        moves = []

        if color == self.WHITE_PIECE:
            for direction in self.__directions:
                if direction[0] != move_direction:  # Beyaz taşlar aşağı hareket olmamalı
                    move = self._discover_move(square, direction)
                    if move:
                        moves.append(move)

        elif color == self.WHITE_KINGS:
            for direction in self.__directions:
                move = self._discover_move(square, direction)
                # print("Here --> 2.0")
                new_dir = tuple(map(lambda x, y: x + y, direction, direction))
                while (move):
                    moves.append(move)
                    # print("Here --> 2.1")
                    if (move >> 9) & 1: return moves
                    move = self._discover_move(square, new_dir)
                    new_dir = tuple(
                        map(lambda x, y: x + y, new_dir, direction))
        elif color == self.BLACK_KINGS:
            for direction in self.__directions:
                move = self._discover_move(square, direction)
                target_sq = tuple(map(lambda x, y: x + y, square, direction))
                while (move):
                    moves.append(move)
                    if (move >> 9) & 1: return moves
                    move = self._discover_move(target_sq, direction)
                    target_sq = tuple(
                        map(lambda x, y: x + y, target_sq, direction))
        # Siyah taşlar
        else:
            for direction in self.__directions:
                if direction[0] != move_direction:  # Siyah taşlarda yukarı hareket olmamalı
                    move = self._discover_move(square, direction)
                    if move:
                        moves.append(move)

        return moves

    # Boolean function, if player has a piece on board return true, or false
    def has_piece_on_board(self, color):
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] * color > 0:
                    return True

        return False

    # Boolean function to check whether given player color has a valid move on board or not
    def has_a_valid_move(self, color):
        for x in range(self.n):
            for y in range(self.n):
                # ilk if case'i squaredeki taşın bizim taşımız olduğundan emin olurken,
                # ikinci if case ise squaredeki taşın valid hamlesinin olup olmadığını kontrol ediyor
                if (self[x][y] * color > 0) and (len(self.get_moves_for_square((x, y))) > 0):
                    return True

        return False

    def get_game_result(self, color):
        """ Burada color yendiyse 1, yenildiyse -1, berabere ise 0 döndürcek.
        Bunu yapabilmek için kontrol etmememiz gereken kriterler ise:
        1 - rakibin tüm taşlarının bitmiş olması,
        2 - player'ın yapacak hamlesi kalmaması """
        # variables

        # SIMPLIFIED CHECKERS ENDING

        # Taşların sayısını kontrol etmek
        enemy = -color  # Rakip taşların rengi

        # Rakip taşı kalmadıysa oyunu biz kazandık
        if not self.has_piece_on_board(enemy):
            return 1
        # Bizim oynatacak taşımız kalmadıysa oyunu rakip kazandı
        if not self.has_a_valid_move(color):
            return -1

        # İki oyuncununda kalan taşları var, oyun bitme koşulu araştırılmalı
        # Beyaz renkler en üst row'a gelince oyunu kazanmalı
        # Siyah renkler en alt row'a gelince oyunu kazanmalı
        if color == self.WHITE_PIECE:
            if color in self.pieces[0]:  # White wins
                return 1
            elif -color in self.pieces[7]:  # Black wins
                return -1
            else:
                return 0  # Game still continues
        else:  # color black
            if color in self.pieces[7]:  # Black wins
                return 1
            elif -color in self.pieces[0]:  # White wins
                return -1
            else:
                return 0  # Game still continues

    def is_promotion_move(self, dest_square, source_square):
        # TODO Şu anlık dama taşlarını kaldırdık deneme amaçlı, bunu zamanı gelince aç.
        return False
        # Oynadığımız taş beyazsa ve promotion alanına girmişsek, true dönder        
        if (self[source_square[0]][source_square[1]] == self.WHITE_PIECE) and (dest_square[0] == 0):
            return True
        # Oynadığımız taş siyahsa ve promotion alanına girmişsek, true dönder        
        if (self[source_square[0]][source_square[1]] == self.BLACK_PIECE) and (dest_square[0] == 7):
            return True
        # Normal hamle, promotion yok
        return False

    def execute_move(self, action, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        # Much like move generation, start at the new piece's square and
        # follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.

        # action = 8 bit length information == [_ _] [_ _ _ _ _ _]
        # ilk 2 bit direction bilgisini tutup bizlere move square'ine hangi yolu kullanarak geldiğimizi bildirecek
        # son 6 bit move info kullanacak bize hangi square gitmemiz gerekiyor bilgisini verecek

        move = action & 63
        # direction = self.get_direction(action >> 6)
        # 4 farklı direction olacak :
        # 00 : Yukarı   == 0:[-1,0]
        # 01 : Aşağı    == 1:[1,0]
        # 10 : Sağa     == 2:[0,1]
        # 11 : Sola     == 3:[0,-1]
        direction_dict = {0: [-1, -1], 1: [-1, 1], 2: [1, -1], 3: [1, 1]}
        direction = direction_dict[(action >> 6) & 3]

        # capture flag
        capture = (action >> 8) & 1

        square = [int(move / self.n), move % self.n]

        # x, y = square[0], square[1]

        if capture:
            captured_piece = [sum(t) for t in zip(square, direction)]
            # Burada captured piece'i bulana kadar geriye doğru gitmeli
            while self[captured_piece[0]][captured_piece[1]] == 0:
                captured_piece = [sum(t) for t in zip(captured_piece, direction)]

            capturing_piece = [sum(t) for t in zip(captured_piece, direction)]
            # Burada da capture yapan taşı bulana kadar geriye gitmeli
            while self[capturing_piece[0]][capturing_piece[1]] == 0:
                capturing_piece = [sum(t) for t in zip(capturing_piece, direction)]

            self.pieces[square[0]][square[1]] = color * 3 if self.is_promotion_move(
                square, capturing_piece) else self.pieces[capturing_piece[0]][capturing_piece[1]]
            self.pieces[captured_piece[0]][captured_piece[1]] = 0
            self.pieces[capturing_piece[0]][capturing_piece[1]] = 0
        else:
            piece_to_move = [sum(t) for t in zip(square, direction)]
            while self[piece_to_move[0]][piece_to_move[1]] == 0:
                # print("Here --> 6")
                piece_to_move = [sum(t) for t in zip(piece_to_move, direction)]

            self.pieces[square[0]][square[1]] = color * 3 if self.is_promotion_move(
                square, piece_to_move) else self.pieces[piece_to_move[0]][piece_to_move[1]]
            self.pieces[piece_to_move[0]][piece_to_move[1]] = 0

    def has_multi_capture_move(self, source_square):
        # Önceden capture hamlesi yapan taşlar için çağrılıyor,
        # ilk hamlesinden sonra başka capture hareketi var mı diye kontrol ediliyor
        # Squarede capture hamlesi varsa True, yoksa False dönecek
        moves = self.get_moves_for_square(square=source_square)
        if not moves:
            return False

        for move in moves:
            capture_flag = (move >> 8) & 1
            if capture_flag:
                return True

        return False

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin[0] + direction[0], origin[1] + direction[1]

        if not ((0 <= x < self.n) and (0 <= y < self.n)):
            return

        color = self.pieces[origin[0]][origin[1]]
        square = self.pieces[x][y]

        direction_dict = {0: (1, 1), 1: (1, -1), 2: (-1, 1), 3: (-1, -1)}
        norm_direction = tuple([int(num / abs(num)) for num in direction])
        for key, ele in direction_dict.items():
            if ele == norm_direction:
                direction_way = key

        if square == 0:
            return int(self.get_bin(0, 2) + self.get_bin(direction_way, 2) + self.get_bin(x * 8 + y, 6), 2)
        elif color * square < 0:
            x1, y1 = x + norm_direction[0], y + norm_direction[1]

            if not ((0 <= x1 < self.n) and (0 <= y1 < self.n)):
                return

            if self.pieces[x1][y1] == 0:
                s = self.get_bin(direction_way, 2) + self.get_bin(x1 * 8 + y1, 6)
                self.pieces[x1][y1] = color
                self.pieces[origin[0]][origin[1]] = 0
                self.pieces[x][y] = 0
                if self.has_multi_capture_move((x1, y1)):
                    self.pieces[x1][y1] = 0
                    self.pieces[origin[0]][origin[1]] = color
                    self.pieces[x][y] = square
                    action = int(self.get_bin(3, 2) + s, 2)
                    if action not in self.multi_capture_list:
                        self.multi_capture_list.append(action)
                    return action
                else:
                    self.pieces[x1][y1] = 0
                    self.pieces[origin[0]][origin[1]] = color
                    self.pieces[x][y] = square
                    self.captureList.append(int(self.get_bin(1, 2) + s, 2))
                    return int(self.get_bin(1, 2) + s, 2)

        return

    def get_bin(self, x, n):
        """
        Get the binary representation of x with n digits.

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
