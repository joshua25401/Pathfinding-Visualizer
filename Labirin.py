from visualSetting import *
import random


class Labirin:

    def __init__(self, app, posisiTembok) -> None:
        self.app = app
        self.tembok = posisiTembok
        self.visitedNode = []

        self.nilai_max_X = KOLOM_NODE
        self.nilai_max_Y = BARIS_NODE

    # Function untuk membuat semua Node Hitam

    def isi_tembok(self):

        for baris in range(1, self.nilai_max_Y):
            for kolom in range(1, self.nilai_max_X):
                self.tembok.append((kolom, baris))
                self.gambar_tembok((kolom, baris), BLACK)

        self.gambar_garis()
        self.buat_labirin()

    # Function untuk menggambar garis

    def gambar_garis(self):
        for kolom in range(KOLOM_NODE - 1):
            pygame.draw.line(self.app.screen, ALICE,
                             (GS_X + kolom * 24, GS_Y), (GS_X + kolom * 24, GE_Y))

        for baris in range(BARIS_NODE - 1):
            pygame.draw.line(self.app.screen, ALICE,
                             (GS_X, GS_Y + baris * 24), (GE_X, GS_Y + baris * 24))

    # Function gambar Tembok
    def gambar_tembok(self, posisi, warna):
        baris, kolom = posisi
        pygame.draw.rect(self.app.screen, warna,
                         (baris * 24 + 240, kolom * 24, 24, 24), 0)

    # Function membuat labirin
    def buat_labirin(self):
        posisi_baris = random.randint(1, self.nilai_max_X)
        posisi_kolom = random.randint(1, self.nilai_max_Y)
        posisi_node_awal = (posisi_baris, posisi_kolom)

        self.dfs_labirin(posisi_node_awal)

    def dfs_labirin(self, posisi_node_awal):
        dfs_constraint = ['kiri', 'kanan', 'atas', 'bawah']
        baris, kolom = posisi_node_awal

        while dfs_constraint:
            pilih_langkah_random = random.randint(0, len(dfs_constraint)-1)
            langkah_sekarang = dfs_constraint.pop(pilih_langkah_random)

            barisTemp = baris
            kolomTemp = kolom

            if langkah_sekarang == 'kiri':
                barisTemp -= 2
            elif langkah_sekarang == 'kanan':
                barisTemp += 2
            elif langkah_sekarang == 'atas':
                kolomTemp += 2
            else:
                kolomTemp -= 2

            posisiBaru = (barisTemp, kolomTemp)

            if self.check_posisi(posisiBaru):
                self.tembok.remove(posisiBaru)

                jarakBaris = posisiBaru[0] - baris
                jarakKolom = posisiBaru[1] - kolom

                posisiTembokTengah = (
                    baris + jarakBaris / 2, kolom + jarakKolom / 2)

                if ((posisiTembokTengah) in self.tembok):
                    self.tembok.remove((posisiTembokTengah))
                    self.bentuk_labirin(posisiTembokTengah, AQUAMARINE)
                    self.bentuk_labirin(posisiBaru, AQUAMARINE)
                    self.dfs_labirin(posisiBaru)

        return

    def bentuk_labirin(self, posisi, warna):
        self.gambar_tembok(posisi, warna)

        for kolom in range(KOLOM_NODE - 1):
            pygame.draw.line(self.app.screen, ALICE,
                             (GS_X + kolom * 24, GS_Y), (GS_X + kolom * 24, GE_Y))

        for baris in range(BARIS_NODE - 1):
            pygame.draw.line(self.app.screen, ALICE,
                             (GS_X, GS_Y + baris * 24), (GE_X, GS_Y + baris * 24))

        pygame.display.update()

    def check_posisi(self, posisiTujuan):

        if posisiTujuan not in wall_nodes_coords_list and posisiTujuan in self.tembok:
            return True
        return False
