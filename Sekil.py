from SekilTipi import SekilTipi


class Sekil:
    def __init__(self, malzeme_eklenecek_mi):
        # Hesaplanacak
        self.Ip = 0
        self.Ix = 0
        self.Iy = 0

        self.ID_TREEVIEW = 0
        self.SEKIL_TIPI = SekilTipi.TEMEL
        self.MALZEME_EKLENECEK_MI = True
        self.ALAN = 0
        self.CoM_X = 0
        self.CoM_Y = 0

    def _em_hesapla(self):
        pass
