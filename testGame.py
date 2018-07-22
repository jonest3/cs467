class TestGame:
	def __init__(self, game):
		self.game = game

	def playerDetails(self):
		player = self.game.player
		if player:
			print("\n-- Player Details --\n")
			print("Current Location: {location}".format(location=player._Location.Name))
			print("Turns Remaining: {turns}".format(turns=player.Turns_Left))
			print("Bag Contents:")
			for item in player.Bag:
				print(item.Name)			



	def printItemDetails(self, item_name):
		item = self.game.items[item_name]
		print("---------")
		print("Item: {name}".format(name=item.Name))
		print("Desc: {desc}".format(desc=item.Desc))
		print("KeyVal: {key}".format(key=item.KeyVal))



	def itemsDetails(self):
		print("\n-- Item Details --\n")
		items = list(self.game.items)
		for item in items:
			self.printItemDetails(item)


	def printRoomDetails(self, room_name):
		room = self.game.rooms[room_name]
		print("--------")
		print("Room: {name}".format(name=room.Name))
		print("Long Desc: {lDesc}".format(lDesc=room.LongDesc))
		print("\nShort Desc:  {sDesc}".format(sDesc=room.ShortDesc))
		print("\nFloor Items:")
		floor = room.Floor
		for item in floor:
			self.printItemDetails(item.KeyVal)
		print("\nShelf Items:")
		shelf = room.Shelves
		for item in shelf:
			self.printItemDetails(item.KeyVal)


	def roomsDetails(self):
		print("\n-- Room Details --\n")
		rooms = self.game.rooms
		for room in rooms:
			self.printRoomDetails(room)


	def testEnteringAllRooms(self):
		print("\n-- Testing Entering All Rooms --\n")
		rooms = list(self.game.rooms)
		for room in rooms:
			self.testRoomEnter(room)


	def testRoomEnter(self):
		print("\n-- Testing Entering Room --\n")
		room = self.game.player._Location
		room.enter()
		print("--------------------")	


	def testPlayerTake(self):
		print("\n-- Testing Taking Item --\n")
		room = self.game.player._Location
		print("--- Enter Room ---")
		room.enter()
		self.playerDetails()
		take_item = input("\n\nEnter Item to take: ")
		self.game.player.take(take_item)		
		print("-- Show Room Again --")
		print("\n--- item should be missing ---")
		room.enter()
		self.playerDetails()
		
		
	def testPlayerDrop(self):
		print("\n-- Test Dropping Item --\n")
		print("Player Details:")
		self.playerDetails()
		drop_item = input("\n\nEnter Item to drop: ")
		self.game.player.drop(drop_item)


	def testPlayerMove(self):
		print("\n-- Test Player Moving --\n")
		self.playerDetails()
		print("Possible Rooms to Choose:")
		room = self.game.player._Location
		for neighbor in room.Neighbors:
			print("-{name}".format(name=neighbor.Name))
			
		move_to = input("\n\nEnter Room to Move to: ")
		self.game.player.move(move_to)


	def numToTest(self, argument):
		switcher = {
			1: self.playerDetails,
			2: self.itemsDetails,
			3: self.roomsDetails,
			4: self.testPlayerTake,
			5: self.testEnteringAllRooms,
			6: self.testRoomEnter,
			7: self.testPlayerDrop,
			8: self.testPlayerMove
		}
		func = switcher.get(argument, lambda: "Invalid Input")
		func()


	def main(self):
		user_input = 1
		
		while user_input:
			print("\n\n-- TEST MENU--\n")
			print("0 -- Exit")
			print("1 -- See Player's Details")
			print("2 -- See All Items' Details")
			print("3 -- See All Rooms' Details")
			print("4 -- Test Taking Item")
			print("5 -- Test Entering All Rooms")
			print("6 -- Test Entering Player's Current Room")
			print("7 -- Test Dropping Item")
			print("8 -- Test Player Moving")

			user_input = int(input("\nEnter the corresponding number for the test you would like to run: "))
			if user_input and user_input <= 8:
				self.numToTest(user_input)

