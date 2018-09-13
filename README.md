# GAME_flying_piggy
Developed with pygame

_A major project inspired by Chapter 12 of "Python Crash Course"._

Game Overview:

* Player controls a flying piggy, trying to avoid all the square rocks for as long as possible.
* Flying piggy can shoot bullets to destroy rocks. The bigger the rock, the more likelihood there is a reward upon destroying the rock (probability of each type of rock carrying rewards can be found in reward_stats). The three types of rocks appear with different probability, and they also carry different HP.
* There are three rewards: 
  * power-up (boosting up the power of each bullet)
  * multiply projectile (allowing shooting of multiple bullets at a time)
  * shield (protecting flying piggy from one rock contact. Shield can accumulate, meaning if the piggy acquires significant amount of shields, it can smash through rocks unharmed until all shields are gone).
*  The scoring system is determined by destroying a rock (earning the most points) and letting a rock pass through the screen (earning less points). The three types of rocks carry different amount of points upon destruction and pass-through. 
* There is no end to the game by itself. The game levels up once the player reaches the target score required. Each new level, there is no change to the rocks or piggy. The only change is that rocks’ HP and points scale up, as well as the target score for the new level. 
* The longer a player can remain in the game, the better. Player only has one life. Once the flying piggy is touched by a rock, the game is over. The goal is to achieve the highest score possible, which translates as destroying as many rocks as possible (as destroying rocks earns more points) and/or staying in the game for as long as possible (as allowing more rocks to pass by also earns points).
