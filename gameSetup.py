from gameEngine import Player, Room, Item, Door, Shelf
from testGame import TestGame
import pickle
import json
import os


MAX_MOVES = 30


class GameComponents:
	def __init__(self):
		self.basePath = "./InitGame/"
		self.items = self.loadItems()
#		self.traps = self.loadTraps()
		self.rooms = self.loadRooms()
		self.player = Player(self.getRoom("helicopterPad"), MAX_MOVES)
		self.getDoorDestinations()
		self.getItemDestinations()
	
	# @param:  directory - the name of the directory to get all files in
	# 
 	# returns: list of files in parsed directory.  Will return empty list if error occurs 
	def getFilesInDir(self, directory):
		path = self.basePath + "{directory}/".format(directory=directory)
		if os.path.exists(path):
			files = []
			try:
				files = os.listdir(path)	
			except:
				print("Error: Could not read files from path: {path}.".format(path=path))
			return files
		else:
			print("Error: No such path: {path}.".format(path=path))
			exit()


	# @param: directory - directory file is in
	# @param: filename - the name of the file to retreive object from
	#
	# returns: object loaded from file or 'None' if error occurs
	def getFileObj(self, directory, filename):
		path = self.basePath + "{directory}/{fname}".format(directory=directory, fname=filename)
		if os.path.exists(path):
			try:
				with open(path, 'r') as data_file:
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
				desc = room["longDesc"]
				shortDesc = room["shortDesc"]
				roomDict[key] = Room(name, desc, shortDesc)
				
				for item in room["items"]["floor"]:
					if self.items[item]:
						itemObj = self.items[item]
						roomDict[key].add_item(itemObj)
					else:
						print("Error: {item} does not exist.".format(item=item))

				for shelf in room["items"]["shelves"]:
					sName = shelf["name"]
					sDesc = shelf["desc"]
					sLocked = True if shelf["locked"] == "True" else False
					sLockVal = shelf["lock_val"] if shelf["lock_val"] != "" else None
					contents = shelf["contents"]
					shelfObj = Shelf(sName, sDesc, sLocked, sLockVal)					
	
					for item in contents:
						if self.items[item]:
							itemObj = self.items[item]		
							shelfObj.add_item(itemObj)
						else:
							print("Error: {item} does not exist.".format(item=item))

					roomDict[key].add_shelf(shelfObj)
				for door in room["doors"]:
					dName = door["name"]
					dDesc = door["desc"]
					unlock_desc = door["unlock_desc"] if door["unlock_desc"] != "" else None
					direction = door["direction"]
					lock_val = door["lock_val"] if door["lock_val"] != "" else None
					destination = door["neighbor"]
					locked = True if door["locked"] == "True" else False
					doorObj = Door(dName, dDesc, direction, destination, locked, lock_val, unlock_desc)
					roomDict[key].add_door(doorObj)


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
				lock = item["lock_val"] if item["lock_val"] != "" else None
				trans_id = item["trans_id"] if item["trans_id"] != "" else None
				trap_desc = item["trap_desc"] if item["trap_desc"] != "" else None
				destination = item["destination"] if item["destination"] != "" else None
				itemDict[key] = Item(name, desc, key, lock, trans_id, trap_desc, destination)
		return itemDict

	
	# @param: room_name - name of room to return
	#
	# returns: room if it exists, else 'None'
	def getRoom(self, room_key):
		try:
			return self.rooms[room_key]
		except:
			return None

	def getItem(self, item_key):
		try:
			return self.items[item_key]
		except:
			return None

	def getDoorDestinations(self):
		for room in list(self.rooms):
			roomObj = self.rooms[room]
			for door in list(roomObj.Doors):
				neighbor_key = door.Destination
				neighbor = self.getRoom(neighbor_key)
				door.Destination = neighbor


	def getItemDestinations(self):
		for item in list(self.items):
			itemObj = self.items[item]
			if itemObj.Destination:
				room = itemObj.Destination
				itemObj.Destination = self.rooms[room]

	
	def saveGame(self, game):
		directory = "./SavedGame"
		path = "{directory}/Game.save".format(directory=directory)
		if not os.path.exists(directory):
			os.makedirs(directory)
		pickle.dump(game, open(path, 'wb'))

cont_game = 1
while cont_game:
#	gameState = input("Enter 'loadgame' or 'savegame': ")
#	directory = "./SavedGame"
#	path = "{directory}/Game.save".format(directory=directory)

#	if gameState == "loadgame":
#		game = pickle.load(open(path, 'rb'))			
#	else:
	game = GameComponents()
#	if gameState == "savegame":
#		 game.saveGame(game)
	tester = TestGame(game)
	cont_game = tester.main()
