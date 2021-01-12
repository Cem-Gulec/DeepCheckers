
# Sol taraf row, Sağ taraf column gösterecek şekilde tasarlandı

# Taşların değerleriyse şöyle:
# 3     : Dama olmuş Beyaz renkli taş
# 1     : Normal Beyaz renkli taş
# 0     : Boş alan
# -1    : Normal Siyah renkli taş
# -3    : Dama olmuş Siyah renkli taş
class Board():
    
    # Hamlelerimizin yönlerinin tutulduğu yer
    #
    #  1, 0     ==>  Alt tarafa doğru, aşağıya hamle yönü
    # -1, 0     ==>  Üst tarafa doğru, yukarıya hamle yönü
    #  0, 1     ==>  Yan tarafa doğru, sağ tarafa hamsle yönü
    #  0, -1    ==>  Yan tarafa doğru, sol tarafa hamle yönü
    #  1, 1     ==>  Sağ aşağı yönlü, çapraz saldırma hareketi
    #  1, -1    ==>  Sol aşağı yönlü, çapraz saldırma hareketi
    # -1, 1     ==>  Sağ yukarı yönlü, çapraz saldırma hareketi
    # -1, -1    ==>  Sol yukarı yönlü, çapraz saldırma hareketi
    __directions = [(1,0), (-1,0), (0,1), (0,-1),
                    (1,1), (1,-1), (-1,1), (-1,-1)]
    
    # N burada boardın size'ını belirlemek için, default olarak 8
    def __init__(self, n=8):
        
        self.n = n
        
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
        
        # Beyaz taşlar
        self.pieces[5] = [1] * self.n
        self.pieces[6] = [1] * self.n
    
    def __getitem__(self, index): 
        return self.pieces[index]
    
    def countDiff(self, color):
        #  1    == Beyaz
        #  0    == Boşluk
        # -1    == Siyah
        count = 0
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] == color:
                    count += 1
                if self[x][y] == -color:
                    count -= 1
        
        return count
    
    def get_legal_moves(self, color):
        # returns all the legal moves
        
        return
    def has_legal_moves(self, color):
        return False
    
    def get_moves_for_square(self, square):
        """Returns all the legal moves that ue the given square as a base.
        """
        # Square koordinatlarını aldı
        (x, y) = square
        
        # color hangisi
        color = self[x][y]
        
        # Eğer square boşsa return et
        if color == 0:
            return None
        
        moves = []
        # Beyaz taşlarda, aşağı yön hareketlerine bakma
        if color == 1:
            for direction in self.__directions:
                if direction[0] != 1:
                    move = self._discover_move(square, direction)
                    if move:
                        moves.append(move)
                
        # Siyah taşlarda yukarı yönlü hareketlerine bakma
        else:
            for direction in self.__directions:
                if direction[0] != -1:
                    move = self._discover_move(square, direction)
                    if move:
                        moves.append(move)
        
        return moves
        
    
    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        
        

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        #initialize variables
        flips = [origin]

        for x, y in Board._increment_move(origin, direction, self.n):
            #print(x,y)
            if self[x][y] == 0:
                return []
            if self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == color and len(flips) > 0:
                #print(flips)
                return flips

        return []

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move=list(map(sum,zip(move,direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

    

        
        
        