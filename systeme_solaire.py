# Simulation d'un decollage de fusee vers Jupiter
# auteur : Paul Juillard 2024
import pygame
import math
import random

WIDTH, HEIGHT =  1200, 1200

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (240, 137, 19)
DARK_GREY = (80, 78, 81)


TIMESTEP = 1
SCALE = 1

class Planet:

	def __init__(self, x, y, speed, radius, color):
		self.x = x
		self.y = y

		self.r = math.sqrt(x**2 + y**2)
		self.theta = math.acos(x/self.r)
		self.speed = - speed

		self.radius = radius
		self.color = color


	def draw(self, win):
		x = self.x * SCALE + WIDTH / 2
		y = self.y * SCALE + HEIGHT / 2
		pygame.draw.circle(win, self.color, (x, y), self.radius)

	def update_position(self, time):
		self.theta = self.theta + self.speed * time
		self.x = math.cos(self.theta) * self.r
		self.y = math.sin(self.theta) * self.r

	def collision(self, x, y, margin = 0):
			distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
			return (distance - margin) < self.radius

class Asteroids(pygame.sprite.Sprite):

	def __init__(self, x, y, speed, size):
		super().__init__()

		self.x = x
		self.y = y
		self.size = size

		self.r = math.sqrt(x**2 + y**2)
		self.theta = math.acos(x/self.r)
		self.speed = -speed

		self.image = pygame.image.load("asteroids.png")
		self.image = pygame.transform.scale(self.image, size)

	def draw(self, win):
		x = self.x * SCALE + WIDTH / 2
		y = self.y * SCALE + HEIGHT / 2
		rotated = pygame.transform.rotate(self.image, - self.theta * 360 / (2 * math.pi))
		win.blit(rotated, (x, y))

	def update_position(self, time):
		self.theta = self.theta + self.speed * time
		self.x = math.cos(self.theta) * self.r
		self.y = math.sin(self.theta) * self.r

	def collision(self, x, y, margin = 0):

			distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
			return (distance - margin) < self.size[0] / 2


class Rocket(pygame.sprite.Sprite):

	def __init__(self, earth, trajectory):
		super().__init__()
		self.earth = earth
		self.x = earth.x
		self.y = earth.y

		self.image = pygame.image.load("Cohete_off.png")
		self.image = pygame.transform.scale(self.image, (25, 25))
		self.image = pygame.transform.rotate(self.image, -90)
		self.rect = self.image.get_rect()
		self.rect.x = earth.x
		self.rect.y = earth.y

		self.trajectory = trajectory
		self.trace = []

		self.vel = 0

		self.launched = False
		self.exploded = False

	def launch(self):
		self.speed = 1
		self.launched = True
		self.ox = self.x
		self.oy = self.y

		print("launch")


	def draw(self, win):
		if self.launched:
			self.rect.x = self.x + WIDTH/2
			self.rect.y = self.y + HEIGHT/2
			win.blit(self.image, (self.rect.x, self.rect.y))

			self.trace.append(self.rect.center)
			if(len(self.trace) > 2):
				pygame.draw.lines(win, BLUE, False, self.trace)

	def update_position(self, step):
		if self.launched and not self.exploded:
			speed = 3
			self.y = self.oy - self.trajectory((self.x - self.ox) * 1.8)
			self.x += step * speed

		elif not self.exploded:
			self.x = self.earth.x
			self.y = self.earth.y

	def explosion(self):
		if not self.exploded :
			print("explosion")
			self.image = pygame.image.load("explosion_Boom_2.png")
			self.image = pygame.transform.scale(self.image, (30, 30))
		self.exploded = True

def draw_sun(win):
	pygame.draw.circle(win, YELLOW, (WIDTH / 2, HEIGHT/2), 30)

def atterrissage(a, b, c):
	return a == -0.001 and ((b == 0 and c == 591) or (c == 0 and b == 591))

