import sys
import pygame
from bullet import Bullet
from rock import Rock
from reward_stats import RewardStats
from reward import Reward
# from missile import Missile
from shield import Shield
# from time import clock
# from random import sample

def create_rock(screen, ai_settings, rock_stats, rocks):
	# create a rock and assign its random flag and trajectory slope
	rock_flag = rock_stats.assign_rock()
	slope = rock_stats.assign_slope()
	reward_stats = RewardStats(rock_flag)
	reward_flag = reward_stats.assign_reward()
	new_rock = Rock(screen, ai_settings, rock_flag, slope, reward_flag)
	rocks.add(new_rock)

def create_initial_rocks(screen, ai_settings, rock_stats, rocks):
	for i in range(ai_settings.number_of_rocks):
		create_rock(screen, ai_settings, rock_stats, rocks)

def update_rocks(screen, ai_settings, rock_stats, rocks, piggy, stats, score_board):
	if len(rocks) < ai_settings.number_of_rocks:
		for i in range(ai_settings.number_of_rocks - len(rocks)):
			create_rock(screen, ai_settings, rock_stats, rocks)
	check_rock_edges(rocks)
	rocks.update()

	for rock in rocks.copy():
		if rock.rect.left >= rock.screen_rect.right:
			stats.score += rock.points
			score_board.prep_score()
			rocks.remove(rock)

	if pygame.sprite.spritecollideany(piggy, rocks):
		piggy_hit(stats)

def piggy_hit(stats):
	'''when piggy got hit by a rock, game over'''
	# set game to inactive and prompt a player response
	stats.game_active = False
	pygame.mouse.set_visible(True)

def check_rock_edges(rocks):
	# whenever a rock hits the up and down edge, change its trajectory slope as if it has bounced on the edge
	for rock in rocks.sprites():
		if rock.check_edges():
			rock.rock_direction *= (-1)

def check_offensive_reward(reward_flag, ai_settings):
	# increase number of projectiles per shot
	if reward_flag == "M":
		if ai_settings.projectile_number < ai_settings.max_projectile:
			ai_settings.projectile_number += 1
	# power-up each bullet
	if reward_flag == "P":
		ai_settings.bullet_power += 1

def check_defensive_reward(reward_flag, shields, screen, ai_settings, piggy):
	# make a shield
	if reward_flag == "S":
		ai_settings.shield_number += 1
		create_shield(shields, screen, ai_settings, piggy)

def create_reward(screen, ai_settings, rock, rewards):
	# create a new reward at the same position where a designated rock is hit
	reward = Reward(screen, ai_settings, rock.reward_flag, rock.x_speed)
	reward.rect.centerx = rock.rect.centerx
	reward.rect.centery = rock.rect.centery
	reward.x = float(reward.rect.x)
	rewards.add(reward)

def update_rewards(shields, screen, ai_settings, piggy, rewards):
	# update reward position and delete reward when it hits piggy or disappears off the screen
	rewards.update()

	# delete rewards that have traveled outside the screen from the Group
	for reward in rewards.copy():
		if reward.rect.left >= reward.screen_rect.right:
			rewards.remove(reward)

	check_reward_piggy_collision(shields, screen, ai_settings, piggy, rewards)

def check_reward_piggy_collision(shields, screen, ai_settings, piggy, rewards):
	# check whether a reward has hit the piggy
	# record the reward
	reward = pygame.sprite.spritecollideany(piggy, rewards)
	if reward:
		check_offensive_reward(reward.reward_flag, ai_settings)
		check_defensive_reward(reward.reward_flag, shields, screen, ai_settings, piggy)
		# remove the reward that has hit the ship
		rewards.remove(reward)

def create_shield(shields, screen, ai_settings, piggy):
	# create shield based on how many S reward player has collected
	# note that all shields will be stacked on top of each other, so the amount won't be able to tell from the screen
	shield = Shield(screen, ai_settings, piggy)
	shields.add(shield)

def update_shields(shields, ai_settings, rocks):
	# update shield position and its behavior once got hit by missile
	shields.update()

	collisions_rock_shield = pygame.sprite.groupcollide(rocks, shields, True, False)
	if collisions_rock_shield:
		ai_settings.shield_number -= 1
		if ai_settings.shield_number == 0:
			shields.empty()


