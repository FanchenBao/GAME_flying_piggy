from random import randint

class RockStats():
	''' a class to represent stats for rock'''
	''' S is small rock
		M is medium rock
		B is big rock '''
	def __init__(self):
		# small rocks appear 60% of the time
		self.prob_s = 75
		# medium rocks appear 30% of the time
		self.prob_m = 20
		# big rocks appear 10% of the time
		self.prob_b = 5

	def assign_rock(self):
		list_s = list(range(1, self.prob_s + 1))
		list_m = list(range(self.prob_s + 1, self.prob_s + self.prob_m + 1))
		list_b = list(range(self.prob_s + self.prob_m + 1, self.prob_s + self.prob_m + self.prob_b + 1))
		
		test_number = randint(1, 100)
		
		if test_number in list_s:
			return("S")
		if test_number in list_m:
			return("M")
		if test_number in list_b:
			return("B")

	def assign_slope(self):
		slope_int = randint(-5, 5)
		slope_deci = randint(1, 9)
		slope = float(slope_int + 0.1 * slope_deci)
		return(slope)




