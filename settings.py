class Settings():
	''' to store all settings for alien_invasion'''
	def __init__(self):
		''' the static settings'''
		self.screen_height = 500
		self.screen_width = 1200
		# background needs to be sky blue
		self.background_color = (50, 100, 200)

		# bullet settings
		self.bullet_width = 15
		self.bullet_height = 3
		# bullet is pink
		self.bullet_color = (200, 100, 50)
		self.bullet_speed = 10
		# maximum projectiles allowed per shot
		self.max_projectile = 5
		# set the distance between the projectles fired at the same time
		self.between_projectile = 5
		# flag to determine whether bullet firing is on
		self.open_fire = False

		# rock settings
		self.small_rock_speed = 4
		self.medium_rock_speed = 3
		self.big_rock_speed = 2

		# max number of shield one can have
		self.max_shield = 3
		
		# scale for rock hp, points, and number when progression in rounds
		self.rock_scale = 1.5

		# reward settings
		self.reward_speed = 2

		self.initialize_dynamic_settings()

		# reset settings related to rewards
		self.reset_reward_settings()

	def reset_reward_settings(self):
		# how many projectiles shot out with one spacebar press
		self.projectile_number = 5
		# how many shields the ship has currently
		self.shield_number = 0
		# piggy's speed increases when getting the corresponding rewards
		self.piggy_speed = 4

	def initialize_dynamic_settings(self):
		''' the following settings change throughout the game'''
		# how many points earned shooting down one alien
		self.small_rock_points = 20
		self.medium_rock_points = 40
		self.big_rock_points = 80
		# hp of each type of rock
		self.small_rock_hp = 20
		self.medium_rock_hp = 50
		self.big_rock_hp = 100
		# maximum number of rocks allowed on the screen at the same time
		self.number_of_rocks = 10
		