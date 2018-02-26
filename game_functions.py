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

def update_rocks(screen, ai_settings, rock_stats, rocks, piggy, stats):
	if len(rocks) < ai_settings.number_of_rocks:
		for i in range(ai_settings.number_of_rocks - len(rocks)):
			create_rock(screen, ai_settings, rock_stats, rocks)
	check_rock_edges(rocks)
	rocks.update()

	for rock in rocks.copy():
		if rock.rect.left >= rock.screen_rect.right:
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

def get_alien_per_row(ai_settings, alien_width):
	# determine how many aliens can fit in one row
	available_space_x = ai_settings.screen_width - alien_width * 2
	alien_per_row = int(available_space_x / (alien_width * 2))
	return(alien_per_row)

def get_row_per_screen(ai_settings, alien_height, ship_height):
	# determine how many rows of aliens can fit in one screen
	available_space_y = ai_settings.screen_height - alien_height * 3 - ship_height
	row_per_screen = int(available_space_y / (alien_height * 2))
	return(row_per_screen)

def create_alien(screen, ai_settings, number_of_alien, number_of_row, aliens, alien_count):
	alien = Alien(screen, ai_settings)
	# each new alien is positioned to the right of the previous one with one alien width of space in between
	alien.x = alien.rect.x + number_of_alien * alien.rect.width * 2
	alien_y = alien.rect.y + number_of_row * alien.rect.height * 2
	alien.rect.x = alien.x
	alien.rect.y = alien_y
	# each alien has a different tag number
	alien.number = alien_count
	aliens.add(alien)

def create_alien_fleet(screen, ai_settings, aliens, ship, stats):
	# create a default alien which is NOT added to the alien fleet
	default_alien = Alien(screen, ai_settings)
	alien_per_row = get_alien_per_row(ai_settings, default_alien.rect.width)
	#max_row_per_screen = get_row_per_screen(ai_settings, default_alien.rect.height, ship.rect.height)
	
	row_per_screen = ai_settings.rows_each_level(stats)
	total_alien = alien_per_row * row_per_screen
	alien_count = 0
	# create a full fleet
	for number_of_row in range(row_per_screen):
		for number_of_alien in range(alien_per_row):
			create_alien(screen, ai_settings, number_of_alien, number_of_row, aliens, alien_count)
			alien_count += 1
	# create an instance of reward_stats, based on the game level
	if stats.level >= 4:
		reward_stats = RewardStats(stats.level)

		# find the aliens that will carry the reward
		designated_aliens = sample(range(total_alien), reward_stats.number_of_reward)
		for alien in aliens:
			if alien.number in designated_aliens:
				alien.reward_flag = reward_stats.assign_reward()

