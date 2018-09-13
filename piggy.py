'''
Author: Fanchen Bao
Date: 1/28/2018

Description:
Piggy class
'''

import pygame
from pygame.sprite import Sprite

class Piggy(Sprite):
	def __init__(self, screen, ai_settings):
		super().__init__()
		'''initialize ship and determine its original position on screen'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.speed = self.ai_settings.piggy_speed

		#load the ship image and get its rect
		self.image = pygame.image.load('images/flying_piggy.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()

		self.image_width = self.rect.width
		self.image_height = self.rect.height

		# start new ship at the right center of screen
		self.rect.centery = self.screen_rect.centery
		self.rect.right = self.screen_rect.right
		# store a decimal value for the ship's center
		self.center_x = float(self.rect.centerx)
		self.center_y = float(self.rect.centery)
		# movement flag
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		''' update new position of piggy based on the movement flag, which itself is based on user key input'''
		''' piggy will NOT disappear from the edge'''
		if self.moving_right:
			self.center_x += self.speed
			self.current_right = self.center_x + self.image_width/2
			if self.current_right > self.screen_rect.right:
				self.center_x = self.screen_rect.right - self.image_width/2
		if self.moving_left:
			self.center_x -= self.speed
			self.current_left = self.center_x - self.image_width/2
			if self.current_left < self.screen_rect.left:
				self.center_x = self.screen_rect.left + self.image_width/2
		if self.moving_down:
			self.center_y += self.speed
			self.current_bottom = self.center_y + self.image_height/2
			if self.current_bottom > self.screen_rect.bottom:
				self.center_y = self.screen_rect.bottom - self.image_height/2
		if self.moving_up:
			self.center_y -= self.speed
			self.current_top = self.center_y - self.image_height/2
			if self.current_top < self.screen_rect.top:
				self.center_y = self.screen_rect.top + self.image_height/2
		
		# set the current piggy position
		self.rect.centerx = self.center_x
		self.rect.centery = self.center_y


	def blitme(self):
		''' draw the ship at its current location'''
		self.screen.blit(self.image, self.rect)