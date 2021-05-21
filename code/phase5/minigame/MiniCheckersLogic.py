
# Sol taraf row, Sağ taraf column gösterecek şekilde tasarlandı

# Taşların değerleriyse şöyle:
# 3     : Dama olmuş Beyaz renkli taş
# 1     : Normal Beyaz renkli taş
# 0     : Boş alan
# -1    : Normal Siyah renkli taş
# -3    : Dama olmuş Siyah renkli taş
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
    __directions = [(1,1), (1,-1), (-1,1), (-1,-1)]

    def __init__(self, x=8, y=4):

        self.x = x
        self.y = y
        #self.capture = False
        self.captureList = list()

        # Board kurulumu
        self.pieces = list()
        for i in range(self.x):
            row = []
            for j in range(self.y):
                row.append(0)
            self.pieces.append(row)

        # Artık elimizde self.pieces 'de 8x8lik boş bir board var

        #               Initial case:
        #       8 . B . B 
        #       7 B . B . 
        #       6 . B . B 
        #       5 . . . . 
        #       4 . . . . 
        #       3 W . W . 
        #       2 . W . W 
        #       1 W . W . 
        #         a b c d 

        # Beyaz taşlar a2:h2 + a3:h3; Tahtada B ile gösterilen yerler
        # Siyah taşlar a6:h6 + a7:h7; Tahtada S ile gösterilen yerler

        # Siyah taşlar
        self.pieces[0][1], self.pieces[0][3] = -1, -1
        self.pieces[1][0], self.pieces[1][2] = -1, -1
        self.pieces[2][1], self.pieces[2][3] = -1, -1

        self.pieces[5][0], self.pieces[5][2] = 1, 1
        self.pieces[6][1], self.pieces[6][3] = 1, 1
        self.pieces[7][0], self.pieces[7][2] = 1, 1


    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self, color):
        # returns all the legal moves

        moves = set()
        for x in range(self.x):
            for y in range(self.y):
                # empty kareleri ele
                if self[x][y] * color > 0:
                    newmoves = self.get_moves_for_square((x, y))
                    moves.update(newmoves)

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
                if direction[0] != move_direction:   # Beyaz taşlar aşağı hareket olmamalı
                    move = self._discover_move(square, direction)
                    if move:
                        moves.append(move)

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
        for x in range(self.x):
            for y in range(self.y):
                if self[x][y] * color > 0:
                    return True
        
        return False
    
    # Boolean function to check whether given player color has a valid move on board or not
    def has_a_valid_move(self, color):
        for x in range(self.x):
            for y in range(self.y):
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
        enemyCount = 0  # Rakip taşların sayısı
        myCount = 0     # Bizim taşların sayısı
        
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
            if color in self.pieces[0]:     # White wins
                return 1
            elif -color in self.pieces[7]:  # Black wins
                return -1
            else:
                return 0        # Game still continues
        else:       # color black
            if color in self.pieces[7]:     # Black wins
                return 1
            elif -color in self.pieces[0]:  # White wins
                return -1
            else:
                return 0        # Game still continues

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

        move = action & 31
        # direction = self.get_direction(action >> 6)
        # 4 farklı direction olacak :
        # 00 : Yukarı   == 0:[-1,0]
        # 01 : Aşağı    == 1:[1,0]
        # 10 : Sağa     == 2:[0,1]
        # 11 : Sola     == 3:[0,-1]
        direction_dict = {0: [-1, -1], 1: [-1, 1], 2: [1, -1], 3: [1, 1]}
        direction = direction_dict[(action >> 5) & 3]

        # capture flag 
        capture = (action >> 7) & 1        

        square = (int(move/self.y), move % self.y)

        x, y = square[0], square[1]

        if capture:
            captured_piece = [x+direction[0], y+direction[1]]
            capturing_piece = [x+2*direction[0], y+2*direction[1]]

            self.pieces[captured_piece[0]][captured_piece[1]] = 0
            self.pieces[capturing_piece[0]][capturing_piece[1]] = 0
            self.pieces[x][y] = color
            self.captureList.clear()
        else:
            piece_to_move = [x+direction[0], y+direction[1]]
            self.pieces[piece_to_move[0]][piece_to_move[1]] = 0
            self.pieces[x][y] = color

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin[0] + direction[0], origin[1] + direction[1]

        if not ((0 <= x < self.x) and (0 <= y < self.y)):
            return

        color = self.pieces[origin[0]][origin[1]]
        square = self.pieces[x][y]

        direction_dict = {0: (1, 1), 1: (1, -1), 2: (-1, 1), 3: (-1, -1)}
        for key, ele in direction_dict.items():
            if ele == direction:
                direction_way = key

        if square == 0:
            return int(self.get_bin(0, 2) + self.get_bin(direction_way, 2) + self.get_bin(x*self.y+y, 5), 2)
        elif color * square < 0:
            x1, y1 = x+direction[0], y+direction[1]

            if not ((0 <= x1 < self.x) and (0 <= y1 < self.y)):
                return

            if self.pieces[x1][y1] == 0:
                self.capture = True
                self.captureList.append(
                    int(self.get_bin(1, 2) + self.get_bin(direction_way, 2) + self.get_bin(x1*self.y+y1, 5), 2))

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
