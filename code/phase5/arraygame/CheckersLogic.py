
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
    #  1, 0     ==>  Alt tarafa doğru, aşağıya hamle yönü
    # -1, 0     ==>  Üst tarafa doğru, yukarıya hamle yönü
    #  0, 1     ==>  Yan tarafa doğru, sağ tarafa hamle yönü
    #  0, -1    ==>  Yan tarafa doğru, sol tarafa hamle yönü
    __directions = [(1,0), (-1,0), (0,1), (0,-1)] #,
                    #(1,1), (1,-1), (-1,1), (-1,-1)]
    
    # N burada boardın size'ını belirlemek için, default olarak 8
    def __init__(self, n=8):
        
        self.n = n
        self.capture = False
        self.captureList = set()
        
        # Board kurulumu 
        self.pieces = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n
        
        # Artık elimizde self.pieces 'de 8x8lik boş bir board var
        
        #               Initial case:
        #       8 . . . . . . . .
        #       7 S S S S S S S S
        #       6 S S S S S S S S
        #       5 . . . . . . . .
        #       4 . . . . . . . .
        #       3 B B B B B B B B
        #       2 B B B B B B B B
        #       1 . . . . . . . .
        #         a b c d e f g h
        
        # Beyaz taşlar a2:h2 + a3:h3; Tahtada B ile gösterilen yerler
        # Siyah taşlar a6:h6 + a7:h7; Tahtada S ile gösterilen yerler
        
        # Siyah taşlar
        self.pieces[1] = [-1] * self.n
        self.pieces[2] = [-1] * self.n
        
        """ self.pieces[4][2] = -1
        self.pieces[4][3] = 1
        self.pieces[4][4] = -1
        self.pieces[3][3] = -1 """
        
        # Beyaz taşlar
        self.pieces[5] = [1] * self.n
        self.pieces[6] = [1] * self.n
    
    # add [][] indexer syntax to the Board
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
        
    def get_game_result(self, color):
        """ Burada color yendiyse 1, yenildiyse -1, berabere ise 0 döndürcek.
        Bunu yapabilmek için kontrol etmememiz gereken kriterler ise:
        1 - rakibin tüm taşlarının bitmiş olması,
        2 - player'ın yapacak hamlesi kalmaması """
        # variables
        enemy = -color
        enemyCount = 0
        numberOfValidMoves = 0
        
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] * enemy > 0:      # Squarede enemy taşı var
                    enemyCount += 1
                elif self[x][y] * color > 0:    # Squarede bizim taşımız var
                    numberOfValidMoves += len(self.get_moves_for_square((x, y)))  # Squarede legal move var mı
                
                if enemyCount > 0 and numberOfValidMoves > 0:
                    return 0    # Oyun devam etmeli
        
        # Bütün squareleri kontrol ettik ve hala enemy piece bulamadıysak, oyunu kazanmışızdır
        if enemyCount == 0:
            return 1
        
        # Hala enemy piece varsa ve bizim valid hamlemiz kalmadıysa, rakip oyunu kazanmıştır
        if numberOfValidMoves == 0:
            return -1
        
        # Oyun hala devam etmekte
        return 0
    
    
    def execute_move(self, action, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        
        # action = 8 bit length information == [_ _] [_ _ _ _ _ _] 
        # ilk 2 bit direction bilgisini tutup bizlere move square'ine hangi yolu kullanarak geldiğimizi bildirecek
        # son 6 bit move info kullanacak bize hangi square gitmemiz gerekiyor bilgisini verecek
        
        move = action & 63
        direction = self.get_direction(action >> 6)
        square = (int(move/self.n), move%self.n)
        
        x, y = square[0], square[1]
        
        if self.capture:
            captured_piece = [x-direction[0], y-direction[1]]
            capturing_piece = [x-2*direction[0], y-2*direction[1]]
             
            self.pieces[captured_piece[0]][captured_piece[1]] = 0
            self.pieces[capturing_piece[0]][capturing_piece[1]] = 0
            self.pieces[x][y] = color
            self.capture = False
            self.captureList.clear()
        else:
            piece_to_move = [x-direction[0], y-direction[1]]
            print(len(self.pieces))
            print(len(self.pieces[1]))
            self.pieces[piece_to_move[0]][piece_to_move[1]] = 0
            self.pieces[x][y] = color
        
        
        
    def get_direction(self, direction_number):
        # 4 farklı direction olacak :
        # 00 : Yukarı   == 0:[-1,0]
        # 01 : Aşağı    == 1:[1,0]
        # 10 : Sağa     == 2:[0,1]
        # 11 : Sola     == 3:[0,-1]
        
        direction_dict = {0:[-1,0], 1:[1,0], 2:[0,1], 3:[0,-1]}                 
        return direction_dict[direction_number]
        
    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin[0] + direction[0], origin[1] + direction[1]
        
        if not (x < self.n and y < self.n ):
            return
        
        color = self.pieces[origin[0]][origin[1]]
        square = self.pieces[x][y]
        
        
        if square == 0:
            return (x, y)
        elif color * square < 0:
            x1, y1 = x+direction[0], y+direction[1]
            
            if not (x1 < self.n and y1 < self.n ):
                return
            
            if self.pieces[x1][y1] == 0:
                self.capture = True
                self.captureList.update([(x1,y1)])
            
        return