def change_fleet_direction(aliens, ai_settings):
	''' change fleet direction and move aliens down'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.alien_drop_speed
	ai_settings.fleet_direction *= -1	

def check_fleet_edges(aliens, ai_settings, screen, missiles):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(aliens, ai_settings)
			fire_missile(missiles, ai_settings, aliens, screen)
			break

def fire_missile(missiles, ai_settings, aliens, screen):
	# create a missle that is fired by a randomly selected alien
	# reassign numbers so that all aliens are in the pool for random selection for firing missle
	reassign_alien_number(aliens)
	
	# do not change the missile_number parameter in settings, use a proxy to accept changes
	missile_number = ai_settings.missile_number
	
	# if number of alien is smaller than missile number, make missile number always 1 smaller than alien number
	if len(aliens) < missile_number:
		missile_number = len(aliens) - 1
	# choose randomly the number of aliens to fire missile
	designated_aliens = sample(range(len(aliens)), missile_number)

	for alien in aliens.sprites():
		# find the designated alien
		if alien.number in designated_aliens:
			if len(missiles) < missile_number:
				# make the missile
				missile = Missile(ai_settings, screen, alien)
				missiles.add(missile)

def reassign_alien_number(aliens):
	count = 0
	for alien in aliens.sprites():
		alien.number = count
		count += 1

def update_missiles(stats, aliens, bullets, ship, screen, ai_settings, score_board, rewards, missiles, shields):
	missiles.update()
	# delete missiles that have traveled outside the screen from the Group
	for missile in missiles.copy():
		if missile.rect.top >= missile.screen_rect.bottom:
			missiles.remove(missile)
			stats.score += ai_settings.missile_points
			score_board.prep_score()

	check_missile_ship_collision(stats, aliens, bullets, ship, screen, ai_settings, score_board, rewards, missiles, shields)

def check_missile_ship_collision(stats, aliens, bullets, ship, screen, ai_settings, score_board, rewards, missiles, shields):
	# check to see whether a missile has hit the ship
	if pygame.sprite.spritecollideany(ship, missiles):
		ship_hit(stats, aliens, bullets, ship, screen, ai_settings, score_board, rewards, missiles, shields)

def alien_hit_bottom(aliens):
	for alien in aliens.sprites():
		if alien.rect.bottom >= alien.screen_rect.bottom:
			return True
			break



def check_key_down_event(event, stats, piggy, rocks, bullets, screen, ai_settings, rock_stats):
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
	# 	# save high score and then quit
	# 	record_high_score(stats.high_score, filename)
		sys.exit()

	# press "P" to play the game	
	elif event.key == pygame.K_p:
		if not stats.game_active:
	# 		# restart or start a new game
			game_restart(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats)
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

def check_events(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats):
	# an event loop to monitor user's input (press key or move mouse)
	# The one below checks whether user clicks to close the program.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# save high score and then quit
			# record_high_score(stats.high_score, filename)
			sys.exit()
		# check whether the event is a key press
		elif event.type == pygame.KEYDOWN:
			check_key_down_event(event, stats, piggy, rocks, bullets, screen, ai_settings, rock_stats)
		elif event.type == pygame.KEYUP:
			check_key_up_event(event, piggy, ai_settings)


		# check for mouseclick on play button
		# elif event.type == pygame.MOUSEBUTTONDOWN:
		# 	mouse_x, mouse_y = pygame.mouse.get_pos()
		# 	check_play_button(play_button, stats, mouse_x, mouse_y, aliens, bullets, screen, ai_settings, ship)

def record_high_score(high_score, filename):
	'''record high score in a separate file so that each new game starts with a previous high score'''
	str_high_score = str(high_score)
	with open(filename, 'w') as file_object:
		file_object.write(str_high_score) 

def check_play_button(play_button, stats, mouse_x, mouse_y, aliens, bullets, screen, ai_settings, ship):
	# click play_button to play the game again
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked:
		# to prevent clicking the button area (without button present) 
		# and restarting the game. Game restarts ONLY when game inactive and mouse click
		if not stats.game_active:
			game_restart(stats, aliens, bullets, screen, ai_settings, ship)
			# hide the mouse cursor
			pygame.mouse.set_visible(False)

def game_restart(stats, piggy, rocks, bullets, screen, ai_settings, rock_stats):
	# restart the game by resetting stats and clearing out remnants of previous game
	stats.game_active = True
	
	# reset all the stats
	stats.reset_stats()
	ai_settings.reset_reward_settings()
	ai_settings.initialize_dynamic_settings()

	# reset all the scoreboard images
	# prep_scoreboard_images(score_board)

	# empty out any remaining rocks, bullets, shields
	rocks.empty()
	bullets.empty()
	shields.empty()

	# create new rocks
	create_initial_rocks(screen, ai_settings, rock_stats, rocks)
	
	#reposition piggy to right center position
	piggy.center_x = piggy.screen_rect.right - piggy.rect.width / 2
	piggy.center_y = piggy.screen_rect.centery

def prep_scoreboard_images(score_board):
	score_board.prep_score()
	score_board.prep_level()
	score_board.prep_ships()
	
def update_screen(ai_settings, screen, piggy, bullets, stats, play_button, rocks, rewards, shields):
	# redraw the scren during each pass of the loop
	screen.fill(ai_settings.background_color)
	# draw each bullet BEHIND the ship, so bullet drawn ahead of ship
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	piggy.blitme()
	rocks.draw(screen)
	# aliens.draw(screen)
	rewards.draw(screen)
	# for missile in missiles.sprites():
	# 	missile.draw_missile()
	shields.draw(screen)
	
	# # draw the play button only when game is inactive
	if not stats.game_active:
		play_button.draw_button()

	# score_board.show_score()

	# display the most recently drawn screen.
	pygame.display.flip()

def update_bullets(screen, ai_settings, rocks, bullets, rewards):
	# update bullet position and delete extra bullets
	bullets.update()

	# delete bullets that have traveled outside the screen from the Group
	for bullet in bullets.copy():
		if bullet.rect.right <= 0:
			bullets.remove(bullet)

	check_bullet_rock_collision(screen, ai_settings, rocks, bullets, rewards)

def check_bullet_rock_collision(screen, ai_settings, rocks, bullets, rewards):
	# check to see whether a bullet has hit an alien. If so, remove both the bullet and alien.
	collisions = pygame.sprite.groupcollide(rocks, bullets, False, True)
	if collisions:
		for rock, bullets in collisions.items():
			# update the damage on each rock
			rock.damage += len(bullets)

			if rock.damage >= rock.hp:
				if rock.reward_flag:
					create_reward(screen, ai_settings, rock, rewards)
				rocks.remove(rock)

		# 	# calculate score
		# 	stats.score += ai_settings.alien_points * len(aliens)
		# 	score_board.prep_score()

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

def check_high_score(stats, score_board):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		score_board.prep_high_score()