def fire_bullet(ai_settings, screen, piggy, bullets):
	# fire a bullet if the limit is not reached yet and when open_fire is true
	if ai_settings.open_fire:
		if len(bullets) == 0:
			# when there is no bullet, create one no matter what
			create_bullet(ai_settings, bullets, screen, piggy)
		else:
			# when there are already bullets, next bullet doesn't fire 
			# until the previous one is 10 pixels above the ship
			for bullet in bullets.sprites():
				if (piggy.rect.left - bullet.rect.right) < 40:
					return
			create_bullet(ai_settings, bullets, screen, piggy)

def create_bullet(ai_settings, bullets, screen, piggy):
	# create a single bullet
	# bullet's y_position depends on the number of projectiles. This is to set highest projectile postion
	y_position = (ai_settings.projectile_number-1) * (-ai_settings.between_projectile)
	for projectile in range(ai_settings.projectile_number):
		new_bullet = Bullet(ai_settings, screen, piggy, y_position)
		bullets.add(new_bullet)
		# each new projectile is 2 y_position down the earlier projectile
		y_position += 2 * ai_settings.between_projectile


def check_key_down_event(event, stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename):
	# determine action when key is pushed down
	if event.key == pygame.K_RIGHT:
		# set the moving flag to true so that ship continues moving right
		piggy.moving_right = True
	elif event.key == pygame.K_LEFT:
		# set the moving flag to true so that ship continues moving left
		piggy.moving_left = True
	elif event.key == pygame.K_UP:
		# move up
		piggy.moving_up = True
	elif event.key == pygame.K_DOWN:
		# move down
		piggy.moving_down = True

	elif event.key == pygame.K_SPACE:
		# create bullets when spacebar is pressed down
		ai_settings.open_fire = True
	elif event.key == pygame.K_q:
		# save high round and then quit
		record_high_round(stats.high_round, filename)
		sys.exit()

	# press "P" to play the game	
	elif event.key == pygame.K_p:
		if not stats.game_active:
	# 		# restart or start a new game
			game_restart(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename)
	# 		# hide the mouse cursor
	# 		pygame.mouse.set_visible(False)

def check_key_up_event(event, piggy, ai_settings):
	# determine action when key is released
	if event.key == pygame.K_RIGHT:
	# set the moving flag to false so that ship stops moving when right arrow key is released
		piggy.moving_right = False
	elif event.key == pygame.K_LEFT:
	# set the moving flag to false so that ship stops moving when left arrow key is released
		piggy.moving_left = False
	elif event.key == pygame.K_UP:
		# not move up
		piggy.moving_up = False
	elif event.key == pygame.K_DOWN:
		# not move down
		piggy.moving_down = False
	elif event.key == pygame.K_SPACE:
		# stop firing bullets when spacebar is lifted
		ai_settings.open_fire = False

def check_events(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename):
	# an event loop to monitor user's input (press key or move mouse)
	# The one below checks whether user clicks to close the program.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# save high score and then quit
			# record_high_score(stats.high_score, filename)
			sys.exit()
		# check whether the event is a key press
		elif event.type == pygame.KEYDOWN:
			check_key_down_event(event, stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename)
		elif event.type == pygame.KEYUP:
			check_key_up_event(event, piggy, ai_settings)


		# check for mouseclick on play button
		# elif event.type == pygame.MOUSEBUTTONDOWN:
		# 	mouse_x, mouse_y = pygame.mouse.get_pos()
		# 	check_play_button(play_button, stats, mouse_x, mouse_y, aliens, bullets, screen, ai_settings, ship)

def record_high_round(high_round, filename):
	'''record high round in a separate file so that each new game starts with a previous high score'''
	str_high_round = str(high_round)
	with open(filename, 'w') as file_object:
		file_object.write(str_high_round)

