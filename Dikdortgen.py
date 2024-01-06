import math

from Sekil import Sekil
from SekilTipi import SekilTipi


class Dikdortgen(Sekil):
    def __init__(self, malzeme_eklenecek_mi, kose_1, kose_2):
        super().__init__(malzeme_eklenecek_mi)

        self.SEKIL_TIPI = SekilTipi.DIKDORTGEN
        self.MALZEME_EKLENECEK_MI = malzeme_eklenecek_mi
        self.KOSE_1 = kose_1
        self.KOSE_2 = kose_2

        if kose_1.X < kose_2.X:
            self.CoM_X = kose_1.X + abs(kose_2.X - kose_1.X) / 2
            self.GENISLIK = kose_2.X - kose_1.X
        else:
            self.CoM_X = kose_2.X + abs(kose_1.X - kose_2.X) / 2
            self.GENISLIK = kose_1.X - kose_2.X

        if kose_1.Y < kose_2.Y:
            self.CoM_Y = kose_1.Y + abs(kose_2.Y - kose_1.Y) / 2
            self.YUKSEKLIK = kose_2.Y - kose_1.Y
        else:
            self.CoM_Y = kose_2.Y + abs(kose_1.Y - kose_2.Y) / 2
            self.YUKSEKLIK = kose_1.Y - kose_2.Y

        if self.GENISLIK == 0 or self.YUKSEKLIK == 0:
            # TODO kontrol eklenecek
            print("Dikdörtgen genişliği yada yüksekliği sıfır olamaz!")
        else:
            self.ALAN = self.GENISLIK * self.YUKSEKLIK

        self._em_hesapla()

    def karsilastir(self, sekil):
        ayni_mi = True
        if self.KOSE_1.X != sekil.KOSE_1.X:
            ayni_mi = False
        elif self.KOSE_1.Y != sekil.KOSE_1.Y:
            ayni_mi = False
        elif self.KOSE_2.X != sekil.KOSE_2.X:
            ayni_mi = False
        elif self.KOSE_2.Y != sekil.KOSE_2.Y:
            ayni_mi = False
        elif self.MALZEME_EKLENECEK_MI != sekil.MALZEME_EKLENECEK_MI:
            ayni_mi = False

        return ayni_mi

    def listede_var_mi(self, sekil_listesi):
        sekil_listede_var_mi = False
        for sekil in sekil_listesi:
            if sekil.SEKIL_TIPI != SekilTipi.DIKDORTGEN:
                continue
            elif self.karsilastir(sekil):
                sekil_listede_var_mi = True

        return sekil_listede_var_mi

    def _em_hesapla(self):
        self.Ix = self.GENISLIK * (self.YUKSEKLIK ** 3) / 12
        self.Iy = self.YUKSEKLIK * (self.GENISLIK ** 3) / 12
        self.Ip = self.Ix + self.Iy

    def yazdir(self):
        print("\nMALZEME_EKLENECEK_MI: " + str(self.MALZEME_EKLENECEK_MI) +
              "\nKOSE_1: " + str(self.KOSE_1) +
              "\nKOSE_2: " + str(self.KOSE_2) +
              "\nCoM_X: " + str(self.CoM_X) +
              "\nCoM_Y: " + str(self.CoM_Y) +
              "\nGENISLIK: " + str(self.GENISLIK) +
              "\nYUKSEKLIK: " + str(self.YUKSEKLIK) +
              "\nALAN: " + str(self.ALAN) +
              "\nIx: " + str(self.Ix) +
              "\nIy: " + str(self.Iy) +
              "\nIp: " + str(self.Ip))
