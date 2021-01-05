
# Oyunun kuralları :

# Toplamda 5 tane bitboard olacak, bunlar : 
# Beyeaz Pawn   : Normal ilerleyen taşlar
# Beyaz King    : Bunlar Dama olmuş beyaz taşlar
# Siyah Pawn    : Normal ilerleyen taşlar
# Siyah King    : Bunlar Dama olmuş siyah taşlar   
# Büyük Board   : Bunların hepsini içeren oyunun oynandığı board

# Side == 1     : Sıra Beyazda (Player1),
# Side == -1    : Sıra Siyahta (Player2);

# Occupancies ile alakalı 3 board olacak:
# Beyaz occupancy   : Bu bitboardda Beyaz taşların nerede olduğu 
# Siyah occupancy   : Bu bitboardda Siyah taşların nerede olduğu 
# All occupancy     : Bu bitboardda bütün taşların nerede olduğu 


import logging
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)


class Board():
    
    # Türk daması board initial state
    __bitboard     = 0x00ffff0000ffff00

    # saldırı hamleleri üzerinde denemek için
    __tmp_bitboard = 0x0000000000000000
    
                        # Tahtanın Represent Edilmesi İçin gerekli Bitboardlar
    
    #  Beyaz Pawn Taşları 'P' Tahtası                       Beyazın b8 de dama taşı olduğunu varsayarsak 'K' tahtasının son hali
    #   8  0 0 0 0 0 0 0 0                                                  8  0 1 0 0 0 0 0 0    
    #   7  0 0 0 0 0 0 0 0                                                  7  0 0 0 0 0 0 0 0  
    #   6  0 0 0 0 0 0 0 0                                                  6  0 0 0 0 0 0 0 0  
    #   5  0 0 0 0 0 0 0 0                                                  5  0 0 0 0 0 0 0 0  
    #   4  0 0 0 0 0 0 0 0                                                  4  0 0 0 0 0 0 0 0  
    #   3  1 1 1 1 1 1 1 1                                                  3  0 0 0 0 0 0 0 0  
    #   2  1 1 1 1 1 1 1 1                                                  2  0 0 0 0 0 0 0 0  
    #   1  0 0 0 0 0 0 0 0                                                  1  0 0 0 0 0 0 0 0  
    #      a b c d e f g h                                                     a b c d e f g h
    #   HEX : 0x0000000000ffff00
    #
    #  Siyah Pawn Taşları 'p' Tahtası                       Siyahın d4 de dama taşı olduğunu varsayarsak 'k' tahtasının son hali
    #   8  0 0 0 0 0 0 0 0                                                  8  0 0 0 0 0 0 0 0    
    #   7  1 1 1 1 1 1 1 1                                                  7  0 0 0 0 0 0 0 0  
    #   6  1 1 1 1 1 1 1 1                                                  6  0 0 0 0 0 0 0 0  
    #   5  0 0 0 0 0 0 0 0                                                  5  0 0 0 0 0 0 0 0  
    #   4  0 0 0 0 0 0 0 0                                                  4  0 0 0 1 0 0 0 0  
    #   3  0 0 0 0 0 0 0 0                                                  3  0 0 0 0 0 0 0 0  
    #   2  0 0 0 0 0 0 0 0                                                  2  0 0 0 0 0 0 0 0  
    #   1  0 0 0 0 0 0 0 0                                                  1  0 0 0 0 0 0 0 0  
    #      a b c d e f g h                                                     a b c d e f g h
    #    HEX = 0x00ffff0000000000
    
    __Pboard = 0x0000000000ffff00   # Beyaz pawn taşları initial state
    __Kboard = 0x0000000000000000   # Beyaz dama taşları initial state
    __pboard = 0x00ffff0000000000   # Siyah pawn taşları initial state
    __kboard = 0x0000000000000000   # Siyah dama taşları initial state
    
    __allbitboards = [
    __Pboard,              # Burası beyaz piyonları temsil etmekte, 
    __Kboard,              # Burası beyaz dama taşlarını temsil ediyo,  
    __pboard,              # Burası siyah piyonları temsil etmekte, 
    __kboard               # Burası siyah dama taşlarını temsil ediyo
    ]
    
    # Boardın tamamındaki toplam taşların gösterilmesi durumu
    
    #       Beyaz Taşlarının ilk konumda olduklarını tek farkının b4 de dama taşının olduğunu varsayalım,
    #                       White Occupancies Tahtası Reprensente edilmiş hali
    #
    #                           8  0 0 0 0 0 0 0 0  
    #                           7  0 0 0 0 0 0 0 0    
    #                           6  0 0 0 0 0 0 0 0   
    #                           5  0 0 0 0 0 0 0 0   
    #                           4  0 1 0 0 0 0 0 0    
    #                           3  1 0 1 1 1 1 1 1    
    #                           2  1 1 1 1 1 1 1 1    
    #                           1  0 0 0 0 0 0 0 0  
    #                              a b c d e f g h
    # 
    #       Aynı mantıkla siyahın bütün taşlarını barındıran bir board 'black',
    #       Hem siyahın tüm taşlarını hemde beyazın tüm taşlarını barındıran board 'both'
    
    __whiteocc  = 0x0000000000ffff00    # Beyazın tüm taşları initial statedeyken
    __blackocc  = 0x00ffff0000000000    # Siyahın tüm taşları initial statedeyken
    __bothocc   = 0x00ffff0000ffff00    # İkisininde tüm taşları initial statedeyken
    
    __occupancyboards = [
    __whiteocc,
    __blackocc,
    __bothocc
    ]
    
    # Oynama sırasının kimde olduğunu tutacak variable
    #
    #   side == 1   ==> Oynama sırası Beyaz taşların
    #   side == 0   ==> Oynama sırası Siyah taşların
    __side = 1

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
        
        self.ascii_pieces = ["P","K","p","k"]
        
    # Şimdilik o square değeri yerine orda belli bir taş varsa 1 dön, yoksa 0
    # ilerideki aşamalarda bunu taşın değeri olarak döndürülebilir
    
    def get_square(self, bitboard, index):
        return 1 if (bitboard & (0x1 << index)) else 0
    
    # girilen labela göre pozisyon indexini döndürür
    # belki set olayını yaparken işleri kolaylaştırır
    def get_enum_index(self, label):
        return self.positions.index(label)

    # Belirlenen square taş koy
    def set_square(self, bitboard, index):
        bitboard |= (0x1 << index)
        return bitboard

    # Saldırı hamlesi için belirtilen pozisyonları
    # boş tahtada set etmek için
    def set_square_atk(self, bitboard, index):
        bitboard |= (0x1 << index)

    # Belirlenen squaredeki taşı sil
    def pop_square(self, bitboard, index):
        # Taşın olup olmadığını konrol et
        if self.get_square(bitboard, index):
            bitboard ^= (0x1 << index)
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

    # Verilen indexte hareket ettirebileceğimiz taş
    # olduğunu farz ediyorum
    def forward_move(self, bitboard, side, index):
        # Beyaz hamle
        if (not side):
            move = index + 8
            # Eğer önünde taş yoksa ileri hareket edecek
            if not self.get_square(bitboard, move):
                board.set_square(bitboard, move)
                board.pop_square(bitboard, index)
            else:
                print("not a valid move")

        # Siyah hamle
        else:
            move = index - 8;
            if not self.get_square(bitboard, move):
                board.set_square(bitboard, move)
                board.pop_square(bitboard, index)
            else:
                print("not a valid move")

    # Asıl bitboard'un nasıl gözüktüğünü print etmek için
    def print_bitboard(self, bitboard):
        
        print("\n")
        
        for i in reversed(range(8)):
            for j in range(8):
                
                # SOl taraftaki board indexlerini yaz
                if not j:
                    print(i+1, end = "  ")
                
                # Square'in locationu, bit olarak hesaplanıyor
                square = i * 8 + j
                # Square'de taş varsa 1, yoksa 0 yaz
                print(1 if (bitboard & (0x1 << square)) else 0, end = " ")  
    
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
    
    def print_board(self):
        print("\n")
        
        self.__Pboard = self.set_square(self.__Pboard, self.get_enum_index("e5"))
        self.__allbitboards[0] = self.__Pboard
        self.print_bitboard(self.__Pboard)
        self.print_bitboard(self.__allbitboards[0])
        print(self.get_square(self.__allbitboards[0], self.get_enum_index("e5")))#bitboard & (0x1 << index)
        #TODO: Burada __allbitboards güncellenmiyor, sorunu bulmak lazım
        
        for i in reversed(range(8)):
            for j in range(8):
                
                # SOl taraftaki board indexlerini yaz
                if not j:
                    print(i+1, end = "  ")
                
                # Square'in locationu, bit olarak hesaplanıyor
                square = i * 8 + j
                
                piece = -1
                
                for k in range(4):
                    if (self.get_square(self.__allbitboards[k], square)):
                        piece = k
                
                print(self.ascii_pieces[piece] if piece != -1 else ".", end=" ")
                
                
            print("\n")
        print("   a b c d e f g h\n\n")
    

       


board = Board()
board.print_board()

#if __name__ == "__main__":        
#    board = Board()
#    board.print_bitboard()
#    index_deneme = board.get_enum_index("h6")
    #board.set_square(index_deneme)
    #board.pop_square(index_deneme)
    # Beyaz a5 saldırıyor. Buna göre saldırabileceği pozisyonlar
    #board.print_attack_OnBoard(board.generate_pawn_attack(0, index_deneme))

#    board.forward_move(1, index_deneme)
#    board.print_bitboard()