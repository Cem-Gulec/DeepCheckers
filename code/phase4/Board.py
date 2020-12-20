
class Board():
    
    # Türk daması board initial state
    __bitboard     = 0x00ffff0000ffff00

    # saldırı hamleleri üzerinde denemek için
    __tmp_bitboard = 0x0000000000000000

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
    ]

    # pawn_attack_table[bölge][index]
    # örnek: pawn_attack_table[beyaz][a5]'da beyaz aşağıda düşünülürse a5'in boardun
    # yukarı tarafına yapacağı saldırı hamlelerini tutar 
    # Hem siyah hem beyaz için tüm saldırı hamlelerini içeren look-up table
    # bölge(0): beyaz, bölge(1): siyah
    # MxN = 2x64
    pawn_attack_table = [ [0] * 64 for _ in range(2)]

    # Bu sütunları tutmadaki amaç kenar noktalarını belirleyerek
    # kenarı aşarak başka taşı yemesini engellemek
    # örneğin a_column: 
    # 8  0 0 0 0 0 0 0 0  
    # 7  0 1 1 1 1 1 1 1    
    # 6  0 1 1 1 1 1 1 1   
    # 5  0 0 0 0 0 0 0 0   
    # 4  0 0 0 0 0 0 0 0    
    # 3  0 1 1 1 1 1 1 1    
    # 2  0 1 1 1 1 1 1 1    
    # 1  0 0 0 0 0 0 0 0  
    a_column = 0xfefefefefefefefe
    h_column = 0x7f7f7f7f7f7f7f7f
    
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
    # belki set olayını yaparken işleri kolaylaştırır
    def get_enum_index(self, label):
        return self.positions.index(label)

    # Belirlenen square taş koy
    def set_square(self, index):
        self.__bitboard |= (0x1 << index)

    # Saldırı hamlesi için belirtilen pozisyonları
    # boş tahtada set etmek için
    def set_square_atk(self, index):
        self.__tmp_bitboard |= (0x1 << index)

    # Belirlenen squaredeki taşı sil
    def pop_square(self, index):
        # Taşın olup olmadığını konrol et
        if self.get_square(index):
            self.__bitboard ^= (0x1 << index)
        else: 0

    # Look-up table'i generate ettiğimiz hamlelerle doldurmak için
    def init_attack_table(self):
        for index in reversed(range(64)):  
            self.pawn_attack_table[0][index] = self.generate_pawn_attack(0, index)
            self.pawn_attack_table[1][index] = self.generate_pawn_attack(1, index)

    # eğer kuralları ihlal etmediyse (kenarlara denk gelebilir)
    # saldırabileceği 1 veya 2 pozisyonu return eder
    def generate_pawn_attack(self, side, index):
        # ilk başta boş gerekli hamlelerle doldurulacak
        __attacks = 0x0000000000000000
        
        # ilk olarak indexi boarda koy 
        self.set_square_atk(index)

        # Beyaz hamle
        if(not side):
            # Sağ sütunu aşıp aşmadığını kontrol et
            # Eğer sorun yoksa sağ tarafa hamle yapabilir
            if (self.__tmp_bitboard << 7) & self.h_column: 
                __attacks |= (self.__tmp_bitboard << 7)
            # Sol sütunu aşıp aşmadığını kontrol et
            # Eğer sorun yoksa sol tarafa hamle yapabilir
            if (self.__tmp_bitboard << 9) & self.a_column: 
                __attacks |= (self.__tmp_bitboard << 9)
        
        # Siyah hamle
        else:
            if (self.__tmp_bitboard >> 7) & self.a_column: 
                __attacks |= (self.__tmp_bitboard >> 7)
            if (self.__tmp_bitboard >> 9) & self.h_column: 
                __attacks |= (self.__tmp_bitboard >> 9)


        return __attacks

    # Asıl bitboard'un nasıl gözüktüğünü print etmek için
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

    # Asıl board dışında bir hamlenin board yapısında nasıl
    # gözükeceğini print etmek için
    def print_attack_OnBoard(self, attack):
        
        print("\n")
        
        for i in reversed(range(8)):
            for j in range(8):
                
                # SOl taraftaki board indexlerini yaz
                if not j:
                    print(i+1, end = "  ")
                
                # Square'in locationu, bit olarak hesaplanıyor
                square = i * 8 + j
                # Square'de taş varsa 1, yoksa 0 yaz
                print(1 if (attack & (0x1 << square)) else 0, end = " ")  
    
            print("\n")
        print("   a b c d e f g h\n\n")

    

       

if __name__ == "__main__":        
    board = Board()
    board.print_bitboard()
    index_deneme = board.get_enum_index("d2")
    #board.set_square(index_deneme)
    #board.pop_square(index_deneme)

    # Beyaz a5 saldırıyor. Buna göre saldırabileceği pozisyonlar
    board.print_attack_OnBoard(board.generate_pawn_attack(0, index_deneme))