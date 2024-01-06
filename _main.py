import os
import pygubu
import math

from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from Eksen import Eksen
from Daire import Daire
from Dikdortgen import Dikdortgen
from Nokta import Nokta
from SekilTipi import SekilTipi
from Ucgen import Ucgen

sekiller = [Dikdortgen(True, Nokta(-18, 0), Nokta(18, 24)),
            Dikdortgen(True, Nokta(-6, 24), Nokta(6, 60)),
            Dikdortgen(True, Nokta(-6, 180), Nokta(6, 216)),
            Dikdortgen(True, Nokta(-85, 216), Nokta(85, 240))]

sekiller2 = [Dikdortgen(True, Nokta(0, 0), Nokta(40, 20)),
             Dikdortgen(True, Nokta(40, 0), Nokta(60, 120)),
             Dikdortgen(True, Nokta(60, 0), Nokta(90, 30)),
             Dikdortgen(True, Nokta(117, 0), Nokta(140, 30))]

sekiller3 = [Dikdortgen(True, Nokta(-50, -100), Nokta(50, 100)),
             Daire(True, Nokta(0, 100), 50, 0, 180),
             Daire(True, Nokta(0, -100), 50, 180, 360)]

sekiller4 = [Dikdortgen(True, Nokta(0, 0), Nokta(200, 200)),
             Ucgen(False, Nokta(0, 200), Nokta(120, 200), Nokta(0, 0)),
             Ucgen(False, Nokta(120, 200), Nokta(200, 200), Nokta(200, 0))]

sekiller5 = [Dikdortgen(True, Nokta(0, 20), Nokta(420, 230)),
             Dikdortgen(False, Nokta(0, 80), Nokta(90, 230)),
             Dikdortgen(False, Nokta(330, 80), Nokta(420, 230)),
             Dikdortgen(False, Nokta(150, 20), Nokta(270, 170)),
             Ucgen(False, Nokta(90, 230), Nokta(150, 230), Nokta(90, 80)),
             Ucgen(False, Nokta(270, 230), Nokta(330, 230), Nokta(330, 80)),
             Ucgen(False, Nokta(90, 20), Nokta(150, 20), Nokta(150, 170)),
             Ucgen(False, Nokta(270, 20), Nokta(330, 20), Nokta(270, 170))]

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "gui_data.ui")


