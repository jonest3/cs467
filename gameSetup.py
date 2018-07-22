from gameEngine import Player, Room, Item
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


	def getFilesInDir(self, directory):
		path = self.basePath + "{directory}/".format(directory=directory)
		files = []
		try:
			files = os.listdir(path)	
		except:
			print("Error: Could not read files from path: {path}.".format(path=path))
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
						print(roomDict[key].Floor[len(roomDict[key].Floor) - 1].Name)
					else:
						print("Error: {item} does not exist.".format(item=item))

				for item in shelves:
					if self.items[item]:
						itemObj = self.items[item]	
						roomDict[key].add_shelf(itemObj)
						print(roomDict[key].Shelves[len(roomDict[key].Shelves) - 1].Name)
					else:
						print("Error: {item} does not exist.".format(item=item))
		return roomDict


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
		

	def getRoom(self, room_name):
		if self.rooms[room_name]:
			return self.rooms[room_name]
		else:
			return None

game = GameComponents()
game.getNeighbors()

"""
rooms = list(game.rooms)
for room in rooms:
#   print("------------")
   rObj = game.rooms[room]
#   print("Room: {name}".format(name=rObj.Name))
   neighbors = rObj.Neighbors
   for neighbor in neighbors:
	break
#	print(neighbor.Name)

items = list(game.items)
for item in items:
#   print("____________")
   iObj = game.items[item]
#   print("Item: {name}".format(name=iObj.Name))

game.rooms["nexus"].Visited = True

neighbors = game.rooms["library"].Neighbors
for room in neighbors:
	if room.Name == "Nexus":
		print("Nexus Visited: {visited}".format(visited=room.Visited))

game.rooms["treasureRoom"].enter()
game.rooms["treasureRoom"].enter()
"""

currentRoom = game.player._Location
currentRoom.enter()
print("-- Test Taking Item --")
item = raw_input("Enter Item: ")
game.player.take(item)
currentRoom.enter()

