import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	''' a class to manage bullet'''

	def __init__(self, ai_settings, screen, piggy, y_position):
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.y_position = y_position
		# create a bullet rect at (0, 0) position
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		
		# bullet initial position depends on the projectile number
		self.rect.centery = piggy.rect.centery + 10 + self.y_position
		
		# x coordinate does not change for each projectile
		self.rect.right = piggy.rect.left
		# store bullet x-coordinate as float to fine tune the speed of bullet
		self.x = float(self.rect.x)

		self.color = ai_settings.bullet_color
		self.speed = ai_settings.bullet_speed

	def update(self):
		''' update the position of bullet'''
		self.x -= self.speed
		# update that position to the bullet rect y-coordinate
		self.rect.x = self.x

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)