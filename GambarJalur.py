from visualSetting import *


class GambarJalur():

    def __init__(self, layar, posisiNodeAwal, jalur, koordinatJalur) -> None:
        self.layar = layar
        self.posisiNodeAwal = posisiNodeAwal
        self.jalur = jalur
        self.koordinatJalur = koordinatJalur

    def gambar_jalur(self):
        self.koordinatJalur.pop()
        for (posisi_sbX, posisi_sbY) in self.koordinatJalur:
            pygame.draw.rect(self.layar, SPRINGGREEN,
                             (posisi_sbX*24 + 240, posisi_sbY*24, 24, 24), 0)
