
import sys
from GambarJalur import GambarJalur
from Labirin import Labirin
from visualSetting import *
from Tombol import *
from AStar import *
from Dijkstra import *
import time

pygame.init()


class App:

    # Constructor dari Aplikasi
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((LEBAR, TINGGI))
        self.clock = pygame.time.Clock()
        self.state = 'main_menu'
        self.algoritma = ''
        self.ukuranGrid = 24
        self.nodeChecker = 0
        self.mouseDrag = 0
        self.running = True

        # Load Menu Icon
        self.loadMenuIcon()

        # Konfigurasi awal dari Koordinat Node
        self.posisi_awal_node_sbX = None
        self.posisi_awal_node_sbY = None
        self.posisi_akhir_node_sbX = None
        self.posisi_akhir_node_sbY = None

        # Constraint Node List
        self.wall_pos = wall_nodes_coords_list.copy()

        # Labirin
        self.labirin = Labirin(self, self.wall_pos)

        # Tombol di layar Main Menu
        self.tombol_menu_astar = Tombol(
            self, WHITE, (228 * 2, MAIN_BUTTON_Y), LEBAR_TOMBOL, TINGGI_TOMBOL, 'A-Star Algorithm')

        self.tombol_menu_dijkstra = Tombol(
            self, WHITE, (228 * 4, MAIN_BUTTON_Y), LEBAR_TOMBOL, TINGGI_TOMBOL, 'Dijkstra Algorithm')

        # Tombol di layar Nav Grid Menu
        self.node_awal_akhir = Tombol(
            self, ALICE, (20, POSISI_AWAL_TOMBOL_GRID), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Pilih Node Awal / Akhir")
        self.buat_rintangan = Tombol(
            self, ALICE, (20, POSISI_AWAL_TOMBOL_GRID + TINGGI_TOMBOL_GRID + JARAK), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Buat Rintangan")
        self.ulangi = Tombol(
            self, ALICE, (20, POSISI_AWAL_TOMBOL_GRID + TINGGI_TOMBOL_GRID * 2 + JARAK * 2), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Ulangi")
        self.mulai = Tombol(
            self, ALICE, (20, POSISI_AWAL_TOMBOL_GRID + TINGGI_TOMBOL_GRID * 3 + JARAK * 3), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Mulai Visualisasi")
        self.rintangan_otomatis = Tombol(
            self, ALICE, (20, POSISI_AWAL_TOMBOL_GRID + TINGGI_TOMBOL_GRID * 4 + JARAK * 4), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Rintangan Otomatis")
        self.kembali_ke_menu = Tombol(
            self, ALICE, (20, POSISI_AWAL_TOMBOL_GRID + TINGGI_TOMBOL_GRID * 5 + JARAK * 5), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Kembali")

        self.processing = Tombol(
            self, WHITE, (20, POSISI_AWAL_TOMBOL_GRID + TINGGI_TOMBOL_GRID * 7 + JARAK * 7), LEBAR_TOMBOL_GRID, TINGGI_TOMBOL_GRID, "Processing...")

    def run(self):
        while(self.running):
            if self.state == 'main_menu':
                pygame.display.set_caption(
                    "Pathfinding Visualizer By Kelompok ALU")
                self.main_menu()
            if self.state == 'nav_grid_menu':
                self.nav_grid_menu()
            if self.state == 'pilih_node_awal_akhir' or self.state == 'buat_rintangan':
                self.gambar_node()
            if self.state == 'mulai_visualisasi':
                self.eksekusi_algoritma_pencarian()
            if self.state == 'tampilan_hasil':
                self.hasil()
        pygame.quit()
        sys.exit()

    # Function Load Menu Icon
    def loadMenuIcon(self):
        self.main_menu_icon = pygame.image.load('menu_icon.png')

    # Function Tambah Teks
    def tambah_teks(self, teks, layar, posisi, ukuran, warna, tipeFont, centered=False):
        font = pygame.font.SysFont(tipeFont, ukuran)
        text = font.render(teks, False, warna)
        ukuranTeks = text.get_size()

        if centered:
            (x, y) = (posisi[0] - ukuranTeks[0] //
                      2, posisi[1] - ukuranTeks[1] // 2)
            posisi = (x, y)
        layar.blit(text, posisi)
        layar.blit(text, posisi)

# MAIN MENU

    def setup_main_menu(self):
        self.screen.blit(self.main_menu_icon, (0, 0))
        self.tombol_menu_astar.create_tombol(AQUAMARINE)
        self.tombol_menu_dijkstra.create_tombol(AQUAMARINE)

    def main_menu(self):
        pygame.display.update()
        self.setup_main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            posisiKursor = pygame.mouse.get_pos()
            # print(posisiKursor)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tombol_menu_astar.isOver(posisiKursor):
                    self.tombol_menu_astar.changeColorState()
                    self.algoritma = 'a_star_algorithm'
                    self.state = 'nav_grid_menu'
                    pygame.display.set_caption("Algoritma A-Star")
                elif self.tombol_menu_dijkstra.isOver(posisiKursor):
                    self.tombol_menu_dijkstra.changeColorState()
                    self.algoritma = 'dijkstra_algorithm'
                    self.state = 'nav_grid_menu'
                    pygame.display.set_caption("Algoritma Dijkstra")

            if event.type == pygame.MOUSEMOTION:
                if self.tombol_menu_astar.isOver(posisiKursor):
                    self.tombol_menu_astar.warna = AQUAMARINE
                elif self.tombol_menu_dijkstra.isOver(posisiKursor):
                    self.tombol_menu_dijkstra.warna = AQUAMARINE
                else:
                    self.tombol_menu_astar.changeColorState(WHITE)
                    self.tombol_menu_dijkstra.changeColorState(WHITE)

# NAV_GRID_MENU
    def setup_nav_bar(self):
        # self.screen.fill(ALICE)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)

    def setup_nav_grid_menu(self):
        self.node_awal_akhir.create_tombol(STEELBLUE)
        self.buat_rintangan.create_tombol(STEELBLUE)
        self.ulangi.create_tombol(STEELBLUE)
        self.mulai.create_tombol(STEELBLUE)
        self.rintangan_otomatis.create_tombol(STEELBLUE)
        self.kembali_ke_menu.create_tombol(STEELBLUE)
        self.tambah_teks("Estimated Time : ", self.screen, (35, POSISI_AWAL_TOMBOL_GRID +
                         TINGGI_TOMBOL_GRID * 6 + JARAK * 6), 16, BLACK, FONT)

    def setup_grid_array(self):
        pygame.draw.rect(self.screen, VIOLETRED, (240, 0, LEBAR, TINGGI), 0)
        pygame.draw.rect(self.screen, AQUAMARINE,
                         (264, 24, LEBAR_GRID, TINGGI_GRID), 0)

        for kolom in range(KOLOM_NODE - 1):
            pygame.draw.line(self.screen, ALICE, (GS_X + kolom *
                             self.ukuranGrid, GS_Y), (GS_X + kolom * self.ukuranGrid, GE_Y))

        for baris in range(BARIS_NODE - 1):
            pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + baris *
                             self.ukuranGrid), (GE_X, GS_Y + baris * self.ukuranGrid))

    def nav_grid_menu(self):
        self.setup_nav_bar()
        self.setup_nav_grid_menu()
        self.setup_grid_array()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            posisiKursor = pygame.mouse.get_pos()

            self.nav_grid_menu_action(posisiKursor, event)

    def nav_grid_menu_action(self, pos, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.node_awal_akhir.isOver(pos):
                self.state = 'pilih_node_awal_akhir'
            if self.buat_rintangan.isOver(pos):
                self.state = 'buat_rintangan'
            if self.ulangi.isOver(pos):
                self.reset_grid()
            if self.kembali_ke_menu.isOver(pos):
                self.kembali_ke_main_menu()
            if self.rintangan_otomatis.isOver(pos):
                self.state = 'buat_rintangan'
                self.reset_grid()
                self.labirin.isi_tembok()
                self.state = 'pilih_node_awal_akhir'
            if self.mulai.isOver(pos):
                self.state = 'mulai_visualisasi'

        if event.type == pygame.MOUSEMOTION:
            if self.node_awal_akhir.isOver(pos):
                self.node_awal_akhir.changeColorState(MINT)
            elif self.buat_rintangan.isOver(pos):
                self.buat_rintangan.changeColorState(MINT)
            elif self.ulangi.isOver(pos):
                self.ulangi.changeColorState(MINT)
            elif self.kembali_ke_menu.isOver(pos):
                self.kembali_ke_menu.changeColorState(MINT)
            elif self.rintangan_otomatis.isOver(pos):
                self.rintangan_otomatis.changeColorState(MINT)
            elif self.mulai.isOver(pos):
                self.mulai.changeColorState(MINT)
            else:
                self.node_awal_akhir.changeColorState(ALICE)
                self.buat_rintangan.changeColorState(ALICE)
                self.ulangi.changeColorState(ALICE)
                self.kembali_ke_menu.changeColorState(ALICE)
                self.rintangan_otomatis.changeColorState(ALICE)
                self.mulai.changeColorState(ALICE)

    def state_tombol_navigasi(self):
        if self.state == 'pilih_node_awal_akhir':
            self.node_awal_akhir.changeColorState(MINT)

        if self.state == 'buat_rintangan':
            self.buat_rintangan.changeColorState(MINT)

    # Gambar Node

    def gambar_node(self):
        self.state_tombol_navigasi()
        self.setup_nav_grid_menu()
        pygame.display.update()

        posisiKursor = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            self.nav_grid_menu_action(posisiKursor, event)

            if posisiKursor[0] > 264 and posisiKursor[0] < 1512 and posisiKursor[1] > 24 and posisiKursor[1] < 744:
                posisi_grid_sbX = (posisiKursor[0] - 264) // 24
                posisi_grid_sbY = (posisiKursor[1] - 24) // 24

                # print('GRID : ', posisi_grid_sbX, " ", posisi_grid_sbY)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseDrag = 1

                    if self.state == 'pilih_node_awal_akhir' and self.nodeChecker < 2:
                        if self.nodeChecker == 0 and (posisi_grid_sbX + 1, posisi_grid_sbY + 1) not in self.wall_pos:
                            warnaNode = TOMATO
                            self.posisi_awal_node_sbX = posisi_grid_sbX + 1
                            self.posisi_awal_node_sbY = posisi_grid_sbY + 1
                            self.nodeChecker += 1
                            print("NODE : ", (self.posisi_awal_node_sbX,
                                  self.posisi_awal_node_sbY))

                        elif self.nodeChecker == 1 and (posisi_grid_sbX + 1, posisi_grid_sbY + 1) != (self.posisi_awal_node_sbX, self.posisi_awal_node_sbY) and (posisi_grid_sbX + 1, posisi_grid_sbY + 1) not in self.wall_pos:
                            warnaNode = ROYALBLUE
                            self.posisi_akhir_node_sbX = posisi_grid_sbX + 1
                            self.posisi_akhir_node_sbY = posisi_grid_sbY + 1
                            self.nodeChecker += 1
                            print("NODE : ", (self.posisi_akhir_node_sbX,
                                  self.posisi_akhir_node_sbY))
                        else:
                            continue

                        pygame.draw.rect(
                            self.screen, warnaNode, (264 + posisi_grid_sbX *
                                                     24, 24 + posisi_grid_sbY * 24, 24, 24), 0
                        )
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouseDrag = 0

                if self.mouseDrag == 1:
                    if self.state == 'buat_rintangan':
                        if (posisi_grid_sbX + 1, posisi_grid_sbY + 1) not in self.wall_pos and (posisi_grid_sbX+1, posisi_grid_sbY+1) != (self.posisi_awal_node_sbX, self.posisi_awal_node_sbY) and (posisi_grid_sbX+1, posisi_grid_sbY+1) != (self.posisi_akhir_node_sbX, self.posisi_akhir_node_sbY):
                            pygame.draw.rect(
                                self.screen, BLACK, (264 + posisi_grid_sbX * 24, 24 + posisi_grid_sbY * 24, 24, 24), 0)
                            self.wall_pos.append(
                                (posisi_grid_sbX+1, posisi_grid_sbY+1)
                            )

                for kolom in range(KOLOM_NODE - 1):
                    pygame.draw.line(self.screen, ALICE, (GS_X + kolom *
                                     self.ukuranGrid, GS_Y), (GS_X + kolom * self.ukuranGrid, GE_Y))

                for baris in range(BARIS_NODE - 1):
                    pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + baris *
                                     self.ukuranGrid), (GE_X, GS_Y + baris * self.ukuranGrid))

    # Reset Tampilan Grid
    def reset_grid(self):
        # Reset Pilihan Node awal dan akhir
        self.nodeChecker = 0

        # Reset Posisi Node
        self.posisi_awal_node_sbX = None
        self.posisi_awal_node_sbY = None
        self.posisi_akhir_node_sbX = None
        self.posisi_akhir_node_sbY = None

        # Reset Labirin
        self.wall_pos = wall_nodes_coords_list.copy()
        # Labirin
        self.labirin = Labirin(self, self.wall_pos)

        # Reset tampilan
        self.processing.text = "Processing..."
        self.state = 'nav_grid_menu'

    # Kembali ke Main Menu
    def kembali_ke_main_menu(self):
        # Reset Pilihan Node Awal dan Akhir
        self.nodeChecker = 0

        # Reset Posisi Node
        self.posisi_awal_node_sbX = None
        self.posisi_awal_node_sbY = None
        self.posisi_akhir_node_sbX = None
        self.posisi_akhir_node_sbY = None

        # Reset Labirin
        self.wall_pos = wall_nodes_coords_list.copy()
        # Labirin
        self.labirin = Labirin(self, self.wall_pos)

        # Pindah ke Main Menu
        self.processing.text = "Processing..."
        self.state = "main_menu"

    # Function untuk eksekusi algoritma
    def eksekusi_algoritma_pencarian(self):

        self.processing.create_tombol(None, ROYALBLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.algoritma == 'a_star_algorithm':
            self.astar = AStar(self, (self.posisi_awal_node_sbX, self.posisi_awal_node_sbY),
                               (self.posisi_akhir_node_sbX, self.posisi_akhir_node_sbY), self.wall_pos)

            # print(self.posisi_awal_node_sbX or self.posisi_akhir_node_sbX is not None)
            if self.posisi_awal_node_sbX or self.posisi_akhir_node_sbX is not None:
                self.startTime = time.time()
                self.astar.algoritma_astar()

            if self.astar.ruteDitemukan:
                self.gambarJalur = GambarJalur(
                    self.screen, (self.posisi_awal_node_sbX, self.posisi_awal_node_sbY), None, self.astar.rute)

                print(self.astar.rute)
                self.gambarJalur.gambar_jalur()

        if self.algoritma == 'dijkstra_algorithm':
            self.dijkstra = Dijkstra(self, (self.posisi_awal_node_sbX, self.posisi_awal_node_sbY), (
                self.posisi_akhir_node_sbX, self.posisi_akhir_node_sbY), self.wall_pos)

            if self.posisi_awal_node_sbX or self.posisi_akhir_node_sbX is not None:
                self.startTime = time.time()
                self.dijkstra.algoritma_dijkstra()

            if self.dijkstra.ruteDitemukan:
                self.gambarJalur = GambarJalur(
                    self.screen, (self.posisi_awal_node_sbX,
                                  self.posisi_awal_node_sbY), None, self.dijkstra.rute
                )
                self.gambarJalur.gambar_jalur()

        pygame.display.update()
        self.endTime = time.time() - self.startTime
        self.state = "tampilan_hasil"

    def hasil(self):
        self.setup_nav_bar()
        self.setup_nav_grid_menu()

        if self.algoritma == "a_star_algorithm":
            if self.astar.ruteDitemukan:
                self.processing.text = str(self.endTime)
                self.processing.create_tombol(None, SPRINGGREEN)
            else:
                self.processing.text = "Rute Tidak Ditemukan!"
                self.processing.create_tombol(None, RED)
        else:
            if self.dijkstra.ruteDitemukan:
                self.processing.text = str(self.endTime)
                self.processing.create_tombol(None, SPRINGGREEN)
            else:
                self.processing.text = "Rute Tidak Ditemukan!"
                self.processing.create_tombol(None, RED)

        pygame.display.update()

        posisiKursor = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.node_awal_akhir.isOver(posisiKursor):
                    self.node_awal_akhir.changeColorState(MINT)
                elif self.buat_rintangan.isOver(posisiKursor):
                    self.buat_rintangan.changeColorState(MINT)
                elif self.ulangi.isOver(posisiKursor):
                    self.ulangi.changeColorState(MINT)
                elif self.kembali_ke_menu.isOver(posisiKursor):
                    self.kembali_ke_menu.changeColorState(MINT)
                elif self.rintangan_otomatis.isOver(posisiKursor):
                    self.rintangan_otomatis.changeColorState(MINT)
                elif self.mulai.isOver(posisiKursor):
                    self.mulai.changeColorState(MINT)
                else:
                    self.node_awal_akhir.changeColorState(ALICE)
                    self.buat_rintangan.changeColorState(ALICE)
                    self.ulangi.changeColorState(ALICE)
                    self.kembali_ke_menu.changeColorState(ALICE)
                    self.rintangan_otomatis.changeColorState(ALICE)
                    self.mulai.changeColorState(ALICE)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.ulangi.isOver(posisiKursor):
                    self.reset_grid()
                elif self.kembali_ke_menu.isOver(posisiKursor):
                    self.kembali_ke_main_menu()
