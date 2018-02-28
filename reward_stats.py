from random import randint

class RewardStats():
	''' a class to represent stats for the reward system'''
	''' reward M is to increase projectile number
		reward P is to power-up bullet
		reward S is to add one shield'''
	def __init__(self, rock_flag):
		# set the probability of each reward appearing
		self.rock_flag = rock_flag
		
		if self.rock_flag == "S":
			# probability of reward M, P, S, and no reward appearing in a small rock
			self.prob_m = 0
			self.prob_p = 0
			self.prob_s = 0
			self.prob_none = 100

		if self.rock_flag == "M":
			# probability of reward M, P, S, and no reward appearing in a medium rock
			self.prob_m = 2
			self.prob_p = 2
			self.prob_s = 1
			self.prob_none = 95

		if self.rock_flag == "B":
			# probability of reward M, P, S, and no reward appearing in a big rock
			self.prob_m = 20
			self.prob_p = 20
			self.prob_s = 10
			self.prob_none = 50

	def assign_reward(self):
		list_m = list(range(1, self.prob_m + 1))
		list_p = list(range(self.prob_m + 1, self.prob_m + self.prob_p + 1))
		list_s = list(range(self.prob_m + self.prob_p + 1, self.prob_m + self.prob_p + self.prob_s + 1))
		list_none = list(range(self.prob_m + self.prob_p + self.prob_s + 1, 
			self.prob_m + self.prob_p + self.prob_s + self.prob_none + 1))
		
		test_number = randint(1, 100)

		if test_number in list_m:
			return("M")
		if test_number in list_p:
			return("P")
		if test_number in list_s:
			return("S")
		if test_number in list_none:
			return False
