import pygame
from pygame.sprite import Sprite

class Reward(Sprite):
	def __init__(self, screen, ai_settings, reward_flag, x_speed):
		super().__init__()
		''' initialize the reward class'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = self.screen.get_rect()

		self.reward_flag = reward_flag
		# reward's speed depends on the x_speed of the rock that carries it
		self.speed = x_speed
		
		if self.reward_flag == "M":
			#load the projectile number increase image and get its rect
			self.image = pygame.image.load('images/M.bmp')

		if self.reward_flag == "P":
			#load the bullet power-up image and get its rect
			self.image = pygame.image.load('images/P.bmp')

		if self.reward_flag == "S":
			#load the shield image and get its rect
			self.image = pygame.image.load('images/S.bmp')

		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		# store a decimal value for reward's location for fine tuning position
		self.x = float(self.rect.x)

	def update(self):
		''' update the position of reward'''
		self.x += self.speed
		self.rect.x = self.x

	def blitme(self):
		''' draw the reward at its current location'''
		self.screen.blit(self.image, self.rect)















