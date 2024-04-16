# Simulation d'un decollage de fusee vers Jupiter
# auteur : Paul Juillard 2024

import pygame
pygame.init()
pygame.font.init()
import math
import random

from systeme_solaire import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

### REMPLIR LA FONCTION TRAJECTOIRE ICI
# solution à effacer
# a = -0.002
# b = 0
# c = 591

a = ____
b = ____
c = ____

def trajectoire(x):
	return a * (x - b) * (x - c)

def main():
	run = True
	clock = pygame.time.Clock()

	# Le système solaire
	angular_speed = 2 * math.pi / (20 * 60 * TIMESTEP)
	earth = Planet(0, - 150 * SCALE, angular_speed , 16, BLUE)
	jupyter = Planet(0, - 500 * SCALE, angular_speed * 0.7, 24, RED)
	asteroids = Asteroids(0, -300*SCALE, angular_speed * 0.95, (40, 80))
	planets = [earth, jupyter, asteroids]

	# La fusée
	fusee = Rocket(earth,trajectoire)


    bigfont = pygame.font.SysFont('Corbel',58, bold=True)
    text_gagne = bigfont.render('Réussi' , True , (100,100,100))
    text_perdu = bigfont.render('Explosé' , True , (100,100,100))

	reussi = False
	perdu = False

	try:

		#debut de la simulation

		while run:
			clock.tick(60)
			WIN.fill((0, 0, 0))
			draw_sun(WIN)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False
					if event.key == pygame.K_SPACE:
						pass
			for planet in planets:
				if not reussi :
					planet.update_position(TIMESTEP)
				planet.draw(WIN)

			if earth.y <= 0 and not fusee.launched:
				fusee.launch()

			if not (perdu or reussi) :
				fusee.update_position(TIMESTEP)

			if asteroids.collision(fusee.x, fusee.y, 10):
				fusee.explosion()
				perdu = True

			if jupyter.collision(fusee.x, fusee.y):
				reussi = atterrissage(a, b, c)
				perdu = not atterrissage(a, b, c)
				if perdu:
					fusee.explosion()

			if fusee.x > WIDTH/2 or fusee.y > HEIGHT / 2 or fusee.x < -WIDTH/2 or fusee.y < -HEIGHT/2:
				perdu = True

			if perdu :
				WIN.blit(text_perdu, (100, 100))
			if reussi :
				WIN.blit(text_gagne, (100, 100))

			fusee.draw(WIN)

			pygame.display.update()

		pygame.quit()

	except Exception as e:

		pygame.quit()
		raise e


main()