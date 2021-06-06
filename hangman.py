import random
import re
import time
import os

class Hangman:
	help_menu = '''
\U0001F47E ctrl + d / ctrl + c - to leave the game
\U0001F47E >help  - to view this menu
\U0001F47E >about - about
\U0001F47E >rules - rules of the game
	'''
	game_symbols = {
	'heart' : '\U0001F9E1',
	'player_icon_healthy':'\U0001F601',
	'player_icon_critical':'\U0001F635',
	'player_icon_victory':'\U0001F929',
	'player_icon_dead':'\U0001F480',
	'player_icon_left':'\U0001F921'
	}
	def __init__(self):
		pass

	def __init__(self, difficulty):
		'''The init method is for setting up the important game variables'''

		self.movie_name = random.choice(["inception", "tenet","interstellar","martian","parasite"])

		chars_in_name = ''.join(set(self.movie_name))
		# print(len(chars_in_name))
		if difficulty == 1:
			self.lives = len(chars_in_name)

		elif difficulty == 2:
			self.lives = len(chars_in_name) + 5

		else:
			self.lives = len(chars_in_name) + 10

		self.max_lives = self.lives #for keeping track of the max lives


	def play(self):
		already_guessed_flag, wrong_guess_flag = None, None # This flag helps in checking if the character is already guessed and
		#accordingly helps to print the message
		if " " in self.movie_name:
			self.reg_str = r'^\s '
			print(re.sub(r'\S','*',self.movie_name))
		else:
			self.reg_str = '^'

		self.print_data() # prints the data for the player
		while self.lives != 0:
			try:
				guess = input("type here: ").lower()
				if guess == ">help":
					print(self.help_menu)
					continue
				elif guess == ">about":
					self.about()
					continue
				elif guess == ">rules":
					self.rules()
					continue

			except EOFError:
				self.status = 'q'
				break
			except KeyboardInterrupt:
				self.status = 'q'
				break

			try:
				if guess in self.reg_str:
					if guess == "s" and re.search(r'(\w|\s)s+',self.reg_str) == None:
						self.reg_str += guess
					else:
						already_guessed_flag = True
				else:
					already_guessed_flag = False
					if guess in self.movie_name:
						wrong_guess_flag = False
						self.reg_str += guess
					else:
						wrong_guess_flag = True
						self.lives -= 1

			except:
				print(re.sub("Name of the movie: ",r'\w','*',self.movie_name))

			try:
				if self.movie_name == re.sub(f'[{self.reg_str}]','*',self.movie_name):
					self.status = 'w'
					# print(self.player_stats, self.lives * Hangman.game_symbols['player_icon_dead'])
					break
			except:
				continue

			finally:
				if os.name == 'posix':
					_ = os.system('clear')
				else:
					_ = os.system('cls')
				self.print_data() # prints the data for the player
				if already_guessed_flag:
					print("Already guessed that")
				if wrong_guess_flag:
					print("Wrong guess")

	@staticmethod
	def about():
		print("About the game")

	@staticmethod
	def rules():
		print("You know the rules and so do I!")

	@property
	def player_stats(self):
		if self.lives > int(self.max_lives / 2):
			stats_message = f'''{self.game_symbols['player_icon_healthy']} Lives {self.lives} '''
		else:
			stats_message = f'''{self.game_symbols['player_icon_critical']} Lives {self.lives} '''


		return stats_message

	def print_data(self):
		'''helper function to print the data'''
		print("type '>help' to view the in game options available")
		if self.lives:
			print(self.player_stats, self.lives * self.game_symbols['heart'])

			try:
				print("Name of the movie: ",re.sub(f'[{self.reg_str}]','*',self.movie_name))
			except:
				print("Name of the movie: ",re.sub(r'\w','*',self.movie_name))


game = Hangman
menu =f'''
--------------------------------------
|	  The Hangman Game           |
|------------------------------------|
|-> New game (press n or N)          |
|-> Exit game (press q or Q)         |
|-> Rules of the game (press r or R) |
|-> About (press a or A)             |
--------------------------------------
'''

difficulty_menu = f'''
Difficulty
-------------------------------------
|(1) Mom pick me up I'm scared \U0001F480   |
|(2) No mercy \U0001F479                    |
|(3) Walk in the park \U0001F476            |
-------------------------------------
'''
print(menu)
while True:
	user_decision = str(input("Make a choice : ")).lower()


	if user_decision == "n":
		try:
			print(difficulty_menu)
			difficulty = int(input("your choice (1 2 or 3): "))
		except:
			print("Didn't make a valid choice, setting diffficulty to 'walk in the park'")
			difficulty = 3
		finally:
			hangman = Hangman(difficulty = difficulty)
			game_begins = time.time()
			hangman.play()
			game_ends = time.time()

	elif user_decision == "a":
		game.about()

	elif user_decision == "r":
		game.rules()

	else:
		break

	try:
		if hangman.lives == 0:
			print(3*Hangman.game_symbols['player_icon_dead'],"Hangman's dead!",3*Hangman.game_symbols['player_icon_dead'])
			show_ans = input("Want to see the answer ?(y/n)")
			if show_ans.lower() == "y":
				print(f"Name of the movie : {hangman.movie_name}")
			break
		elif hangman.status == 'w':
			print(3*Hangman.game_symbols['player_icon_victory'],"You win!",3*Hangman.game_symbols['player_icon_victory'])
			print(f"You guesed the correct answer in {game_ends-game_begins} second(s)!")
			break
		elif hangman.status == 'q':
			print(3*Hangman.game_symbols['player_icon_left'],"Player left the game",3*Hangman.game_symbols['player_icon_left'])
			break

	except:
		continue


# add the about and rules of the game

