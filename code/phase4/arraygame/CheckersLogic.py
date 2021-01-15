
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
    # -1, 0     ==>  Alt tarafa doğru, aşağıya hamle yönü
    #  1, 0     ==>  Üst tarafa doğru, yukarıya hamle yönü
    #  0, 1     ==>  Yan tarafa doğru, sağ tarafa hamsle yönü
    #  0, -1    ==>  Yan tarafa doğru, sol tarafa hamle yönü
    #  -1, 1     ==>  Sağ aşağı yönlü, çapraz saldırma hareketi
    #  -1, -1    ==>  Sol aşağı yönlü, çapraz saldırma hareketi
    # 1, 1     ==>  Sağ yukarı yönlü, çapraz saldırma hareketi
    # 1, -1    ==>  Sol yukarı yönlü, çapraz saldırma hareketi
    __move_directions = [(-1,0), (1,0), (0,1), (0,-1)]
    __attack_directions = [(-1,1), (-1,-1), (1,1), (1,-1)]
    
    # N burada boardın size'ını belirlemek için, default olarak 8
    def __init__(self, n=8):
        
        self.n = n
        self.capture_move = False
        
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
        self.pieces[6] = [-1] * self.n
        self.pieces[5] = [-1] * self.n
        
        self.pieces[4][2] = 1
        # Beyaz taşlar
        self.pieces[2] = [1] * self.n
        self.pieces[1] = [1] * self.n
    
    def __getitem__(self, index): 
        return self.pieces[index]
    
    def get_legal_moves(self, color):
        # returns all the legal moves
        moves = set()   # stores the legal moves
        
        for x in range(self.n):
            for y in range(self.n):
                if self[x][y] == color:
                    newmoves = self.get_moves_for_square((x, y))
                    if self.capture_move:
                        moves.clear()
                        moves.update(newmoves)
                    moves.update(newmoves)
        
        return list(moves)
    
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
        
        # ilk başta attack var mı ona bakmalı, varsa onu dön yoksa forward moveları dön
        if color == 1: # Beyaz taşların sırasıysa        
            for attk in self.__attack_directions[-2:]:
                move = self._discover_move(square, attk)
                if move and (self[move[0]][move[1]] == -1):
                    moves.append(move)
        else:  # Siyah taşların sırasıysa
            for attk in self.__attack_directions[:2]:
                move = self._discover_move(square, attk)
                if move and (self[move[0]][move[1]] == 1):
                    moves.append(move)
        
        # Eğer attack hamlesi varsa sadece onlardan yapmalı 
        if len(moves) > 0:
            self.capture_move = True
            return moves
        
        
        self.capture_move = False
        # Eğer attack hamleleri yoksa, geriye gitme hareketinden başka diğer hamleleri yapabilmeli
        if color == 1:
            for direction in self.__move_directions[1:]:
                move = self._discover_move(square, direction)
                if move:
                    moves.append(move)
        else:
            for direction in self.__move_directions:
                if direction == (1, 0):    # Siyahta geri hamleyi atla
                    continue
                move = self._discover_move(square, direction)
                if move:
                    moves.append(move)
        
        return moves
        
    
    def execute_forward_move(self, square, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        (src_x, src_y) = square
        (dest_x, dest_y) = move
        
        assert self[src_x][src_y] == color
        assert self[dest_x][dest_y] == 0
        self[src_x][src_y] = 0
        self[dest_x][dest_y] = color
        
    def execute_capture_move(self, square, move, color):
        
        (src_x, src_y) = square
        (dest_x, dest_y) = move
        
        assert self[src_x][src_y] == color
        assert self[dest_x][dest_y] == -color
        self[src_x][src_y] = 0
        self[dest_x][dest_y] = color
        

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        color = self[x][y]
        
        for x, y in Board._increment_move(origin, direction, self.n):
            if color == self[x][y]:
                return None
            elif self[x][y] == 0:
                return (x, y)
            elif self[x][y] == -color:
                return (x, y)
            #if self[x][y]:
            #    print("Burasi neresi {}", self[x][y])
            #    return None
            #elif self[x][y] == color:
            #    return None


    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        
        if 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
        #move = (move[0]+direction[0], move[1]+direction[1])
        #while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
        #    print(move)
        #    yield move
        #    move=list(map(sum,zip(move,direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

    
    def display(self):
        
        for x in range(self.n-1, -1, -1):
            print(x+1, "|",end="")
            for y in range(self.n):
                piece = board[x][y]    
                if piece == -1: print("x ",end="")      # siyah
                elif piece == 1: print("o ",end="")     # beyaz
                elif piece == -3: print("X ",end="")    # siyah king
                elif piece == 3: print("O ",end="")     # beyaz king
                else:
                    if x==self.n:
                        print("-",end="")
                    else:
                        print("- ",end="")
            print("|")
    
        print("  ------------------")
        
board = Board(8)   
print(board.get_legal_moves(1))    
board.execute_capture_move((5,1) ,(4, 2), -1)
board.display()
print(board.get_legal_moves(-1))         