class GuiDataApp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('frame_main')
        builder.connect_callbacks(self)

        self.CANVAS = builder.get_object('cnvs_ana')
        self.SCRBAR_YATAY = builder.get_object('scrbar_yatay')
        self.SCRBAR_DIKEY = builder.get_object('scrbar_dikey')
        self.CANVAS.configure(yscrollcommand=self.SCRBAR_DIKEY.set, xscrollcommand=self.SCRBAR_YATAY.set)
        self.CANVAS.configure(scrollregion=self.CANVAS.bbox("all"))
        self.SCRBAR_YATAY["command"] = self.CANVAS.xview
        self.SCRBAR_DIKEY["command"] = self.CANVAS.yview

        # This is what enables using the mouse:
        self.CANVAS.bind("<ButtonPress-1>", self.move_start)
        self.CANVAS.bind("<B1-Motion>", self.move_move)
        # windows scroll
        # self.CANVAS.bind("<MouseWheel>", self.zoomer)

        self.LBL_EKLENEN_SEKIL = builder.get_object('lbl_eklenen_sekil')
        self.ENTRY_NOKTA1_X = builder.get_object('entry_nokta1_x')
        self.ENTRY_NOKTA1_Y = builder.get_object('entry_nokta1_y')
        self.ENTRY_NOKTA2_X = builder.get_object('entry_nokta2_x')
        self.ENTRY_NOKTA2_Y = builder.get_object('entry_nokta2_y')
        self.ENTRY_NOKTA3_X = builder.get_object('entry_nokta3_x')
        self.ENTRY_NOKTA3_Y = builder.get_object('entry_nokta3_y')
        self.ENTRY_YARICAP1 = builder.get_object('entry_yaricap1')
        self.ENTRY_YARICAP2 = builder.get_object('entry_yaricap2')
        self.LBL_ACI_BAS = builder.get_object('lbl_aci_bas')
        self.LBL_ACI_SON = builder.get_object('lbl_aci_son')
        self.CBOX_ACI_BAS = builder.get_object('cbox_aci_bas')
        self.CBOX_ACI_SON = builder.get_object('cbox_aci_son')
        self.CBTN_MALZEME_EKLENECEK_MI = builder.get_object('cbtn_malzemeEklenecekMI')
        self.LBL_BILGILENDIRME = builder.get_object('lbl_bilgilendirme')
        self.LBL_SONUC = builder.get_object('lbl_sonuc')
        self.TREEVIEW_SEKIL_LISTESI = builder.get_object('treeview_sekil_listesi')

        self.LBL_ACI_BAS["text"] = "Açı Baş"
        self.CBOX_ACI_BAS["values"] = ["0", "90", "180", "270", "360"]
        self.CBOX_ACI_BAS.current(0)
        self.LBL_ACI_SON["text"] = "Açı Son"
        self.CBOX_ACI_SON["values"] = ["0", "90", "180", "270", "360"]
        self.CBOX_ACI_SON.current(4)

        self.TREEVIEW_SEKIL_LISTESI["columns"] = ("nokta", "ekle")
        self.TREEVIEW_SEKIL_LISTESI.column("#0", width=100, minwidth=100, stretch=tk.NO)
        self.TREEVIEW_SEKIL_LISTESI.column("nokta", width=100, minwidth=100, stretch=tk.NO)
        self.TREEVIEW_SEKIL_LISTESI.column("ekle", width=60, minwidth=60, stretch=tk.NO)

        self.TREEVIEW_SEKIL_LISTESI.heading("#0", text="Şekil", anchor=tk.W)
        self.TREEVIEW_SEKIL_LISTESI.heading("nokta", text="Nokta", anchor=tk.W)
        self.TREEVIEW_SEKIL_LISTESI.heading("ekle", text="Ekle?", anchor=tk.W)

        self.CBTN_MALZEME_EKLENECEK_MI.state(['!alternate'])
        self.CBTN_MALZEME_EKLENECEK_MI.state(["selected"])

        self.guncelleEntry(self.ENTRY_NOKTA1_X, "0")
        self.guncelleEntry(self.ENTRY_NOKTA1_Y, "0")
        self.guncelleEntry(self.ENTRY_NOKTA2_X, "0")
        self.guncelleEntry(self.ENTRY_NOKTA2_Y, "0")

        self.EKLENECEK_SEKIL_TIPI = SekilTipi.TEMEL
        self.eksen_listesi = []
        self.sekil_listesi = []

        # TODO deneme kodu
        # self.sekil_listesi = sekiller2

        self.pencere_genisligi = 1024
        self.pencere_yuksekligi = 1024
        self.pencere_genisligi_onda_bir = self.pencere_genisligi / 10
        self.pencere_yuksekligi_onda_bir = self.pencere_yuksekligi / 10
        self.pencere_orta = Nokta(self.pencere_genisligi / 2, self.pencere_yuksekligi / 2)
        self.renk_arkaplan = (50, 50, 50)
        self.renk_center_of_mass = (223, 242, 7)
        self.renk_eksen = (62, 196, 35)
        self.renk_eksen_yazisi = (232, 22, 7)
        self.renk_sekil_ekle = (200, 200, 200)
        self.renk_sekil_cikar = (90, 90, 90)
        self.renk_cizgi_ekle = (20, 20, 20)
        self.renk_cizgi_cikar = (24, 147, 181)
        self.renk_eksen = (50, 168, 82)
        self.cizgi_kalinligi = 1
        self.eksen_kalinligi = 2

        self.sayi_basamak = 2

        self.CENTER_OF_MASS_VISIBLE = False
        self.CENTER_OF_MASS_X = 0
        self.CENTER_OF_MASS_Y = 0
        self.CENTER_OF_MASS_R = 3

        self.image = Image.new("RGBA", (self.pencere_genisligi, self.pencere_yuksekligi), self.renk_arkaplan)
        self.fnt = ImageFont.truetype("hatlar/unispace.ttf", 12)

        self.image_context = ImageDraw.Draw(self.image)

        self.guncelleResim()

    # move
    def move_start(self, event):
        self.CANVAS.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.CANVAS.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if event.delta > 0:
            self.CANVAS.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.CANVAS.scale("all", event.x, event.y, 0.9, 0.9)
        self.CANVAS.configure(scrollregion=self.CANVAS.bbox("all"))

    def run(self):
        self.mainwindow.mainloop()

    def ayarlaOnlukBasamak(self, sayi):
        return '{:.2f}'.format(sayi)

    def yazdirHata(self, yazi, bos_satir):
        self.LBL_BILGILENDIRME["text"] = yazi + "\n" * bos_satir

    def yazdirSonuc(self, yazi, bos_satir):
        self.LBL_SONUC["text"] = yazi + "\n" * bos_satir

    def guncelleEntry(self, entry, yazi):
        entry.delete(0, tk.END)
        entry.insert(0, yazi)

    def gosterEksen_OnClick(self):
        print("gosterEksen_OnClick")

        self.EKLENECEK_SEKIL_TIPI = SekilTipi.EKSEN
        self.LBL_EKLENEN_SEKIL["text"] = "Eksen ekleniyor"
        self.ENTRY_NOKTA1_X["state"] = "normal"
        self.ENTRY_NOKTA1_Y["state"] = "normal"
        self.ENTRY_NOKTA2_X["state"] = "normal"
        self.ENTRY_NOKTA2_Y["state"] = "normal"
        self.ENTRY_NOKTA3_X["state"] = "disabled"
        self.ENTRY_NOKTA3_Y["state"] = "disabled"
        self.ENTRY_YARICAP1["state"] = "disabled"
        self.ENTRY_YARICAP2["state"] = "disabled"
        self.CBOX_ACI_BAS["state"] = "disabled"
        self.CBOX_ACI_SON["state"] = "disabled"
        self.CBTN_MALZEME_EKLENECEK_MI["state"] = "disabled"
        self.CBTN_MALZEME_EKLENECEK_MI.state(['!alternate'])
        self.CBTN_MALZEME_EKLENECEK_MI.state(["selected"])

    def gosterDikdortgen_OnClick(self):
        print("gosterDikdortgen_OnClick")

        self.EKLENECEK_SEKIL_TIPI = SekilTipi.DIKDORTGEN
        self.LBL_EKLENEN_SEKIL["text"] = "Dikdörtgen ekleniyor"
        self.ENTRY_NOKTA1_X["state"] = "normal"
        self.ENTRY_NOKTA1_Y["state"] = "normal"
        self.ENTRY_NOKTA2_X["state"] = "normal"
        self.ENTRY_NOKTA2_Y["state"] = "normal"
        self.ENTRY_NOKTA3_X["state"] = "disabled"
        self.ENTRY_NOKTA3_Y["state"] = "disabled"
        self.ENTRY_YARICAP1["state"] = "disabled"
        self.ENTRY_YARICAP2["state"] = "disabled"
        self.CBOX_ACI_BAS["state"] = "disabled"
        self.CBOX_ACI_SON["state"] = "disabled"
        self.CBTN_MALZEME_EKLENECEK_MI["state"] = "normal"
        self.CBTN_MALZEME_EKLENECEK_MI.state(['!alternate'])
        self.CBTN_MALZEME_EKLENECEK_MI.state(["selected"])

    def gosterDaire_OnClick(self):
        print("gosterDaire_OnClick")

        self.EKLENECEK_SEKIL_TIPI = SekilTipi.DAIRE
        self.LBL_EKLENEN_SEKIL["text"] = "Daire ekleniyor"
        self.ENTRY_NOKTA1_X["state"] = "normal"
        self.ENTRY_NOKTA1_Y["state"] = "normal"
        self.ENTRY_NOKTA2_X["state"] = "disabled"
        self.ENTRY_NOKTA2_Y["state"] = "disabled"
        self.ENTRY_NOKTA3_X["state"] = "disabled"
        self.ENTRY_NOKTA3_Y["state"] = "disabled"
        self.ENTRY_YARICAP1["state"] = "normal"
        self.ENTRY_YARICAP2["state"] = "disabled"
        self.CBOX_ACI_BAS["state"] = "normal"
        self.CBOX_ACI_SON["state"] = "normal"
        self.CBTN_MALZEME_EKLENECEK_MI["state"] = "normal"
        self.CBTN_MALZEME_EKLENECEK_MI.state(['!alternate'])
        self.CBTN_MALZEME_EKLENECEK_MI.state(["selected"])

    def gosterUcgen_OnClick(self):
        print("gosterUcgen_OnClick")

        self.EKLENECEK_SEKIL_TIPI = SekilTipi.UCGEN
        self.LBL_EKLENEN_SEKIL["text"] = "Üçgen ekleniyor"
        self.ENTRY_NOKTA1_X["state"] = "normal"
        self.ENTRY_NOKTA1_Y["state"] = "normal"
        self.ENTRY_NOKTA2_X["state"] = "normal"
        self.ENTRY_NOKTA2_Y["state"] = "normal"
        self.ENTRY_NOKTA3_X["state"] = "normal"
        self.ENTRY_NOKTA3_Y["state"] = "normal"
        self.ENTRY_YARICAP1["state"] = "disabled"
        self.ENTRY_YARICAP2["state"] = "disabled"
        self.CBOX_ACI_BAS["state"] = "disabled"
        self.CBOX_ACI_SON["state"] = "disabled"
        self.CBTN_MALZEME_EKLENECEK_MI["state"] = "normal"
        self.CBTN_MALZEME_EKLENECEK_MI.state(['!alternate'])
        self.CBTN_MALZEME_EKLENECEK_MI.state(["selected"])

    def ekleEksen(self):
        print("ekleEksen")
        nokta1_x = self.ENTRY_NOKTA1_X.get()
        nokta1_y = self.ENTRY_NOKTA1_Y.get()
        nokta2_x = self.ENTRY_NOKTA2_X.get()
        nokta2_y = self.ENTRY_NOKTA2_Y.get()

        try:
            nokta1_x = int(nokta1_x)
            nokta1_y = int(nokta1_y)
            nokta2_x = int(nokta2_x)
            nokta2_y = int(nokta2_y)

            eksen = Eksen(Nokta(int(nokta1_x), int(nokta1_y)), Nokta(int(nokta2_x), int(nokta2_y)))
            if eksen.listede_var_mi(self.eksen_listesi):
                self.yazdirHata("Eksen listede tanımlı", 2)
            else:
                self.eksen_listesi.append(eksen)
                self.guncelleResim()

        except ValueError:
            self.yazdirHata("Lütfen girdileri kontrol ediniz", 2)

    def ekleDikdortgen(self):
        print("ekleDikdortgen")
        nokta1_x = self.ENTRY_NOKTA1_X.get()
        nokta1_y = self.ENTRY_NOKTA1_Y.get()
        nokta2_x = self.ENTRY_NOKTA2_X.get()
        nokta2_y = self.ENTRY_NOKTA2_Y.get()
        malzeme_eklenecek_mi = self.CBTN_MALZEME_EKLENECEK_MI.instate(['selected'])

        try:
            nokta1_x = int(nokta1_x)
            nokta1_y = int(nokta1_y)
            nokta2_x = int(nokta2_x)
            nokta2_y = int(nokta2_y)

            dikdortgen = Dikdortgen(malzeme_eklenecek_mi, Nokta(int(nokta1_x), int(nokta1_y)),
                                    Nokta(int(nokta2_x), int(nokta2_y)))
            if dikdortgen.ALAN <= 0:
                self.yazdirHata("Dikdörtgen tanımı hatalı", 2)
            elif dikdortgen.listede_var_mi(self.sekil_listesi):
                self.yazdirHata("Dikdörtgen listede tanımlı", 2)
            else:
                self.sekil_listesi.append(dikdortgen)
                self.guncelleResim()

        except ValueError:
            self.yazdirHata("Lütfen girdileri kontrol ediniz", 2)

    def ekleDaire(self):
        print("ekleDaire")
        nokta1_x = self.ENTRY_NOKTA1_X.get()
        nokta1_y = self.ENTRY_NOKTA1_Y.get()
        yaricap_1 = self.ENTRY_YARICAP1.get()
        aci_bas = self.CBOX_ACI_BAS.get()
        aci_son = self.CBOX_ACI_SON.get()
        malzeme_eklenecek_mi = self.CBTN_MALZEME_EKLENECEK_MI.instate(['selected'])

        try:
            nokta1_x = int(nokta1_x)
            nokta1_y = int(nokta1_y)
            yaricap_1 = int(yaricap_1)
            aci_bas = int(aci_bas)
            aci_son = int(aci_son)

            daire = Daire(malzeme_eklenecek_mi, Nokta(int(nokta1_x), int(nokta1_y)), yaricap_1, aci_bas, aci_son)
            if daire.ALAN <= 0:
                self.yazdirHata("Daire tanımı hatalı", 2)
            elif daire.listede_var_mi(self.sekil_listesi):
                self.yazdirHata("Daire listede tanımlı", 2)
            else:
                self.sekil_listesi.append(daire)
                self.guncelleResim()

        except ValueError:
            self.yazdirHata("Lütfen girdileri kontrol ediniz", 2)

    def ekleUcgen(self):
        print("ekleUcgen")
        nokta1_x = self.ENTRY_NOKTA1_X.get()
        nokta1_y = self.ENTRY_NOKTA1_Y.get()
        nokta2_x = self.ENTRY_NOKTA2_X.get()
        nokta2_y = self.ENTRY_NOKTA2_Y.get()
        nokta3_x = self.ENTRY_NOKTA3_X.get()
        nokta3_y = self.ENTRY_NOKTA3_Y.get()
        malzeme_eklenecek_mi = self.CBTN_MALZEME_EKLENECEK_MI.instate(['selected'])

        try:
            nokta1_x = int(nokta1_x)
            nokta1_y = int(nokta1_y)
            nokta2_x = int(nokta2_x)
            nokta2_y = int(nokta2_y)
            nokta3_x = int(nokta3_x)
            nokta3_y = int(nokta3_y)

            ucgen = Ucgen(malzeme_eklenecek_mi, Nokta(int(nokta1_x), int(nokta1_y)),
                          Nokta(int(nokta2_x), int(nokta2_y)),
                          Nokta(int(nokta3_x), int(nokta3_y)))

            if nokta1_y != nokta2_y:
                self.yazdirHata("Üçgen tanımı hatalı, taban doğrusu yatay olmalıdır.\n"
                                "Taban doğrusu ilk 2 nokta ile tanımlanırr.", 1)
            elif ucgen.ALAN <= 0:
                self.yazdirHata("Üçgen tanımı hatalı, alan sıfırdan küçük olamaz", 2)
            elif ucgen.listede_var_mi(self.sekil_listesi):
                self.yazdirHata("Üçgen listede tanımlı", 2)
            else:
                self.sekil_listesi.append(ucgen)
                self.guncelleResim()

        except ValueError:
            self.yazdirHata("Lütfen girdileri kontrol ediniz", 2)

    def guncelleResim(self):
        print("guncelleResim")

        self.image_context.rectangle((0, 0, self.pencere_genisligi, self.pencere_yuksekligi),
                                     fill=self.renk_arkaplan, outline=self.renk_arkaplan, width=0)

        for sekil in self.sekil_listesi:
            print("Şekil: " + str(sekil.SEKIL_TIPI))
            if sekil.MALZEME_EKLENECEK_MI:
                renk_doldurma = self.renk_sekil_ekle
                renk_dishat = self.renk_cizgi_ekle
                # kalinlik = self.cizgi_kalinligi
                kalinlik = 0
            else:
                renk_doldurma = self.renk_sekil_cikar
                renk_dishat = self.renk_cizgi_cikar
                kalinlik = 0

            if sekil.SEKIL_TIPI == SekilTipi.DIKDORTGEN:
                self.image_context.rectangle((sekil.KOSE_1.X + self.pencere_genisligi_onda_bir,
                                              self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                              sekil.KOSE_1.Y,
                                              sekil.KOSE_2.X + self.pencere_genisligi_onda_bir,
                                              self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                              sekil.KOSE_2.Y),
                                             fill=renk_doldurma, outline=renk_dishat, width=kalinlik)

            elif sekil.SEKIL_TIPI == SekilTipi.DAIRE:
                rect = (sekil.MERKEZ_NOKTA.X - sekil.YARICAP + self.pencere_genisligi_onda_bir,
                        self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                        sekil.MERKEZ_NOKTA.Y - sekil.YARICAP,
                        sekil.MERKEZ_NOKTA.X + sekil.YARICAP + self.pencere_genisligi_onda_bir,
                        self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                        sekil.MERKEZ_NOKTA.Y + sekil.YARICAP)
                if sekil.CEYREK_1_AKTIF:
                    self.image_context.pieslice(rect, 270, 360, fill=renk_doldurma, outline=renk_dishat, width=kalinlik)
                if sekil.CEYREK_2_AKTIF:
                    self.image_context.pieslice(rect, 180, 270, fill=renk_doldurma, outline=renk_dishat, width=kalinlik)
                if sekil.CEYREK_3_AKTIF:
                    self.image_context.pieslice(rect, 90, 180, fill=renk_doldurma, outline=renk_dishat, width=kalinlik)
                if sekil.CEYREK_4_AKTIF:
                    self.image_context.pieslice(rect, 0, 90, fill=renk_doldurma, outline=renk_dishat, width=kalinlik)

            elif sekil.SEKIL_TIPI == SekilTipi.UCGEN:
                noktalar = [(sekil.KOSE_1.X + self.pencere_genisligi_onda_bir,
                             self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir - sekil.KOSE_1.Y),
                            (sekil.KOSE_2.X + self.pencere_genisligi_onda_bir,
                             self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir - sekil.KOSE_2.Y),
                            (sekil.KOSE_3.X + self.pencere_genisligi_onda_bir,
                             self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir - sekil.KOSE_3.Y)]
                self.image_context.polygon(noktalar, fill=renk_doldurma, outline=None)

        for eksen in self.eksen_listesi:
            print("Şekil: " + str(eksen.SEKIL_TIPI))

            if eksen.SEKIL_TIPI == SekilTipi.EKSEN:
                self.image_context.line((eksen.KOSE_1.X + self.pencere_genisligi_onda_bir,
                                         self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir - eksen.KOSE_1.Y,
                                         eksen.KOSE_2.X + self.pencere_genisligi_onda_bir,
                                         self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir - eksen.KOSE_2.Y),
                                        fill=self.renk_eksen, width=self.eksen_kalinligi, joint=None)

        if self.CENTER_OF_MASS_VISIBLE:
            self.image_context.ellipse([self.CENTER_OF_MASS_X - self.CENTER_OF_MASS_R + self.pencere_genisligi_onda_bir,
                                        self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                        self.CENTER_OF_MASS_Y - self.CENTER_OF_MASS_R,
                                        self.CENTER_OF_MASS_X + self.CENTER_OF_MASS_R + self.pencere_genisligi_onda_bir,
                                        self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                        self.CENTER_OF_MASS_Y + self.CENTER_OF_MASS_R],
                                       fill=self.renk_center_of_mass, outline=self.renk_cizgi_ekle, width=1)
            self.image_context.line((self.CENTER_OF_MASS_X + self.pencere_genisligi_onda_bir,
                                     self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                     self.CENTER_OF_MASS_Y,
                                     self.CENTER_OF_MASS_X + self.pencere_genisligi_onda_bir + 30,
                                     self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                     self.CENTER_OF_MASS_Y),
                                    fill=self.renk_eksen, width=1, joint=None)
            self.image_context.line((self.CENTER_OF_MASS_X + self.pencere_genisligi_onda_bir,
                                     self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                     self.CENTER_OF_MASS_Y,
                                     self.CENTER_OF_MASS_X + self.pencere_genisligi_onda_bir,
                                     self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir -
                                     self.CENTER_OF_MASS_Y - 30),
                                    fill=self.renk_eksen, width=1, joint=None)
            """
            self.image_context.text((self.CENTER_OF_MASS_X + 32, self.pencere_yuksekligi - self.CENTER_OF_MASS_Y - 10),
                                    "X", font=self.fnt, fill=self.renk_eksen_yazisi)
            self.image_context.text((self.CENTER_OF_MASS_X + 5, self.pencere_yuksekligi - self.CENTER_OF_MASS_Y - 40),
                                    "Y", font=self.fnt, fill=self.renk_eksen_yazisi)
            """
            self.CENTER_OF_MASS_VISIBLE = False

        self.image_context.line((0, self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir,
                                 self.pencere_genisligi, self.pencere_yuksekligi - self.pencere_yuksekligi_onda_bir),
                                fill=self.renk_eksen, width=1, joint=None)
        self.image_context.line((self.pencere_genisligi_onda_bir, 0,
                                 self.pencere_genisligi_onda_bir, self.pencere_yuksekligi),
                                fill=self.renk_eksen, width=1, joint=None)

        imagetk = ImageTk.PhotoImage(self.image)
        image_sprite = self.CANVAS.create_image(0, 0, anchor=SW, image=imagetk)
        # self.image.show()

        self.CANVAS.configure(scrollregion=self.CANVAS.bbox("all"))

        self.guncelleSekilListesiTreeview()
        self.run()

    def guncelleSekilListesiTreeview(self):
        print("guncelleSekilListesiTreeview")

        self.TREEVIEW_SEKIL_LISTESI.delete(*self.TREEVIEW_SEKIL_LISTESI.get_children())

        for sekil in self.sekil_listesi:
            malzeme_eklenecek_mi = "HAYIR"
            if sekil.MALZEME_EKLENECEK_MI:
                malzeme_eklenecek_mi = "EVET"

            if sekil.SEKIL_TIPI == SekilTipi.DIKDORTGEN:
                nokta = "X:" + str(sekil.KOSE_1.X) + "-Y:" + str(sekil.KOSE_1.Y)
                sekil.ID_TREEVIEW = self.TREEVIEW_SEKIL_LISTESI.insert("", "end", text="Dikdörtgen",
                                                                       values=(nokta, malzeme_eklenecek_mi))

            elif sekil.SEKIL_TIPI == SekilTipi.DAIRE:
                nokta = "X:" + str(sekil.MERKEZ_NOKTA.X) + "-Y:" + str(sekil.MERKEZ_NOKTA.Y)
                sekil.ID_TREEVIEW = self.TREEVIEW_SEKIL_LISTESI.insert("", "end", text="Daire",
                                                                       values=(nokta, malzeme_eklenecek_mi))

            elif sekil.SEKIL_TIPI == SekilTipi.UCGEN:
                nokta = "X:" + str(sekil.KOSE_1.X) + "-Y:" + str(sekil.KOSE_1.Y)
                sekil.ID_TREEVIEW = self.TREEVIEW_SEKIL_LISTESI.insert("", "end", text="Üçgen",
                                                                       values=(nokta, malzeme_eklenecek_mi))

            print("ID_TREEVIEW: " + str(sekil.ID_TREEVIEW))

        for eksen in self.eksen_listesi:
            malzeme_eklenecek_mi = "HAYIR"

            if eksen.SEKIL_TIPI == SekilTipi.EKSEN:
                nokta = "X:" + str(eksen.KOSE_1.X) + "-Y:" + str(eksen.KOSE_1.Y)
                eksen.ID_TREEVIEW = self.TREEVIEW_SEKIL_LISTESI.insert("", "end", text="Eksen",
                                                                       values=(nokta, malzeme_eklenecek_mi))

            print("ID_TREEVIEW: " + str(eksen.ID_TREEVIEW))

        self.run()

    def ekleSekil_OnClick(self):
        print("ekleSekil_OnClick")

        if self.EKLENECEK_SEKIL_TIPI == SekilTipi.EKSEN:
            self.ekleEksen()
        elif self.EKLENECEK_SEKIL_TIPI == SekilTipi.DIKDORTGEN:
            self.ekleDikdortgen()
        elif self.EKLENECEK_SEKIL_TIPI == SekilTipi.DAIRE:
            self.ekleDaire()
        elif self.EKLENECEK_SEKIL_TIPI == SekilTipi.UCGEN:
            self.ekleUcgen()

    def silSekil_OnClick(self):
        secili_sekil_listesi = self.TREEVIEW_SEKIL_LISTESI.selection()
        for secili_sekil in secili_sekil_listesi:
            print("Silindi: " + str(secili_sekil))
            self.TREEVIEW_SEKIL_LISTESI.delete(secili_sekil)

            for sekil in self.sekil_listesi:
                if sekil.ID_TREEVIEW == secili_sekil:
                    self.sekil_listesi.remove(sekil)

        self.guncelleResim()

    def coz_OnClick(self):
        xg_t = 0
        yg_t = 0
        alan_t = 0
        i_x = 0
        i_y = 0

        for sekil in self.sekil_listesi:
            if sekil.MALZEME_EKLENECEK_MI:
                xg_t = xg_t + sekil.CoM_X * sekil.ALAN
                yg_t = yg_t + sekil.CoM_Y * sekil.ALAN
                alan_t = alan_t + sekil.ALAN
            else:
                xg_t = xg_t - sekil.CoM_X * sekil.ALAN
                yg_t = yg_t - sekil.CoM_Y * sekil.ALAN
                alan_t = alan_t - sekil.ALAN

        xg = xg_t / alan_t
        yg = yg_t / alan_t

        self.CENTER_OF_MASS_X = int(xg)
        self.CENTER_OF_MASS_Y = int(yg)

        for sekil in self.sekil_listesi:
            if sekil.MALZEME_EKLENECEK_MI:
                i_x = i_x + (sekil.Ix + sekil.ALAN * (sekil.CoM_Y - yg) ** 2)
                i_y = i_y + (sekil.Iy + sekil.ALAN * (sekil.CoM_X - xg) ** 2)
            else:
                i_x = i_x - (sekil.Ix + sekil.ALAN * (sekil.CoM_Y - yg) ** 2)
                i_y = i_y - (sekil.Iy + sekil.ALAN * (sekil.CoM_X - xg) ** 2)

        sonuc_str = "Toplam Alan: " + str(self.ayarlaOnlukBasamak(alan_t)) + "\n" + \
                    "xG: " + str(self.ayarlaOnlukBasamak(xg)) + " - yG: " + str(self.ayarlaOnlukBasamak(yg)) + "\n" + \
                    "Ix: " + str(self.ayarlaOnlukBasamak(i_x)) + " - Iy: " + str(self.ayarlaOnlukBasamak(i_y))
        self.yazdirSonuc(sonuc_str, 4)

        self.CENTER_OF_MASS_VISIBLE = True
        self.guncelleResim()


if __name__ == '__main__':
    import tkinter as tk

    root = tk.Tk()
    app = GuiDataApp()
    app.run()
