import pickle
import os


class GameHandler:
	def __init__(self, directory=None):
		self.directory = directory or "./SavedGame"
		self.path = "{directory}/Game.save".format(directory=self.directory)
	
	
	def createDirectory(self, directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError:
			print('Error: Creating directory: ' + directory)
		
	def saveGame(self, game):
		try:
			self.createDirectory(self.directory)
			path = self.path
			pickle.dump(game, open(path, 'wb'))
		except:
			print("Error: Could not save game.")


	def loadGame(self):
		user_input = ""
		while user_input != 'Y' and user_input != 'N':
			user_input = input("Enter 'Y' to confirm or 'N' to cancel: ")
			user_input = user_input.upper()
		path = self.path
		loadedGame = None
		if user_input == 'Y':
			if os.path.exists(path):
				try: 
					loadedGame = pickle.load(open(path, 'rb'))
				except pickle.UnpicklingError:
						print("Error: Could not load game.");
			else:
				print("Error: There are no saved games at: {path}".format(path=path))
		return loadedGame
