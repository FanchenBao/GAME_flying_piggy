'''
Author: Fanchen Bao
Date: 02/20/2018

Description:
Shield class
'''

import pygame
from pygame.sprite import Sprite

class Shield(Sprite):
	def __init__(self, screen, ai_settings, piggy):
		super().__init__()
		'''initialize shield and determine its original position on screen'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.piggy = piggy

		#load the shield image and get its rect
		self.image = pygame.image.load('images/shield.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()


		# present shield ahead of the ship
		self.rect.centerx = self.piggy.rect.centerx
		self.rect.centery = self.piggy.rect.centery

		# store a decimal value for alien's location for fine tuning position
		self.center_x = float(self.rect.centerx)
		self.center_y = float(self.rect.centery)

	def update(self):
		self.center_x = self.piggy.center_x
		self.center_y = self.piggy.center_y
		self.rect.centerx = self.center_x
		self.rect.centery = self.center_y

	def blitme(self):
		''' draw the alien at its current location'''
		self.screen.blit(self.image, self.rect)