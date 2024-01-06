from Sekil import Sekil
from SekilTipi import SekilTipi


class Elips(Sekil):
    def __init__(self, malzeme_eklenecek_mi, merkez_nokta, yaricap_1, yaricap_2, dilim_bas, dilim_son):
        super().__init__(malzeme_eklenecek_mi)

        self.SEKIL_TIPI = SekilTipi.ELIPS
        self.MALZEME_EKLENECEK_MI = malzeme_eklenecek_mi
        self.MERKEZ_NOKTA = merkez_nokta
        self.YARICAP_1 = yaricap_1
        self.YARICAP_2 = yaricap_2
        self.DILIM_BAS = dilim_bas
        self.DILIM_SON = dilim_son

    def yazdir(self):
        print("\nMALZEME_EKLENECEK_MI: " + str(self.MALZEME_EKLENECEK_MI) +
              "\nMERKEZ_NOKTA: " + str(self.MERKEZ_NOKTA) + 
              "\nYARICAP_1: " + str(self.YARICAP_1) + 
              "\nYARICAP_2: " + str(self.YARICAP_2) + 
              "\nDILIM_BAS: " + str(self.DILIM_BAS) + 
              "\nDILIM_SON: " + str(self.DILIM_SON))
