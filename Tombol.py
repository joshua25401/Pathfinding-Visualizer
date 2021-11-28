from visualSetting import *


class Tombol():

    # Constructor di python
    # Berisi konfigurasi awal dari tombol seperti :
    # 1. app = jendela dimana tombol tersebut akan ditempatkan
    # 2. warna = warna dari tombol
    # 3. posisi = posisi tombol diletakkan pada jendela berbentuk tuple coordinat cth: (10,20)-> x = 10 dan y = 20
    # 4. lebar = ukuran lebar dari tombol
    # 5. tinggi = ukuran tinggi dari tombol
    # 6. text = Isi text
    def __init__(self, app, warna, posisi, lebar, tinggi, text='') -> None:
        self.app = app
        self.warna = warna
        self.posisi = posisi
        self.lebar = lebar
        self.tinggi = tinggi
        self.text = text

    # Fungsi untuk menciptakan tombol
    def create_tombol(self, outline=None, color=None):
        if outline:
            pygame.draw.rect(self.app.screen, outline,
                             (self.posisi[0]-2, self.posisi[1]-2, self.lebar+4, self.tinggi+4), 0)

        pygame.draw.rect(self.app.screen, self.warna,
                         (self.posisi[0], self.posisi[1], self.lebar, self.tinggi))

        if(self.text != '' and not color):
            # Pilih font yang tersedia pada System komputer
            font = pygame.font.SysFont(FONT, 16)
            # Buat teks dengan warna hitam
            text = font.render(self.text, 1, BLACK)
            # Letakkan Posisi teks berada di tengah tombol
            self.app.screen.blit(text, (self.posisi[0] + (self.lebar / 2 - text.get_width(
            ) / 2), self.posisi[1] + (self.tinggi / 2 - text.get_height() / 2)))
        else:
            # Pilih font yang tersedia pada System komputer
            font = pygame.font.SysFont(FONT, 16)
            # Buat teks dengan warna hitam
            text = font.render(self.text, 1, color)
            # Letakkan Posisi teks berada di tengah tombol
            self.app.screen.blit(text, (self.posisi[0] + (self.lebar / 2 - text.get_width(
            ) / 2), self.posisi[1] + (self.tinggi / 2 - text.get_height() / 2)))
    # Track Kursor apakah berada diatas tombol atau tidak
    # 1. Pos = diisi oleh posisi koordinat dari kursor
    # Return :
    # True -> Jika koordinat kursor berada diantara Tombol
    # False -> Jika koordint kursor tidak berada diantara Tombol
    def isOver(self, pos):
        if pos[0] > self.posisi[0] and pos[0] < self.posisi[0] + self.lebar:
            if pos[1] > self.posisi[1] and pos[1] < self.posisi[1] + self.tinggi:
                return True
        return False

    def changeColorState(self, color=''):
        if color != '':
            self.warna = color
        else:
            self.warna = WHITE
