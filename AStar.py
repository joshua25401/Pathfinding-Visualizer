from visualSetting import *
from time import sleep


class Node:

    def __init__(self, posisi=None, parent=None):
        self.posisi = posisi
        self.parent = parent

        # Parameter untuk nilai F = G + H
        self.F = 0
        self.G = 0
        self.H = 0


class AStar():

    def __init__(self, app, posisi_awal, posisi_akhir, posisi_tembok) -> None:
        self.app = app
        self.posisiAwal = posisi_awal
        self.posisiAkhir = posisi_akhir
        self.listCalonNode = []
        self.listNodeSelesai = []
        self.posisiTembok = posisi_tembok
        self.rute = []
        self.ruteDitemukan = False

    # Function untuk mengupdate jalur pada grid
    def update_jalur(self, posisi_node_sekarang):
        x, y = posisi_node_sekarang

        # Jalur untuk node yang dilewati
        pygame.draw.rect(self.app.screen, TAN,
                         (x * 24 + 240, y * 24, 24, 24), 0)

        # Gambar ulang Node Awal dan Node Akhir
        pygame.draw.rect(self.app.screen, TOMATO, (240 +
                         self.posisiAwal[0] * 24, self.posisiAwal[1] * 24, 24, 24), 0)

        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 +
                         self.posisiAkhir[0] * 24, self.posisiAkhir[1] * 24, 24, 24), 0)

        # Gambar ulang garis
        for kolom in range(KOLOM_NODE - 1):
            pygame.draw.line(self.app.screen, ALICE,
                             (GS_X + kolom * 24, GS_Y), (GS_X + kolom * 24, GE_Y))

        for baris in range(BARIS_NODE - 1):
            pygame.draw.line(self.app.screen, ALICE,
                             (GS_X, GS_Y + baris * 24), (GE_X, GS_Y + baris * 24))

        pygame.display.update()

    # Function untuk check apakah posisi selanjutnya valid atau tidak
    def check_posisi(self, langkahTujuan):
        if langkahTujuan not in self.posisiTembok and langkahTujuan not in self.listNodeSelesai:
            return True
        return False

    # Function untuk menghitung Jarak Heuristic (Euclidean Distance)
    def calculateH(self, child, endNode):
        child.H = ((child.posisi[0] - endNode.posisi[0]) **
                   2) + ((child.posisi[1] - endNode.posisi[1]) ** 2)

    def calculateG(self, child, parent, langkah):
        # Tentukan apakah langkah yang ditempuh adalah diagonal atau lurus
        # Contoh Lurus :
        # Posisi (Atas,Bawah,Kanan,Kiri)
        # -> Atas (-1,0) jika dijumlah maka akan menghasilkan angka 1
        # -> Bawah (1,0) jika dijumlah juga akan menghasilkan angka 1
        # -> Kanan (0,1) jika dijumlah juga akan menghasilkan angka 1
        # -> Kiri (0,-1) jika dijumlah juga akan menghasilkan angka 1
        # Contoh Posisi Diagonal :
        # -> Diagonal Kiri Atas (-1,-1) jika dijumlah akan menghasilkan angka 2
        # -> Diagonal Kanan Atas (-1,1) jika dijumlah akan menghasilkan angka 0
        # -> Diagonal Kanan Bawah (1,1) jika djumlah akan menghasilkan angka 2
        # -> Diagonal Kiri Bawah (1,-1) jika dijumlah akan menghasilkan angka 0
        # Kesimpulan :
        # 1. Memberikan Nilai G paling Kecil jika tipe langkah adalah langkah lurus (1)
        # 2. Memberikan Nilai G paling Besar jika tipe langkah adalah langkah Diagonal (0 atau 2)
        tipeLangkah = abs(sum(langkah))

        if tipeLangkah == 1:
            child.G = parent.G + 10
        elif tipeLangkah == 0 or tipeLangkah == 2:
            child.G = parent.G + 14

    def calculateF(self, child):
        child.F = child.G + child.H

    def check_tembok(self, langkah, posisi_parent):
        if langkah == (-1, 1) or langkah == (1, 1) or langkah == (1, -1) or langkah == (-1, -1):
            parent_x, parent_y = posisi_parent
            (langkah_x, langkah_y) = langkah

            if langkah == (1, 1):
                (tembok_x1, tembok_y1) = (0, 1)
                (tembok_x2, tembok_y2) = (1, 0)
            elif langkah == (1, -1):
                (tembok_x1, tembok_y1) = (1, 0)
                (tembok_x2, tembok_y2) = (0, -1)
            elif langkah == (-1, -1):
                (tembok_x1, tembok_y1) = (0, -1)
                (tembok_x2, tembok_y2) = (-1, 0)
            else:
                (tembok_x1, tembok_y1) = (-1, 0)
                (tembok_x2, tembok_y2) = (0, 1)

            # Check apakah langkah selanjutnya melangkahi tembok atau tidak
            # Jika langkah selanjutnya melangkahi tembok maka berikan False
            if (parent_x + tembok_x1, parent_y + tembok_y1) in self.posisiTembok or (parent_x + tembok_x2, parent_y + tembok_y2) in self.posisiTembok and (parent_x + langkah_x, parent_y + langkah_y) not in self.posisiTembok:
                return False

            return True
        else:
            return True

    # Function untuk check apakah calon node child sudah berada di list calon node atau tidak
    def check_open_list(self, child):
        for node in self.listCalonNode:
            if child.posisi == node.posisi and child.F >= node.F:
                return False
        return True

    # Function untuk mengambil calon child di current node
    def buat_calon_node_child(self, parent, nodeAkhir):
        # print("Calon Node Child :")

        posisi_parent = parent.posisi

        # Check Langkah Selanjutnya dengan Urutan (Atas,Bawah,Kanan,Kiri, dan Diagonal)
        for langkah in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            posisi_child = (
                posisi_parent[0] + langkah[0], posisi_parent[1] + langkah[1])

            if self.check_posisi(posisi_child):
                nodeChild = Node(posisi_child, parent)
                self.calculateG(nodeChild, parent, langkah)
                self.calculateH(nodeChild, nodeAkhir)
                self.calculateF(nodeChild)

                # print(posisi_parent, " ", nodeChild.posisi, " ", nodeChild.F,
                #       " ", nodeChild.G, " ", nodeChild.H)

                if self.check_open_list(nodeChild) and self.check_tembok(langkah, posisi_parent):
                    # print(nodeChild.posisi)
                    self.listCalonNode.append(nodeChild)

    def is_end_node(self, nodeSekarang):
        if nodeSekarang == (self.posisiAkhir[0], self.posisiAkhir[1]):
            return True
        return False

    # Eksekusi Algoritma AStar
    def algoritma_astar(self):
        nodeAwal = Node((self.posisiAwal[0], self.posisiAwal[1]), None)
        nodeAwal.G = nodeAwal.H = nodeAwal.F = 0

        nodeAkhir = Node((self.posisiAkhir[0], self.posisiAkhir[1]), None)
        nodeAkhir.G = nodeAkhir.H = nodeAkhir.F = 0

        self.listCalonNode.append(nodeAwal)

        while len(self.listCalonNode) > 0:
            nodeSekarang = self.listCalonNode[0]
            indeksSekarang = 0

            for indeks, node in enumerate(self.listCalonNode):
                if node.F < nodeSekarang.F:
                    nodeSekarang = node
                    indeksSekarang = indeks

            if self.is_end_node(nodeSekarang.posisi):
                nodeTemp = nodeSekarang
                while nodeTemp is not None:
                    self.rute.append(nodeTemp.posisi)
                    nodeTemp = nodeTemp.parent
                    # print(nodeTemp)
                self.rute.pop(0)
                self.ruteDitemukan = True

                break

            self.buat_calon_node_child(nodeSekarang, nodeAkhir)
            self.update_jalur(nodeSekarang.posisi)

            self.listCalonNode.pop(indeksSekarang)
            self.listNodeSelesai.append(nodeSekarang.posisi)
            sleep(0.001)
