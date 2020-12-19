
class Board():
    
    # Türk daması board initial state
    __bitboard = 0x00ffff0000ffff00

    # sayı-harf pozisyon labelları
    positions = [
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'
    ];

    
    def __init__(self):
        
        # Bunlar genel olarak kullanılabilir, dursun şurada
        self.BP = 0x00ffff0000000000    # Normal Siyah taşlar
        self.BK = 0x0                   # Black Dama Olmuş Taşları 
        self.WP = 0xffff00              # Normal Beyaz taşlar
        self.WK = 0x0                   # White Dama Olmuş Taşları
        
    # Şimdilik o square değeri yerine orda belli bir taş varsa 1 dön, yoksa 0
    # ilerideki aşamalarda bunu taşın değeri olarak döndürülebilir
    def get_square(self, index):
        return 1 if (self.__bitboard & (0x1 << index)) else 0
    
    # girilen labela göre pozisyon indexini döndürür
    def get_enum_index(self, label):
        return self.positions.index(label)

    # Belirlenen square taş koy
    def set_square(self, index):
        self.__bitboard |= (0x1 << index)
    
    def print_bitboard(self):
        
        print("\n")
        
        for i in reversed(range(8)):
            for j in range(8):
                
                # SOl taraftaki board indexlerini yaz
                if not j:
                    print(i+1, end = "  ")
                
                # Square'in locationu, bit olarak hesaplanıyor
                square = i * 8 + j
                # Square'de taş varsa 1, yoksa 0 yaz
                print(1 if (self.__bitboard & (0x1 << square)) else 0, end = " ")  
    
            print("\n")
        print("   a b c d e f g h\n\n")
        

if __name__ == "__main__":        
    board = Board()
    board.print_bitboard()
    print("Square 0'in eski degeri : ", board.get_square(0))
    index_deneme = board.get_enum_index("c4")
    print(index_deneme)
    board.set_square(index_deneme)
    print("Square 0'in yeni degeri : ", board.get_square(0))
    print("\n\n Yeni square 0 ile board : ")
    board.print_bitboard()