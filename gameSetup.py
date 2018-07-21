from gameEngine import Player
import pickle
import json
import os

MAX_MOVES = 12

#def load(path)


class GameComponents:
	def __init__(self, loadSaved=False):
		self.loadSaved = loadSaved
		# self.player = Player(location, MAX_MOVES)
		'''
		self.roomList = ['helicopterPad', 'treasureRoom', 'bridgeRoom', 
				 'antechamber', 'waterfall', 'nexus', 'crypt', 
				 'tortureRoom', 'library','potionsRoom', 'greenhouse',
				 'muralRoom', 'rootRoom', 'dragonRoom', 'cave']
		'''
		self.basePath = "./SavedGame/" if loadSaved else "./InitGame/"
		self.roomFiles = self.getFiles("Rooms");
#		self.itemFiles = self.getFiles("Items");
#		self.doorFiles = self.getFiles("Doors");
#		self.shelfFiles = self.getFiles("Shelf");
#		self.trapFiles = self.getFiles("Traps");



	def getFiles(self, directory):
		path = self.basePath + "{directory}/".format(directory=directory)
		try:
			files = os.listdir(path)# [f for f in os.listdir(path) if isfile(join(path, f))]
			print(files)
		except:
			print("Error: Could not read files from path: {path}.".format(path=path))
			files = []
		
		return files

	def getFileObj(self, directory, filename):
		path = self.basePath + "{directory}/{fname}".format(directory=directory, fname=filename)
		if os.path.exists(path):
			try:
				with open(path, 'rb') as data_file:
					if self.loadSaved:
						return pickle.load(data_file)
					else:
						return json.load(data_file)	 
			except:
				print("Error: Could not load from {path}.".format(path=path))
		else:
			print("Error: No such path: {path}.".format(path=path))
		
		return None
'''
	def loadRooms(self):
		for name in self.roomList:
			room_path = self.getPath("Rooms", name);
			if os.path.exists(room_path):
				
			else: 

	def getPath(self, className, filename):
		if self.loadSaved:
			return "./SavedGame/{className}/{filename}.save".format(className=className, filename=filename)
		else:
			return "./{className}/{filename}.json".format(className=className, filename=filename)
'''

game = GameComponents();

for filename in game.roomFiles:
	print(filename)
	obj = game.getFileObj("Rooms", filename)
	if obj:
		print(obj["name"]);


