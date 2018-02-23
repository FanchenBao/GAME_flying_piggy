import pygame
from pygame.sprite import Group
from settings import Settings
from piggy import Piggy
from button import Button
from rock_stats import RockStats
# from score_board import ScoreBoard
import game_functions as gf
from game_stats import GameStats

def run_game():
	# initialize game and create a screen object.
	
	# initialize game
	pygame.init()

	# create game display
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Flying Piggy")

	# create an instance to store game stats
	filename = 'high_score.txt'
	stats = GameStats(ai_settings, filename)

	piggy = Piggy(screen, ai_settings)
	bullets = Group()
	
	rocks = Group()
	rock_stats = RockStats()
	
	# rewards = Group()
	# shields = Group()

	# create a play button
	msg1 = 'Round ' + str(stats.level)
	msg2 = 'Press "P" to Play'
	play_button = Button(screen, ai_settings, msg1, msg2)

	# score_board = ScoreBoard(screen, ai_settings, stats)
	
	gf.create_initial_rocks(screen, ai_settings, rock_stats, rocks)
	
	# The main loop of the game
	while True:
		gf.check_events(piggy, ai_settings, stats)
		if stats.game_active:
			piggy.update()
			gf.fire_bullet(ai_settings, screen, piggy, bullets)
			gf.update_bullets(bullets)
			gf.update_rocks(screen, ai_settings, rock_stats, rocks)
			# gf.update_aliens(stats, aliens, bullets, ship, screen, ai_settings, score_board, rewards, missiles, shields)
			# gf.update_rewards(ship, rewards, ai_settings, stats, score_board, shields, screen)
			# gf.update_missiles(stats, aliens, bullets, ship, screen, ai_settings, score_board, rewards, missiles, shields)
			# gf.update_shields(shields, missiles, ai_settings, aliens)
		gf.update_screen(ai_settings, screen, piggy, bullets, stats, play_button, rocks)
		
run_game()