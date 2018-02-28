import pygame.font
from pygame.sprite import Group

class ScoreBoard():
	''' a class to record and draw scores on the screen'''
	
	def __init__(self, screen, ai_settings, stats):
		''' initialize scoreboard'''
		self.screen = screen
		self.ai_settings = ai_settings
		self.stats = stats

		self.screen_rect = screen.get_rect()

		# setting font for score
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 28)

		# draw score information on the screen
		self.prep_score()
		self.prep_target_score()
		self.prep_round()
		self.prep_status()
		self.prep_high_round()

	def prep_score(self):
		''' convert score information into image'''
		# round the score to the nearest 10 (if the second argument is 1, that means to ronud to nearest 0.1)
		rounded_score = round(self.stats.score, -1)
		# syntax to insert comma to long number
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.score_image_rect = self.score_image.get_rect()
		self.score_image_rect.centerx = self.screen_rect.centerx
		self.score_image_rect.top = 10

	def prep_target_score(self):
		''' convert high score into image'''
		rounded_target_score = round(self.ai_settings.target_score, -1)
		# syntax to insert comma to long number
		target_score_str = "Target Score: " + "{:,}".format(rounded_target_score)
		self.target_score_image = self.font.render(target_score_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.target_score_image_rect = self.score_image.get_rect()
		self.target_score_image_rect.centerx = self.screen_rect.centerx
		self.target_score_image_rect.top = 50

	def prep_round(self):
		''' convert round information into image'''
		round_str = "Round " + str(self.stats.round)
		self.round_image = self.font.render(round_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.round_image_rect = self.round_image.get_rect()
		self.round_image_rect.left = 10
		self.round_image_rect.top = 10

	def prep_status(self):
		pass

	def prep_high_round(self):
		''' convert round information into image'''
		high_round_str = "Highest Round: " + str(self.stats.high_round)
		self.high_round_image = self.font.render(high_round_str, True, self.text_color, 
			self.ai_settings.background_color)
		self.high_round_image_rect = self.round_image.get_rect()
		self.high_round_image_rect.left = 10
		self.high_round_image_rect.top = 50

	def show_score(self):
		''' draw score information on the screen'''
		self.screen.blit(self.score_image, self.score_image_rect)
		self.screen.blit(self.target_score_image, self.target_score_image_rect)
		self.screen.blit(self.round_image, self.round_image_rect)
		self.screen.blit(self.high_round_image, self.high_round_image_rect)