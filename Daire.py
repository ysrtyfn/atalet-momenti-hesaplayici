import math

from Sekil import Sekil


# TODO açı ile hesaplamalar yapılacak
from SekilTipi import SekilTipi


class Daire(Sekil):
    def __init__(self, malzeme_eklenecek_mi, merkez_nokta, yaricap, dilim_bas, dilim_son):
        super().__init__(malzeme_eklenecek_mi)

        self.SEKIL_TIPI = SekilTipi.DAIRE
        self.MALZEME_EKLENECEK_MI = malzeme_eklenecek_mi
        self.MERKEZ_NOKTA = merkez_nokta
        self.YARICAP = yaricap
        self.DILIM_BAS = dilim_bas
        self.DILIM_SON = dilim_son

        self.CoM_X_1 = 0
        self.CoM_Y_1 = 0
        self.CoM_X_2 = 0
        self.CoM_Y_2 = 0
        self.CoM_X_3 = 0
        self.CoM_Y_3 = 0
        self.CoM_X_4 = 0
        self.CoM_Y_4 = 0

        self.CEYREK_1_AKTIF = False
        self.CEYREK_2_AKTIF = False
        self.CEYREK_3_AKTIF = False
        self.CEYREK_4_AKTIF = False

        if dilim_bas == dilim_son:
            # TODO kontrol eklenecek
            print("DILIM_BAS ve DILIM_SON eşit olamaz!")

        if dilim_bas % 90 != 0:
            # TODO kontrol eklenecek
            print("DILIM_BAS tanımı hatalı!")

        if dilim_son % 90 != 0:
            # TODO kontrol eklenecek
            print("DILIM_SON tanımı hatalı!")

        if self.YARICAP == 0:
            # TODO kontrol eklenecek
            print("Daire yarıçapı 0 olamaz!")
        else:
            self.ALAN_CEYREK = math.pi * (self.YARICAP ** 2) / 4
            daire_acisi = dilim_son - dilim_bas
            if daire_acisi == 90:
                self.ALAN = self.ALAN_CEYREK
                if dilim_bas == 0:
                    self.CEYREK_1_AKTIF = True
                elif dilim_bas == 90:
                    self.CEYREK_2_AKTIF = True
                elif dilim_bas == 180:
                    self.CEYREK_3_AKTIF = True
                elif dilim_bas == 270:
                    self.CEYREK_4_AKTIF = True

            elif daire_acisi == 180:
                self.ALAN = self.ALAN_CEYREK * 2
                if dilim_bas == 0:
                    self.CEYREK_1_AKTIF = True
                    self.CEYREK_2_AKTIF = True
                elif dilim_bas == 90:
                    self.CEYREK_2_AKTIF = True
                    self.CEYREK_3_AKTIF = True
                elif dilim_bas == 180:
                    self.CEYREK_3_AKTIF = True
                    self.CEYREK_4_AKTIF = True
                elif dilim_bas == 270:
                    self.CEYREK_4_AKTIF = True
                    self.CEYREK_1_AKTIF = True

            elif daire_acisi == 270:
                self.ALAN = self.ALAN_CEYREK * 3
                if dilim_bas == 0:
                    self.CEYREK_1_AKTIF = True
                    self.CEYREK_2_AKTIF = True
                    self.CEYREK_3_AKTIF = True
                elif dilim_bas == 90:
                    self.CEYREK_2_AKTIF = True
                    self.CEYREK_3_AKTIF = True
                    self.CEYREK_4_AKTIF = True
                elif dilim_bas == 180:
                    self.CEYREK_3_AKTIF = True
                    self.CEYREK_4_AKTIF = True
                    self.CEYREK_1_AKTIF = True
                elif dilim_bas == 270:
                    self.CEYREK_4_AKTIF = True
                    self.CEYREK_1_AKTIF = True
                    self.CEYREK_2_AKTIF = True

            elif daire_acisi == 360:
                self.ALAN = self.ALAN_CEYREK * 4
                self.CEYREK_1_AKTIF = True
                self.CEYREK_2_AKTIF = True
                self.CEYREK_3_AKTIF = True
                self.CEYREK_4_AKTIF = True

        self._em_hesapla()

    def karsilastir(self, sekil):
        ayni_mi = True
        if self.MERKEZ_NOKTA.X != sekil.MERKEZ_NOKTA.X:
            ayni_mi = False
        elif self.MERKEZ_NOKTA.Y != sekil.MERKEZ_NOKTA.Y:
            ayni_mi = False
        elif self.YARICAP != sekil.YARICAP:
            ayni_mi = False
        elif self.DILIM_BAS != sekil.DILIM_BAS:
            ayni_mi = False
        elif self.DILIM_SON != sekil.DILIM_SON:
            ayni_mi = False
        elif self.MALZEME_EKLENECEK_MI != sekil.MALZEME_EKLENECEK_MI:
            ayni_mi = False

        return ayni_mi

    def listede_var_mi(self, sekil_listesi):
        sekil_listede_var_mi = False
        for sekil in sekil_listesi:
            if sekil.SEKIL_TIPI != SekilTipi.DAIRE:
                continue
            elif self.karsilastir(sekil):
                sekil_listede_var_mi = True

        return sekil_listede_var_mi

    def _em_hesapla(self):
        ceyrek_merkezi_kenar_mesafe = (4 * self.YARICAP) / (3 * math.pi)
        self.Ix_CEYREK = math.pi * (self.YARICAP ** 4) / 16 - self.ALAN_CEYREK * (ceyrek_merkezi_kenar_mesafe ** 2)
        self.Iy_CEYREK = math.pi * (self.YARICAP ** 4) / 16 - self.ALAN_CEYREK * (ceyrek_merkezi_kenar_mesafe ** 2)
        self.Ip_CEYREK = self.Ix_CEYREK + self.Iy_CEYREK

        if self.CEYREK_1_AKTIF:
            self.CoM_X_1 = self.MERKEZ_NOKTA.X + ceyrek_merkezi_kenar_mesafe
            self.CoM_Y_1 = self.MERKEZ_NOKTA.Y + ceyrek_merkezi_kenar_mesafe

        if self.CEYREK_2_AKTIF:
            self.CoM_X_2 = self.MERKEZ_NOKTA.X - ceyrek_merkezi_kenar_mesafe
            self.CoM_Y_2 = self.MERKEZ_NOKTA.Y + ceyrek_merkezi_kenar_mesafe

        if self.CEYREK_3_AKTIF:
            self.CoM_X_3 = self.MERKEZ_NOKTA.X - ceyrek_merkezi_kenar_mesafe
            self.CoM_Y_3 = self.MERKEZ_NOKTA.Y - ceyrek_merkezi_kenar_mesafe

        if self.CEYREK_4_AKTIF:
            self.CoM_X_4 = self.MERKEZ_NOKTA.X + ceyrek_merkezi_kenar_mesafe
            self.CoM_Y_4 = self.MERKEZ_NOKTA.Y - ceyrek_merkezi_kenar_mesafe

        self.CoM_X = ((self.CoM_X_1 + self.CoM_X_2 + self.CoM_X_3 + self.CoM_X_4) * self.ALAN_CEYREK) / self.ALAN
        self.CoM_Y = ((self.CoM_Y_1 + self.CoM_Y_2 + self.CoM_Y_3 + self.CoM_Y_4) * self.ALAN_CEYREK) / self.ALAN

        if self.CEYREK_1_AKTIF:
            self.Ix = self.Ix + self.Ix_CEYREK + self.ALAN_CEYREK * ((self.CoM_Y - self.CoM_Y_1) ** 2)
            self.Iy = self.Iy + self.Iy_CEYREK + self.ALAN_CEYREK * ((self.CoM_X - self.CoM_X_1) ** 2)

        if self.CEYREK_2_AKTIF:
            self.Ix = self.Ix + self.Ix_CEYREK + self.ALAN_CEYREK * ((self.CoM_Y - self.CoM_Y_2) ** 2)
            self.Iy = self.Iy + self.Iy_CEYREK + self.ALAN_CEYREK * ((self.CoM_X - self.CoM_X_2) ** 2)

        if self.CEYREK_3_AKTIF:
            self.Ix = self.Ix + self.Ix_CEYREK + self.ALAN_CEYREK * ((self.CoM_Y - self.CoM_Y_3) ** 2)
            self.Iy = self.Iy + self.Iy_CEYREK + self.ALAN_CEYREK * ((self.CoM_X - self.CoM_X_3) ** 2)

        if self.CEYREK_4_AKTIF:
            self.Ix = self.Ix + self.Ix_CEYREK + self.ALAN_CEYREK * ((self.CoM_Y - self.CoM_Y_4) ** 2)
            self.Iy = self.Iy + self.Iy_CEYREK + self.ALAN_CEYREK * ((self.CoM_X - self.CoM_X_4) ** 2)

        self.Ip = self.Ix + self.Iy

    def yazdir(self):
        print("\nMALZEME_EKLENECEK_MI: " + str(self.MALZEME_EKLENECEK_MI) +
              "\nMERKEZ_NOKTA: " + str(self.MERKEZ_NOKTA) +
              "\nYARICAP: " + str(self.YARICAP) +
              "\nCoM_X: " + str(self.CoM_X) +
              "\nCoM_Y: " + str(self.CoM_Y) +
              "\nIx_CEYREK: " + str(self.Ix_CEYREK) +
              "\nIy_CEYREK: " + str(self.Iy_CEYREK) +
              "\nIx: " + str(self.Ix) +
              "\nIy: " + str(self.Iy) +
              "\nDILIM_BAS: " + str(self.DILIM_BAS) +
              "\nDILIM_SON: " + str(self.DILIM_SON) +
              "\nALAN: " + str(self.ALAN) +
              "\nALAN_CEYREK: " + str(self.ALAN_CEYREK) +
              "\nCEYREK_1_AKTIF: " + str(self.CEYREK_1_AKTIF) +
              "\nCEYREK_2_AKTIF: " + str(self.CEYREK_2_AKTIF) +
              "\nCEYREK_3_AKTIF: " + str(self.CEYREK_3_AKTIF) +
              "\nCEYREK_4_AKTIF: " + str(self.CEYREK_4_AKTIF))
