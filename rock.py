import pygame
from pygame.sprite import Sprite
from random import randint

class Rock(Sprite):
	def __init__(self, screen, ai_settings, rock_flag, slope, reward_flag):
		super().__init__()
		'''initialize alien and determine its original position on screen'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.rock_flag = rock_flag
		self.screen_rect = self.screen.get_rect()
		self.k = slope
		self.rock_direction = 1

		# record how many times a rock has been damaged
		self.damage = 0

		# determine which reward to give once the rock is eliminated
		self.reward_flag = reward_flag

		#load the rock image depending on which rock_flag is given
		if self.rock_flag == "S":
			self.image = pygame.image.load('images/small_rock.bmp')
			self.hp = ai_settings.small_rock_hp
			self.speed = float(ai_settings.small_rock_speed)

		if self.rock_flag == "M":
			#load the projectile number increase image and get its rect
			self.image = pygame.image.load('images/medium_rock.bmp')
			self.hp = ai_settings.medium_rock_hp
			self.speed = float(ai_settings.medium_rock_speed)

		if self.rock_flag == "B":
			#load the unlimited bullets image and get its rect
			self.image = pygame.image.load('images/big_rock.bmp')
			self.hp = ai_settings.big_rock_hp
			self.speed = float(ai_settings.big_rock_speed)


		#get rock rect
		self.rect = self.image.get_rect()
		# set rock flag initially to false
		self.rock_flag = False
		
		# new rock initial position (actual position is random)
		self.rect.x = -self.rect.width
		self.rect.y = randint(0, self.screen_rect.bottom - self.rect.height)

		# store a decimal value for rock's location for fine tuning position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
	def check_edges(self):
		'''check whether a rock has hit the top or bottom edge'''
		if self.rect.top <= 0:
			return True
		elif self.rect.bottom >= self.screen_rect.bottom:
			return True

	def update(self):
		''' update current rock position'''
		# slope of rock trajectory changes direction once it hits edge
		self.k *= self.rock_direction
		
		# get x, and y-axis speed
		self.x_speed = self.speed / ((1 + (self.k) ** 2) ** (1/2))
		self.y_speed = self.x_speed * self.k

		# update x, y coordinate
		self.x += self.x_speed
		self.y += self.y_speed

		# reassign position to rock rect
		self.rect.x = self.x
		self.rect.y = self.y

		

	def blitme(self):
		''' draw the alien at its current location'''
		self.screen.blit(self.image, self.rect)