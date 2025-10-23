import pygame, os, random
from pygame.locals import *
import math

pygame.init()

gameRunning = False

# Fenster erstellen
screen_width = 1920
screen_height = 1020
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coin Eater")
fpsClock = pygame.time.Clock()
fps = 60
background = pygame.Color(10, 10, 10)

# Spielfeld erstellen
spielfeldImage = pygame.transform.rotozoom(pygame.image.load("jahresarbeit/Bilder/spielfeld.png"), 0, 1.02)
spielfeldRect = spielfeldImage.get_rect()
spielfeldRect.topleft = (350, 0)

# Spieler erstellen
player_start_x = 1920/2 - 26
player_start_y = 1020/2 - 26
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imageOben = pygame.image.load("jahresarbeit/Bilder/FroschOben.png")
        self.imageUnten = pygame.image.load("jahresarbeit/Bilder/FroschUnten.png")
        self.imageRechts = pygame.image.load("jahresarbeit/Bilder/FroschRechts.png")
        self.imageLinks = pygame.image.load("jahresarbeit/Bilder/FroschLinks.png")

        self.imageObenRechts = pygame.image.load("jahresarbeit/Bilder/FroschObenRechts.png")
        self.imageUntenRechts = pygame.image.load("jahresarbeit/Bilder/FroschUntenRechts.png")
        self.imageUntenLinks = pygame.image.load("jahresarbeit/Bilder/FroschUntenLinks.png")
        self.imageObenLinks = pygame.image.load("jahresarbeit/Bilder/FroschObenLinks.png")
        
        self.pos = pygame.math.Vector2(player_start_x, player_start_y)
        self.rect = self.imageOben.get_rect()
        self.rect.topleft = self.pos
        self.stopped = True
        self.lineareBewegung = True
        self.lives = 3
        self.dashReady = True
        self.DashCooldown = 180

        # Horizontale und vertikale Bewegung und Anzeige
    def user_input(self):
        self.geschwindigkeit_x = 0
        self.geschwindigkeit_y = 0

        anyEingabe = pygame.key.get_pressed()
        
        if not anyEingabe[pygame.K_w] and not anyEingabe[pygame.K_s] and not anyEingabe[pygame.K_a] and not anyEingabe[pygame.K_d]:
            self.stopped = True
            screen.blit(self.imageOben, self.rect)
        if anyEingabe[pygame.K_w] and self.lineareBewegung:
            self.stopped = False
            self.geschwindigkeit_y = -10
            screen.blit(self.imageOben, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.y -= 40
                self.dashReady = False
        if anyEingabe[pygame.K_s] and self.lineareBewegung and not anyEingabe[pygame.K_w]:
            self.stopped = False
            self.geschwindigkeit_y = 10
            screen.blit(self.imageUnten, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.y += 40
                self.dashReady = False
        if anyEingabe[pygame.K_a] and self.lineareBewegung:
            self.stopped = False
            self.geschwindigkeit_x = -10
            screen.blit(self.imageLinks, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.x -= 40
                self.dashReady = False
        if anyEingabe[pygame.K_d] and self.lineareBewegung and not anyEingabe[pygame.K_a]:
            self.stopped = False
            self.geschwindigkeit_x = 10
            screen.blit(self.imageRechts, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.x += 40
                self.dashReady = False

        # Diagonale Bewegung und Anzeige
        if anyEingabe[pygame.K_w] and anyEingabe[pygame.K_d]:
            self.lineareBewegung = False
            self.geschwindigkeit_y = -10
            self.geschwindigkeit_x = 10
            screen.blit(self.imageObenRechts, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.x += 40
                self.pos.y -= 40
                self.dashReady = False
        if anyEingabe[pygame.K_d] and anyEingabe[pygame.K_s] and not anyEingabe[pygame.K_a] and not anyEingabe[pygame.K_w]:
            self.lineareBewegung = False
            self.geschwindigkeit_y = 10
            self.geschwindigkeit_x = 10
            screen.blit(self.imageUntenRechts, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.x += 40
                self.pos.y += 40
                self.dashReady = False
        if anyEingabe[pygame.K_s] and anyEingabe[pygame.K_a]:
            self.lineareBewegung = False
            self.geschwindigkeit_y = 10
            self.geschwindigkeit_x = -10
            screen.blit(self.imageUntenLinks, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.x -= 40
                self.pos.y += 40
                self.dashReady = False
        if anyEingabe[pygame.K_a] and anyEingabe[pygame.K_w] and not anyEingabe[pygame.K_d] and not anyEingabe[pygame.K_s]:
            self.lineareBewegung = False
            self.geschwindigkeit_y = -10
            self.geschwindigkeit_x = -10
            screen.blit(self.imageObenLinks, self.rect)
            if anyEingabe[pygame.K_SPACE] and self.dashReady:
                self.pos.x -= 40
                self.pos.y -= 40
                self.dashReady = False

        # Behebung der diagonalen Geschwindigkeit
        if self.geschwindigkeit_x != 0 and self.geschwindigkeit_y != 0:
            self.geschwindigkeit_x /= math.sqrt(2)
            self.geschwindigkeit_y /= math.sqrt(2)  

    def move(self):
        self.pos += pygame.math.Vector2(self.geschwindigkeit_x, self.geschwindigkeit_y)
        self.rect.topleft = self.pos
    def dashCooldownTimer(self):
        if self.dashReady == False:
            self.DashCooldown -= 1
            if self.DashCooldown == 0:
                self.DashCooldown = 180
                self.dashReady = True
    def update(self):
        self.user_input()
        self.move()
        self.dashCooldownTimer()

player = Player()

# Rand erstellen
def Rand():
    Rand1 = Rect(340, 0, 10, 1020)
    Rand2 = Rect((1920-350), 0, 10, 1020)
    pygame.draw.rect(screen, (139,69,19), Rand1)
    pygame.draw.rect(screen, (139,69,19), Rand2)
    if player.pos[0] <= 350:
        player.pos[0] = 350
    if player.pos[0] >= 1920 - 51 - 350:
        player.pos[0] = 1920 - 51 - 350

    if player.pos[1] <= 0:
        player.pos[1] = 0
    if player.pos[1] >= 1010 - 51:
        player.pos[1] = 1010 - 51

# Zufallsgenerator für Koordinaten und Geschwindigkeit
def rx():
    return random.randint(350, 1920 - 10 - 350)
def ry():
    return random.randint(0, 1010 - 10)
def rg():
    n = 0
    while n == 0:
        n =  random.randint(-5, 5)
    return n
# Münze erstellen
class Münze(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)        
        self.image = pygame.image.load("Jahresarbeit/Bilder/münze.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos)
    # Kollision überprüfen
    def kollisionTest(self):
        if self.rect.colliderect(player.rect):
            self.pos = pygame.math.Vector2(random.randint(350, 1920 - 30 - 350), random.randint(0, 1010 - 30))
            self.rect.topleft = (self.pos)
            statistiken.ScoreCount += 1  
            i = random.randint(1, 3)
            if i == 1:
                enemyGroup.add(Enemy(rx(), ry(), rg(), rg()))
            münzeaufnehmen_sound.play()
    def update(self):
        screen.blit(self.image, self.rect)
        self.kollisionTest()

münze = Münze(random.randint(350, 1920 - 30 - 350), random.randint(0, 1010 - 30))

# Gegner erstellen
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, geschwindigkeit_x, geschwindigkeit_y):
        super().__init__()
        self.geschwindigkeit_x = geschwindigkeit_x
        self.geschwindigkeit_y = geschwindigkeit_y
        self.image = pygame.image.load("Jahresarbeit/Bilder/steine.png")
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
    def move(self):
        self.pos += (self.geschwindigkeit_x, self.geschwindigkeit_y)
        self.rect.topleft = self.pos
    def Randcheck(self):
        if self.pos[0] <= 350:
            self.pos[0] = 350
            self.geschwindigkeit_x *= -1
        if self.pos[0] >= 1920 - 10 - 350:
            self.pos[0] = 1920 - 10 - 350
            self.geschwindigkeit_x *= -1
        if self.pos[1] <= 0:
            self.pos[1] = 0
            self.geschwindigkeit_y *= -1
        if self.pos[1] >= 1010 - 10:
            self.pos[1] = 1010 - 10
            self.geschwindigkeit_y *= -1
    def kollisionTest(self):
        if pygame.sprite.spritecollide(player, enemyGroup, True):
            player.lives -= 1
            GegnerKollision_sound.play()
            if player.lives <= 0:
                player.pos = (1920/2 - 26, 1020/2 - 26)
                player.rect.topleft = player.pos
                screen.blit(player.imageOben, player.rect)
                global gameRunning
                gameRunning = False
                enemyGroup.empty() 
                enemyGroup.add(Enemy(rx(), ry(), rg(), rg()))
                enemyGroup.add(Enemy(rx(), ry(), rg(), rg()))
                enemyGroup.add(Enemy(rx(), ry(), rg(), rg())) 
                death_sound.play()
                if statistiken.ScoreCount > statistiken.HighscoreCount:
                    statistiken.HighscoreCount = statistiken.ScoreCount
            
    def update(self):
        self.move()
        self.Randcheck()
        self.kollisionTest()
            
enemyGroup = pygame.sprite.Group()
enemyGroup.add(Enemy(rx(), ry(), rg(), rg()))
enemyGroup.add(Enemy(rx(), ry(), rg(), rg()))
enemyGroup.add(Enemy(rx(), ry(), rg(), rg()))

# Punkteanzeige erstellen
font = pygame.font.SysFont("microsoftsansserif", 50, True, True)
class Statistiken(object):
    def __init__(self):
        self.imageScoreboard = pygame.transform.rotozoom(pygame.image.load("Jahresarbeit/Bilder/Highscore.png"), 0, 1.45)
        self.ScoreCount = 0
        self.HighscoreCount = 0
        self.imageHerz = pygame.transform.rotozoom(pygame.image.load("Jahresarbeit/Bilder/FroschLife.png"), 0, 1.5)
    def highsScoreUpdate(self):
        highscoreText = font.render(str(self.HighscoreCount), 1, (0, 0, 0))
        screen.blit(highscoreText, (1700, 365))
    def scoreUpdate(self):
        scoreText = font.render("Score: " + str(self.ScoreCount), 1, (200, 200, 10))
        screen.blit(scoreText, (1620, 480))
    def playerLivesUpdate(self):
        if player.lives == 3:
            screen.blit(self.imageHerz, (20, 50))
            screen.blit(self.imageHerz, (20 + 100, 50))
            screen.blit(self.imageHerz, (20 + 100 + 100, 50))
        if player.lives == 2:
            screen.blit(self.imageHerz, (20, 50))
            screen.blit(self.imageHerz, (20 + 100, 50))
        if player.lives == 1:
            screen.blit(self.imageHerz, (20, 50))
    def update(self):
        screen.blit(statistiken.imageScoreboard, (1920 - 312, 300))
        self.highsScoreUpdate()
        self.scoreUpdate()
        self.playerLivesUpdate()

statistiken = Statistiken()

# Healfeld erstellen
class Heal(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("Jahresarbeit/Bilder/heal.png")
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(random.randint(350, 1920 - 40 - 350), random.randint(0, 1010 - 40))
        self.rect.topleft = self.pos
        self.Status = True

    def spawnTime(self):
        if self.Status:
            screen.blit(heal.image, heal.rect)  
            if player.rect.colliderect(heal.rect) and player.lives < 3:
                player.lives += 1
                self.pos = (random.randint(350, 1920 - 40 - 350), random.randint(0, 1010 - 40))
                self.rect.topleft = self.pos
                self.Status = False
                HPaufnehmen_sound.play()
        else:
            if random.randint(0, 1000) == 0:
                self.Status = True

heal = Heal()

# Infotexte erstellen und anzeigen
DashCooldownInSekunden = 0
font1 = pygame.font.SysFont("microsoftsansserif", 30, True, True)
class Info(object):
    def __init__(self):
        self.imageSteuerung = pygame.image.load("Jahresarbeit/Bilder/steuerung.png")
    def startText(self):
        startText = font.render("Drücke 'P' um das Spiel zu starten!", 1, (255, 255, 255))
        screen.blit(startText, (600, 300))
    def drawDashText(self):
        DashText = font1.render("[Leertaste = Sprung]", 1, (255, 255, 255))
        screen.blit(DashText, (35, 800))
    def dashBereitText(self):
        if player.DashCooldown <= 180:
            DashCooldownInSekunden = 3
            if player.DashCooldown <= 120:
                DashCooldownInSekunden = 2
                if player.DashCooldown <= 60:
                    DashCooldownInSekunden = 1
        if player.dashReady:
            DashBereitText = font1.render("Sprung: Bereit", 1, (0, 255, 0))
            screen.blit(DashBereitText, (40, 700))
        else:
            DashNichtBereitText = font1.render("Sprung bereit in: %d" % (DashCooldownInSekunden), 1, (255, 0, 0))
            screen.blit(DashNichtBereitText, (40, 700))
    def steuerungText(self):
        screen.blit(self.imageSteuerung, (70, 350))
    def update(self):
        self.drawDashText()
        self.dashBereitText()
        self.steuerungText()
        
info = Info()

# Hintergrundmusik hinzufügen
background_music = pygame.mixer_music.load("Jahresarbeit/Musik_Sound/Froschgame.mp3")
pygame.mixer.music.play(-1)
background_music_volume = 0.3
pygame.mixer_music.set_volume(background_music_volume)

# Soundeffekte hinzufügen
death_s = 0.5
death_sound = pygame.mixer.Sound("Jahresarbeit/Musik_Sound/FroschDead.mp3")
death_sound.set_volume(death_s)
münzen_s = 0.025
münzeaufnehmen_sound = pygame.mixer.Sound("Jahresarbeit/Musik_Sound/münzeaufnehmen.mp3")
münzeaufnehmen_sound.set_volume(münzen_s)
HP_s = 0.1
HPaufnehmen_sound = pygame.mixer.Sound("Jahresarbeit/Musik_Sound/heilen.mp3")
HPaufnehmen_sound.set_volume(HP_s)
G_s = 0.5
GegnerKollision_sound = pygame.mixer.Sound("Jahresarbeit/Musik_Sound/GegnerKollisionSound.mp3")
GegnerKollision_sound.set_volume(G_s)

class Volume(object):
    def __init__(self):
        self.imageVolUp = pygame.image.load("Jahresarbeit/Bilder/volumeUP.png")
        self.imageVolUp_rect = self.imageVolUp.get_rect()
        self.imageVolUP_pos = pygame.math.Vector2(1830, 900)
        self.imageVolUp_rect.center = self.imageVolUP_pos

        self.imageVolDOWN = pygame.image.load("Jahresarbeit/Bilder/volumeDOWN.png")
        self.imageVolDOWN_rect = self.imageVolDOWN.get_rect()
        self.imageVolDOWN_pos = pygame.math.Vector2(1670, 900)
        self.imageVolDOWN_rect.center = self.imageVolDOWN_pos

        self.imageVolUp1 = pygame.image.load("Jahresarbeit/Bilder/volumeUP1.png")
        self.imageVolUp1_rect = self.imageVolUp1.get_rect()
        self.imageVolUP1_pos = pygame.math.Vector2(1830, 700)
        self.imageVolUp1_rect.center = self.imageVolUP1_pos

        self.imageVolDOWN1 = pygame.image.load("Jahresarbeit/Bilder/volumeDOWN1.png")
        self.imageVolDOWN1_rect = self.imageVolDOWN1.get_rect()
        self.imageVolDOWN1_pos = pygame.math.Vector2(1670, 700)
        self.imageVolDOWN1_rect.center = self.imageVolDOWN1_pos

    def drawSoundButtons(self):
        SoundText = font1.render("Sound", 1, (230, 230, 230))
        screen.blit(SoundText, (1680, 800))
        screen.blit(self.imageVolUp, self.imageVolUp_rect)
        screen.blit(self.imageVolDOWN, self.imageVolDOWN_rect)
    def drawMusicButtons(self):
        MusicText = font1.render("Musik", 1, (230, 230, 230))
        screen.blit(MusicText, (1680, 600))
        screen.blit(self.imageVolUp1, self.imageVolUp1_rect)
        screen.blit(self.imageVolDOWN1, self.imageVolDOWN1_rect)
    def update(self):
        self.drawSoundButtons()
        self.drawMusicButtons()

volume = Volume()

# Hauptschleife
while True:
    screen.fill(background)
    screen.blit(spielfeldImage, spielfeldRect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_p:
                if gameRunning != True:
                    statistiken.ScoreCount = 0
                    player.lives = 3
                gameRunning = True
        elif event.type == KEYUP:
            player.lineareBewegung = True
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.math.Vector2(event.pos)
            if math.dist(mouse_pos, volume.imageVolDOWN_pos) <= 25:
                death_s -= 0.1
                death_sound.set_volume(death_s)
                münzen_s -= 0.005
                münzeaufnehmen_sound.set_volume(münzen_s)
                HP_s -= 0.02
                HPaufnehmen_sound.set_volume(HP_s)
                G_s -= 0.1
                GegnerKollision_sound.set_volume(G_s)
            if math.dist(mouse_pos, volume.imageVolUP_pos) <= 25:
                death_s += 0.1
                death_sound.set_volume(death_s)
                münzen_s += 0.005
                münzeaufnehmen_sound.set_volume(münzen_s)
                HP_s += 0.02
                HPaufnehmen_sound.set_volume(HP_s)
                G_s += 0.1
                GegnerKollision_sound.set_volume(G_s)
            if math.dist(mouse_pos, volume.imageVolDOWN1_pos) <= 25:
                background_music_volume -= 0.05
                if background_music_volume <= 0:
                    background_music_volume = 0
                pygame.mixer_music.set_volume(background_music_volume)
            if math.dist(mouse_pos, volume.imageVolUP1_pos) <= 25:
                background_music_volume += 0.05
                if background_music_volume >= 1:
                    background_music_volume = 1
                pygame.mixer_music.set_volume(background_music_volume)



    Rand()
    münze.update()
    statistiken.update()
    heal.spawnTime()
    for enemy in enemyGroup:
        screen.blit(enemy.image, enemy.rect)

    if gameRunning == False:
        screen.blit(player.imageOben, player.rect)
        info.startText()
        
    if gameRunning:
        player.update()
        for enemy in enemyGroup:
            enemy.update()
    info.update()
    volume.update()

    
    pygame.display.update()
    fpsClock.tick(fps)
