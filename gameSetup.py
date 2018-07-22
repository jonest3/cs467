from gameEngine import Player, Room, Item
from testGame import TestGame
import pickle
import json
import os


MAX_MOVES = 30


class GameComponents:
	def __init__(self, loadSaved=False):
		self.loadSaved = loadSaved
		self.basePath = "./SavedGame/" if loadSaved else "./InitGame/"
		self.items = self.loadItems()
#		self.doors = self.loadDoors()
#		self.traips = self.loadTraps()
		self.rooms = self.loadRooms()
		self.player = Player(self.getRoom("helicopterPad"), MAX_MOVES)


	
	# @param:  directory - the name of the directory to get all files in
	# 
 	# returns: list of files in parsed directory.  Will return empty list if error occurs 
	def getFilesInDir(self, directory):
		path = self.basePath + "{directory}/".format(directory=directory)
		files = []
		try:
			files = os.listdir(path)	
		except:
			print("Error: Could not read files from path: {path}.".format(path=path))
		return files


	# @param: directory - directory file is in
	# @param: filename - the name of the file to retreive object from
	#
	# returns: object loaded from file or 'None' if error occurs
	def getFileObj(self, directory, filename):
		path = self.basePath + "{directory}/{fname}".format(directory=directory, fname=filename)
		if os.path.exists(path):
			try:
				with open(path, 'r') as data_file:
					if self.loadSaved:
						return pickle.load(data_file)
					else:
						return json.load(data_file)	 
			except:
				print("Error: Could not load from {path}.".format(path=path))
		else:
			print("Error: No such path: {path}.".format(path=path))
		return None


	# @param: None
	#
	# returns: dict of instantiated Room objects for every room file stored in the rooms directory
	def loadRooms(self):
		roomDict = {}
		room_files = self.getFilesInDir("Rooms")
		for filename in room_files:
			room = self.getFileObj("Rooms", filename)
			if room:
				key = room["key"]
				name = room["name"]
				longDesc = room["longDesc"]
				shortDesc = room["shortDesc"]
				neighbors = room["neighbors"]
				shelves = room["items"]["shelves"]
				floor = room["items"]["floor"]
				roomDict[key] = Room(name, longDesc, shortDesc)
				roomDict[key].Neighbors = neighbors
				
				for item in floor:
					if self.items[item]:
						itemObj = self.items[item]
						roomDict[key].add_item(itemObj)
					else:
						print("Error: {item} does not exist.".format(item=item))

				for item in shelves:
					if self.items[item]:
						itemObj = self.items[item]	
						roomDict[key].add_shelf(itemObj)
					else:
						print("Error: {item} does not exist.".format(item=item))
		return roomDict



	# @param: None
	#
	# returns: dict of instantiated Item objects for every item file stored in the items directory
	def loadItems(self):
		itemDict = {}
		item_files = self.getFilesInDir("Items")
		for filename in item_files:
			item = self.getFileObj("Items", filename)
			if item:
				name = item["name"]
				desc = item["desc"]
				key = item["key_val"]
				itemDict[key] = Item(name, desc, key)
		return itemDict

	

	# @param: None
	#
	# returns: None
	#
	# Used to link neighbors and rooms
	def getNeighbors(self):
		rooms_list = list(self.rooms)
		if len(rooms_list):
			for room in rooms_list:
				roomObj = self.rooms[room]
				neighbors = roomObj.Neighbors
				roomObj.Neighbors = []
				for neighbor in neighbors:
					neighborObj = self.rooms[neighbor]
					roomObj.add_neighbor(neighborObj)
		

	# @param: room_name - name of room to return
	#
	# returns: room if it exists, else 'None'
	def getRoom(self, room_name):
		try:
			return self.rooms[room_name]
		except:
			return None


game = GameComponents()
game.getNeighbors()

tester = TestGame(game)
tester.main()
