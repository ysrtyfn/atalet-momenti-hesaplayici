from Nokta import Nokta
from Sekil import Sekil
from SekilTipi import SekilTipi

"""İlk 2 nokta taban doğrusunu tanımlar"""
"""                                  """
"""                *                 """
"""              *   *               """
"""        a   *       *   c         """
"""          *           *           """
"""        *               *         """
"""      *  **************   *       """
"""               b                  """
"""                                  """


class Ucgen(Sekil):
    def __init__(self, malzeme_eklenecek_mi, kose_1, kose_2, kose_3):
        super().__init__(malzeme_eklenecek_mi)

        self.SEKIL_TIPI = SekilTipi.UCGEN
        self.MALZEME_EKLENECEK_MI = malzeme_eklenecek_mi
        self.KOSE_1 = kose_1
        self.KOSE_2 = kose_2
        self.KOSE_3 = kose_3

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
        elif self.KOSE_3.X != sekil.KOSE_3.X:
            ayni_mi = False
        elif self.KOSE_3.Y != sekil.KOSE_3.Y:
            ayni_mi = False
        elif self.MALZEME_EKLENECEK_MI != sekil.MALZEME_EKLENECEK_MI:
            ayni_mi = False

        return ayni_mi

    def listede_var_mi(self, sekil_listesi):
        sekil_listede_var_mi = False
        for sekil in sekil_listesi:
            if sekil.SEKIL_TIPI != SekilTipi.UCGEN:
                continue
            elif self.karsilastir(sekil):
                sekil_listede_var_mi = True

        return sekil_listede_var_mi

    def _em_hesapla(self):
        self.CoM_X = (self.KOSE_1.X + self.KOSE_2.X + self.KOSE_3.X) / 3
        self.CoM_Y = (self.KOSE_1.Y + self.KOSE_2.Y + self.KOSE_3.Y) / 3

        taban_dogrusu_orta_nokta = Nokta((self.KOSE_1.X + self.KOSE_2.X) / 2, (self.KOSE_1.Y + self.KOSE_2.Y) / 2)
        self.M = (self.KOSE_2.Y - self.KOSE_1.Y) / (self.KOSE_2.X - self.KOSE_1.X)
        self.N = self.KOSE_1.Y - self.M * self.KOSE_1.X
        self.B = ((self.KOSE_2.Y - self.KOSE_1.Y) ** 2 + (self.KOSE_2.X - self.KOSE_1.X) ** 2) ** 0.5
        self.H = abs((self.KOSE_2.Y - self.KOSE_1.Y) * self.KOSE_3.X - (self.KOSE_2.X - self.KOSE_1.X) * self.KOSE_3.Y +
                     self.KOSE_2.X * self.KOSE_1.Y - self.KOSE_2.Y * self.KOSE_1.X) / self.B
        # TODO aşağıdaki formüller taban eğimli ise geçerli olmaz
        self.S = self.KOSE_3.X - self.KOSE_1.X
        self.T = self.KOSE_2.X - self.KOSE_3.X

        self.ALAN = self.B * self.H / 2

        self.Ix = self.B * (self.H ** 3) / 36
        self.Iy = self.H * self.B * (self.B ** 2 - self.S * self.T) / 36

    def yazdir(self):
        print("\nMALZEME_EKLENECEK_MI: " + str(self.MALZEME_EKLENECEK_MI) +
              "\nKOSE_1: " + str(self.KOSE_1) +
              "\nKOSE_2: " + str(self.KOSE_2) +
              "\nKOSE_3: " + str(self.KOSE_3) +
              "\nCoM_X: " + str(self.CoM_X) +
              "\nCoM_Y: " + str(self.CoM_Y) +
              "\nALAN: " + str(self.ALAN) +
              "\nIx: " + str(self.Ix) +
              "\nIy: " + str(self.Iy) +
              "\nM: " + str(self.M) +
              "\nN: " + str(self.N) +
              "\nB: " + str(self.B) +
              "\nH: " + str(self.H))
