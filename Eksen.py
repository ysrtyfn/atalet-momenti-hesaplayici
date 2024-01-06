import math

from Sekil import Sekil
from SekilTipi import SekilTipi


class Eksen(Sekil):
    def __init__(self, kose_1, kose_2):
        super().__init__(False)

        self.SEKIL_TIPI = SekilTipi.EKSEN
        self.KOSE_1 = kose_1
        self.KOSE_2 = kose_2

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

        return ayni_mi

    def listede_var_mi(self, eksen_listesi):
        eksen_listede_var_mi = False
        for eksen in eksen_listesi:
            if eksen.SEKIL_TIPI != SekilTipi.EKSEN:
                continue
            elif self.karsilastir(eksen):
                eksen_listede_var_mi = True

        return eksen_listede_var_mi

    def yazdir(self):
        print("\nKOSE_1: " + str(self.KOSE_1) +
              "\nKOSE_2: " + str(self.KOSE_2))
