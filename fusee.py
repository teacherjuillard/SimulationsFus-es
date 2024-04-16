# Simulation d'un decollage de fusee vers Jupiter
# auteur : Paul Juillard 2024
import pygame
import math

pygame.init()
pygame.font.init()

WIDTH, HEIGHT =  800, 800

class Fusee(pygame.sprite.Sprite):
    def __init__(self, reservoir_gauche, reservoir_droit):
        """
        x and y at the bottom center of the rocket
        """
        x, y, w, h = 0.5*WIDTH, 0.8*HEIGHT-15, 150, 300
        super().__init__()
        self.rg = reservoir_gauche
        self.image = pygame.image.load("cohete_off.png")
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x - w/2
        self.rect.y = y - h

    def update(self):
        self.rect.y = self.rg.rect.y - 75

class Reservoir(pygame.sprite.Sprite):
    def __init__(self, rayon, cote):
        """
        x and y at the bottom center of the rocket
        """
        super().__init__()

        self.rayon = rayon

        x, y, w, h = 0, 0, 0, 0
        if cote == "gauche":
            x, y, w, h = 0.5*WIDTH - 150/4 - rayon*5, 0.8*HEIGHT + 10, rayon*15, 250
        elif cote == "droit":
            x, y, w, h = 0.5*WIDTH + 150/4 + rayon*5, 0.8*HEIGHT + 10, rayon*15, 250
        self.h = h
        self.r = w/2
        self.outline = pygame.image.load("rocket_outline.png")
        self.outline = pygame.transform.scale(self.outline, (w, h))
        self.fuel = pygame.image.load("rocket_red.png")
        self.fuel = pygame.transform.scale(self.fuel, (w, h))
        self.booster = pygame.image.load("booster.png")
        self.booster = pygame.transform.scale(self.booster, (w*0.7, h*97/330*0.5))
        self.image = self.outline.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x - w/2
        self.rect.y = y - h
        self.origin_y = y-h
        self.allume = False
        self.boom = False

    def update(self):
        if self.boom:
            return

        # décollage
        if self.allume and self.quantite > 0 and self.rect.y > -self.h:
            self.rect.y -= 2
            self.quantite -= 2 * self.rayon / 7.7
            if self.quantite <= 0:
                self.image = self.outline.copy()
            self.update_image()

        # chute
        elif self.allume and self.quantite <= 0 and self.rect.y > -self.h and self.rect.y <= self.origin_y:
            self.rect.y += 4

        # "atterissage"
        elif self.allume and self.quantite <= 0 and self.rect.y > self.origin_y:
            self.explosion()

        elif self.allume:
            return

    def update_image(self):
        if self.allume and self.quantite > 0:
            self.image.blit(self.booster, (15, self.h*0.8))
        self.fuel.set_alpha(255 * self.quantite / self.quantite_max)
        self.image.blit(self.outline, (0,0))
        self.image.blit(self.fuel, (0,0))

    def remplir(self, quantite):
        self.quantite_max = 0.8 * HEIGHT
        self.quantite = quantite / 275 * 0.8 * HEIGHT
        self.update_image()

    def decollage(self):
        self.allume = True

    def explosion(self):
        self.boom = True
        print("explosion")
        explosion = pygame.image.load("explosion_Boom_2.png")
        explosion = pygame.transform.scale(explosion, (self.r*2, self.r*2))
        self.image.blit(explosion, (0,self.h/3))


def decollage(rayon, quantite, rg, rd):
    print("decollage", rayon, quantite)
    if quantite / rayon > 73 : #or quantite / rayon < 70 :
        print("decollage :", quantite/rayon)
        # 560 / 7.7 = 72.7
        rg.explosion()
        rd.explosion()

    else :
        rg.decollage()
        rd.decollage()

def simulation(carburant_total, rayon, fusee, reservoir_gauche, reservoir_droit):

    ### Initialisation
    pygame.init()
    pygame.font.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Planet Simulation")
    background = pygame.image.load("landscape.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    WIN.blit(background, (0,0))
    pygame.draw.line(WIN, (0,0,0), (0, 0.8*HEIGHT), (WIDTH, 0.8*HEIGHT))

    # Bouton de décollage
    smallfont = pygame.font.SysFont('Corbel',40, bold=True)

    text = smallfont.render('Décollage' , True , (100,100,100))
    button_coord = (50,50)
    button_size = (200, 50)

    # ecrans de fins
    bigfont = pygame.font.SysFont('Corbel',58, bold=True)
    gagne = bigfont.render('Gagné' , True , (100,100,100))
    perdu = bigfont.render('Perdu' , True , (100,100,100))

    ### Objets a simuler
    fusees = pygame.sprite.Group()
    fusees.add(fusee)
    fusees.add(reservoir_gauche)
    fusees.add(reservoir_droit)

    ### Boucle de simulation
    done = False
    reussi = False

    try :
        # Simulation
        while not done:

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse[0] >= button_coord[0] and mouse[0] <= button_coord[0] + button_size[0]:
                        if mouse[1] >= button_coord[1] and mouse[1] <= button_coord[1] + button_size[1]:
                            decollage(rayon, carburant_total, reservoir_gauche, reservoir_droit)


            fusees.update()

            # background
            # WIN.blit(background, (0.33*WIDTH, 0), [0.33* WIDTH, 0, 0.6*WIDTH, HEIGHT])

            WIN.blit(background, (0,0))
            pygame.draw.line(WIN, (0,0,0), (0, 0.8*HEIGHT), (WIDTH, 0.8*HEIGHT))

            # button
            pygame.draw.rect(WIN,(150, 150, 150),[button_coord[0], button_coord[1],button_size[0], button_size[1]])
            WIN.blit(text,(button_coord[0] + 10, button_coord[1] + 10))

            # others
            fusees.draw(WIN)
            pygame.display.update()

            if reservoir_gauche.rect.y <= -reservoir_gauche.h:
                done = True
                reussi = True
                print("reussi", reservoir_gauche.quantite)
            elif reservoir_gauche.boom:
                pygame.time.wait(1000)
                done = True
                reussi = False
                print("perdu")

        # Ecran de fin
        done = False

        if reussi :
            WIN.fill((10, 235, 10))
            WIN.blit(gagne, (WIDTH/2 - 70, HEIGHT/2))
        else :
            WIN.fill((230, 10, 10 ))
            WIN.blit(perdu, (WIDTH/2 - 70, HEIGHT/2))

        pygame.display.update()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.QUIT:
                    done = True

    except Exception as e:
        pygame.quit()
        raise e

    pygame.quit()
    print("pygame_quit")