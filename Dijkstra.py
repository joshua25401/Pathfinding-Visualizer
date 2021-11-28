from visualSetting import *
from time import sleep


class Node:

    def __init__(self, posisi=None, parent=None):
        self.posisi = posisi
        self.parent = parent

        # Jarak antara Node yang dikunjungi dari Node awal
        self.jarak = 0


class Dijkstra:

    def __init__(self, app, posisiAwal, posisiAkhir, posisiTembok) -> None:
        self.app = app
        self.posisiAwal = posisiAwal
        self.posisiAkhir = posisiAkhir
        self.posisiTembok = posisiTembok

        self.rute = []
        self.ruteDitemukan = False
        self.listCalonNode = []
        self.listNodeSelesai = []

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

    # Check apakah ketika bergerak atau melangkah secara diagonal tidak melewati tembok
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

    # Function untuk check apakah posisi selanjutnya valid atau tidak
    def check_posisi(self, langkahTujuan):
        if langkahTujuan not in self.posisiTembok and langkahTujuan not in self.listNodeSelesai:
            return True
        return False

    def hitung_jarak(self, nodeChild, nodeParent, langkah):

        tipeLangkah = abs(sum(langkah))

        if tipeLangkah == 1:
            nodeChild.jarak = nodeParent.jarak + 10
        elif tipeLangkah == 0 or tipeLangkah == 2:
            nodeChild.jarak = nodeParent.jarak + 14

    def check_posisi_valid(self, posisi):

        if posisi not in self.posisiTembok and posisi not in self.listNodeSelesai:
            return True

        return False

    def check_list_calon_node(self, child):

        for node in self.listCalonNode:
            if child.posisi == node.posisi and child.jarak >= node.jarak:
                return False
        return True

    def buat_calon_node_child(self, parent):
        posisiParent = parent.posisi
        # print(posisiParent)
        for langkah in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            posisiChild = (posisiParent[0] + langkah[0],
                           posisiParent[1] + langkah[1])

            # print(self.check_posisi_valid(posisiChild))
            if self.check_posisi_valid(posisiChild):
                nodeChild = Node(posisiChild, parent)
                self.hitung_jarak(nodeChild, parent, langkah)

                # print(nodeChild.posisi)

                if self.check_list_calon_node(nodeChild) and self.check_tembok(langkah, parent.posisi):
                    self.listCalonNode.append(nodeChild)

    def is_node_end(self, posisi):
        if posisi == (self.posisiAkhir[0], self.posisiAkhir[1]):
            return True
        return False

    def algoritma_dijkstra(self):
        # print(self.posisiAwal)
        # print(self.posisiAkhir)
        nodeAwal = Node((self.posisiAwal[0], self.posisiAwal[1]), None)
        nodeAwal.jarak = 0
        nodeAkhir = Node((self.posisiAkhir[0], self.posisiAkhir[1]), None)

        self.listCalonNode.append(nodeAwal)
        # print(nodeAwal.posisi)
        while len(self.listCalonNode) > 0:
            nodeSekarang = self.listCalonNode[0]
            indeksSekarang = 0

            # print(nodeSekarang.posisi)

            # print("TRUE")
            for indeks, node in enumerate(self.listCalonNode):
                # print(node.jarak < nodeSekarang.jarak)
                if node.jarak < nodeSekarang.jarak:
                    nodeSekarang = node
                    indeksSekarang = indeks

            # print(self.is_node_end(nodeSekarang.posisi))
            if self.is_node_end(nodeSekarang.posisi):
                nodeTemp = nodeSekarang

                while nodeTemp is not None:
                    self.rute.append(nodeTemp.posisi)
                    nodeTemp = nodeTemp.parent

                self.rute.pop(0)
                self.ruteDitemukan = True
                break

            print(nodeSekarang.posisi)
            self.update_jalur(nodeSekarang.posisi)
            self.buat_calon_node_child(nodeSekarang)

            self.listCalonNode.pop(indeksSekarang)
            self.listNodeSelesai.append(nodeSekarang.posisi)
            sleep(0.001)