def game_restart(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats, shields, rewards, score_board, filename):
	# restart the game by resetting stats and clearing out remnants of previous game
	stats.game_active = True
	
	# reset all the stats
	stats.reset_stats()
	ai_settings.reset_reward_settings()
	ai_settings.initialize_dynamic_settings()

	# reset all the scoreboard images
	prep_scoreboard_images(score_board)

	# empty out any remaining rocks, bullets, shields
	rocks.empty()
	bullets.empty()
	shields.empty()
	rewards.empty()

	# create new rocks
	create_initial_rocks(screen, ai_settings, rock_stats, rocks)
	
	#reposition piggy to right center position
	piggy.center_x = piggy.screen_rect.right - piggy.rect.width / 2
	piggy.center_y = piggy.screen_rect.centery

def prep_scoreboard_images(score_board):
	score_board.prep_score()
	score_board.prep_target_score()
	score_board.prep_round()
	score_board.prep_high_round()
	
def update_screen(ai_settings, screen, piggy, bullets, stats, play_button, rocks, rewards, shields, score_board):
	# redraw the scren during each pass of the loop
	screen.fill(ai_settings.background_color)
	# draw each bullet BEHIND the ship, so bullet drawn ahead of ship
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	piggy.blitme()
	rocks.draw(screen)
	rewards.draw(screen)
	shields.draw(screen)
	
	# draw the play button only when game is inactive
	if not stats.game_active:
		play_button.draw_button()

	score_board.show_score()

	# display the most recently drawn screen.
	pygame.display.flip()

def update_bullets(screen, ai_settings, rocks, bullets, rewards, stats, score_board):
	# update bullet position and delete extra bullets
	bullets.update()

	# delete bullets that have traveled outside the screen from the Group
	for bullet in bullets.copy():
		if bullet.rect.right <= 0:
			bullets.remove(bullet)

	check_bullet_rock_collision(screen, ai_settings, rocks, bullets, rewards, stats, score_board)

def check_bullet_rock_collision(screen, ai_settings, rocks, bullets, rewards, stats, score_board):
	# check to see whether a bullet has hit an alien. If so, remove both the bullet and alien.
	collisions = pygame.sprite.groupcollide(rocks, bullets, False, True)
	if collisions:
		for rock, bullets in collisions.items():
			# update the damage on each rock
			rock.damage += len(bullets) * ai_settings.bullet_power

			if rock.damage >= rock.hp:
				if rock.reward_flag:
					create_reward(screen, ai_settings, rock, rewards)
				
				# calculate score
				stats.score += rock.points
				score_board.prep_score()

				# remove the destroyed rock
				rocks.remove(rock)

		# 	for alien in aliens:
		# 		if alien.reward_flag:
		# 			create_reward(screen, ai_settings, alien.reward_flag, rewards, alien)
		# check_high_score(stats, score_board)	

	# remove remaining bullets when all aliens are destroyed
	# if len(aliens) == 0:
	# 	bullets.empty()
	# 	rewards.empty()
	# 	missiles.empty()

	# 	# level up by increasing speed for every element
	# 	ai_settings.increase_speed()

	# 	# update level information
	# 	stats.level += 1
	# 	score_board.prep_level()

	# 	# update alien missile information
	# 	if ai_settings.missile_number < ai_settings.max_missile:
	# 		ai_settings.missile_number += 1

	# 	create_alien_fleet(screen, ai_settings, aliens, ship, stats)

	# 	# give a little pause
	# 	sleep(0.5)

def check_round(stats, score_board, ai_settings):
	if stats.score >= ai_settings.target_score:
		stats.round += 1
		score_board.prep_round()
		level_up(ai_settings)
		score_board.prep_target_score()


	if stats.round > stats.high_round:
		stats.high_round = stats.round
		score_board.prep_high_round()

def level_up(ai_settings):
	# all relevant game settings scale up after leveling up
	ai_settings.small_rock_points *= ai_settings.rock_scale
	ai_settings.medium_rock_points *= ai_settings.rock_scale
	ai_settings.big_rock_points *= ai_settings.rock_scale

	ai_settings.small_rock_hp *= ai_settings.rock_scale
	ai_settings.medium_rock_hp *= ai_settings.rock_scale
	ai_settings.big_rock_hp *= ai_settings.rock_scale

	ai_settings.piggy_speed *= ai_settings.rock_scale

	ai_settings.target_score *= ai_settings.rock_scale

