class TestGame:
	def __init__(self, game):
		self.game = game

	def playerDetails(self):
		player = self.game.player
		if player:
			print("\n-- Player Details --\n")
			print("Current Location: {location}".format(location=player._Location.Name))
			print("Turns Remaining: {turns}".format(turns=player.Turns_Remaining))
			print("Bag Contents:")
			for item in player.Bag:
				print(item.Name)			



	def printItemDetails(self, item_key):
		item = self.game.items[item_key]
		print("---------")
		print("Item: {name}".format(name=item.Name))
		print("Desc: {desc}".format(desc=item.Desc))
		print("KeyVal: {key}".format(key=item.KeyVal))
		item.examine()


	def itemsDetails(self):
		print("\n-- Item Details --\n")
		items = list(self.game.items)
		for item in items:
			self.printItemDetails(item)


	def printRoomDetails(self, room):
		if isinstance(room, str):
			room = self.game.rooms[room]

		print("--------")
		print("Room: {name}".format(name=room.Name))
		print("Long Desc: {lDesc}".format(lDesc=room.Desc))
		print("\nShort Desc:  {sDesc}".format(sDesc=room.ShortDesc))
		print("\nFloor Items:")
		floor = room.Floor
		for item in floor:
			self.printItemDetails(item.KeyVal)
		print("\nShelf Items:")
		shelves = room.Shelves
		for shelf in shelves:
			for item in shelf.Contents:
				self.printItemDetails(item.KeyVal)
		print("\nVisited: {visited}".format(visited=room.Visited))
		room.examine()
		print("--------")


	def roomsDetails(self):
		print("\n-- Room Details --\n")
		rooms = list(self.game.rooms)
		for room in rooms:
			self.printRoomDetails(room)


	def testEnteringAllRooms(self):
		print("\n-- Testing Entering All Rooms --\n")
		rooms = list(self.game.rooms)
		for room in rooms:
			roomObj = self.game.rooms[room]
			self.game.player._Location = roomObj
			self.testRoomEnter()


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
		for door in room.Doors:
			door.examine()
			print(door.Direction)
		move_to = input("\n\nEnter where to move to: ")
		self.game.player.move(move_to)

	def testPlayerUse(self):
		self.playerDetails()
		item = input("\n\nItem to use: ")
		target = input("Target to use on: ")

		self.game.player.use(item, target)

	
	def testPlayerLook(self):
		room = self.game.player._Location
		self.printRoomDetails(room)
		target = input("\n\nTarget to look at: ")
		self.game.player.look(target)

	def testPlayerLookAround(self):
		self.game.player.look_around()


	def numToTest(self, argument):
		switcher = {
			1: self.playerDetails,
			2: self.itemsDetails,
			3: self.roomsDetails,
			4: self.testEnteringAllRooms,
			5: self.testRoomEnter,
			6: self.testPlayerTake,
			7: self.testPlayerDrop,
			8: self.testPlayerMove,
			9: self.testPlayerUse,
			10: self.testPlayerLook,
			11: self.testPlayerLookAround
		}
		func = switcher.get(argument, lambda: "Invalid Input")
		func()


	def main(self):
		user_input = 1
		
		while user_input:
			print("\n\n-- TEST MENU--\n")
			print(" 0 -- Exit")
			print(" 1 -- See Player's Details")
			print(" 2 -- See All Items' Details")
			print(" 3 -- See All Rooms' Details")
			print(" 4 -- Test Entering All Rooms")
			print(" 5 -- Test Entering Player's Current Room")
			print(" 6 -- Test Player.take")
			print(" 7 -- Test Player.drop")
			print(" 8 -- Test Player.move")
			print(" 9 -- Test Player.use")
			print("10 -- Test Player.look")
			print("11 -- Test Player.look_around")

			user_input = int(input("\nEnter the corresponding number for the test you would like to run: "))
			if user_input and user_input <= 11:
				self.numToTest(user_input)
		return user_input
