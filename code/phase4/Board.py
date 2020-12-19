
class Board():
    
    # Türk daması board initial state
    __bitboard = 0x00ffff0000ffff00
    
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
    
    # Belirlenen square taş koy
    def set_square(self, index):
        self.__bitboard |= (0x1 << index)
    
    def print_bitboard(self):
        
        print("\n")
        
        for i in reversed(range(8)):
            for j in range(8):
                
                # SOl taraftaki board indexlerini yaz
                if not j:
                    print(i+1, end = " ")
                
                # Square'in locationu, bit olarak hesaplanıyor
                square = i * 8 + j
                # Square'de taş varsa 1, yoksa 0 yaz
                print(1 if (self.__bitboard & (0x1 << square)) else 0, end = " ")  
    
            print("\n")
        print("  a b c d e f g h\n\n")
        
board = Board()
board.print_bitboard()
print("Square 0'in eski degeri : ", board.get_square(0))
board.set_square(0)
print("Square 0'in yeni degeri : ", board.get_square(0))
print("\n\n Yeni square 0 ile board : ")
board.print_bitboard()