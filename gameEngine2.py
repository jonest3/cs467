class Item:

    # initializes the item. name = the name of the item
    # desc = the description of the item provided when the player examines it
    # key_val = the value the item has as a key, passed to an object if this item is used on it
    # lock_val = the value compared with a given key value to see if this item reacts with an item being used on it
    # trans_id = an item that this item becomes after the correct key has been applied to it
    def __init__(self, name, desc, key_val, lock_val=None, trans_id=None, destination=None, trap_desc=None):
        self.Name = name
        self.Desc = desc
        self.KeyVal = key_val
        self._LockVal = lock_val
        self._TransID = trans_id
        self.Destination = destination
        self.Trap_Desc = trap_desc

    def get_lock_val(self):
        return self._LockVal

    def get_trans_id(self):
        return self._TransID

    def examine(self):
        print(self.Desc)

    # use some object on this item to see if it does anything. If it does, turn into the relevant item
    # and return 1, if the items do not interact return 0
    def use(self, input):
        key = input.KeyVal
        if self._LockVal is not None and key == self._LockVal:
            output = "It works! The " + input.get_name() + " and the " + self.Name + " become a " \
                     + self._TransID.getName()
            print(output)
            self.Name = self._TransID.getName()
            self.Desc = self._TransID.getDesc()
            self.KeyVal = self._TransID.getKeyVal()
            self._LockVal = self._TransID.getTransKey()
            self._TransID = self._TransID.getTransID()
            return 1
        else:
            return 0


# represents the player character and the actions they take
class Player:

    # Initializes with a Room variable indicating the Room the player starts the game in, an integer indicating how
    # many actions the player has before time runs out, and a Bag list indicating the items what
    # the player has in their inventory
    def __init__(self, location, time):
        self.Bag = []
        self._Location = location
        self.Turns_Remaining = time
        self.Last_Loc = None

    def add_item(self, item):
        self.Bag.append(item)

    # takes the name of an item the player wishes to pick up, and searches everywhere the player has access to for an
    # Item with a matching name. If found, adds the Item to the player's Bag construct
    def take(self, item):
        for thing in self._Location.Floor:
            if thing.Name == item:
                self.Bag.append(thing)
                self._Location.Floor.remove(thing)
                print("You pick up the " + item + "and put it in your bag")
                return 1
        for shelf in self._Location.Shelves:
            if not shelf.Locked:
                for thing in shelf.Contents:
                        if thing.Name == item:
                            self.Bag.append(thing)
                            self._Location.Floor.remove(thing)
                            print("You pick up the " + item + "and put it in your bag")
                            if thing.destination is not None:
                                print(thing.Trap_Desc)
                                self._Location = thing.Destination
                            return 1
        print("There is no " + item + " here.")
        return 0

    # represents the player using an item from their inventory on another object (combining it with another item in
    # their inventory, using it to unlock a door, or shelf, or disarm a trap). Takes as argument the Name of the Item
    # the player wishes to use as item and the Name of the object they wish to use it on as target
    def use(self, item, target):
        lock = None
        key = None
        for thing in self.Bag:
            if thing.Name == item:
                key = thing
            elif thing.Name == target:
                lock = thing
        for thing in self._Location.Doors:
            if thing.Name == target:
                lock = thing
        for thing in self._Location.Traps:
            if thing.Name == target:
                lock = thing
        for thing in self._Location.Shelves:
            if thing.Name == target:
                lock = thing
        if lock and key:
            if lock.use(key) == 1:
                self.Bag.remove(key)
        if not key:
            print("You do not have a " + item)
        elif not lock:
            print("There is no " + target + " to use your " + item + " on.")

    # takes as argument the name of an object the player wishes to examine more closely. If the object is found, prints
    # the description of that object
    def look(self, target):
        if self._Location.Name == target:
            self._Location.examine()
            return 1
        for thing in self.Bag:
            if thing.Name == target:
                thing.examine()
                return 1
        for thing in self._Location.Floor:
            if thing.Name == target:
                thing.examine()
                return 1
        for thing in self._Location.Shelves:
            if thing.Name == target:
                thing.examine()
                return 1
        for thing in self._Location.Traps:
            if thing.Name == target:
                thing.examine()
                return 1
        for thing in self._Location.Doors:
            if thing.Name == target:
                thing.examine()
                return 1
        print("There is no " + target + " here.")
        return 0

    # gives the player the more detailed text they receive upon first entering a room
    def look_around(self):
        self._Location.look_around()

    # takes as argument the name of an Item the player wishes to remove from their bag
    def drop(self, item):
        for thing in self.Bag:
            if thing.Name == item:
                print("You drop your " + item + " on the floor")
                self._Location.add_item(thing)
                self.Bag.remove(thing)
                return 1
        print("You do not have a " + item)
        return 0

    # takes as argument the name of a room the player wishes to move to, and attempts to move there (if it can be found
    # and there are no traps preventing it)
    def move(self, room):
<<<<<<< HEAD
        for thing in self._Location.Neighbors:
            if thing.Name == room:
                for trap in self._Location.Traps:
                    if trap.Locked is True:
                        trap.spring()
                        if trap.Destination:
                            self._Location = trap.Destination
                        else:
                            self.Turns_Left = 0
                        return 2
                thing.enter()
                self._Location = thing
                return 1
        print("You do not see a " + room + " to go to.")
=======
        for door in self._Location.Doors:
            if not door.Locked:
                if door.Destination.Name == room or door.Direction == room or door.Name == room:
                    if door.Destination == self.Last_Loc:
                        door.Destination.enter()
                        self.Last_Loc = self._Location
                        self._Location = door.Destination
                        return 1
                    for trap in self._Location.Traps:
                        if trap.Locked is True:
                            trap.spring()
                            if trap.Destination:
                                self._Location = trap.Destination
                            else:
                                self.Turns_Remaining = 0
                            return 2
                    door.Destination.enter()
                    self.Last_Loc = self._Location
                    self._Location = door.Destination
                    return 1
        print("You cannot get to " + room + " from here.")
>>>>>>> origin/GameEngine
        return 0


class Room:
    # Represents the discrete spaces found within the dungeon. Initializes with a name and a description, as well as
    # empty lists to contain the Items, Doors, Shelves, Traps, and other Rooms that can be accessed from this room
<<<<<<< HEAD
    def __init__(self, name, long_desc, short_desc):
        self.Name = name
        self.LongDesc = long_desc
=======
    def __init__(self, name, desc, short_desc):
        self.Name = name
        self.Desc = desc
>>>>>>> origin/GameEngine
        self.ShortDesc = short_desc
        self.Floor = []
        self.Doors = []
        self.Shelves = []
        self.Traps = []
        self.Visited = False

    def add_item(self, item):
        self.Floor.append(item)

    def add_door(self, door):
        self.Doors.append(door)

    def add_shelf(self, shelf):
        self.Shelves.append(shelf)

    def add_trap(self, trap):
        self.Traps.append(trap)

    def examine(self):
        if self.Visited:
<<<<<<< HEAD
                print(self.ShortDesc)
        else:
                print(self.LongDesc)
        print("Through nearby doorways, you can see: ")
        for room in self.Neighbors:
            print(room.Name)
        if len(self.Doors) > 0:
            for door in self.Doors:
                print("There is a " + door.Name + " here.")
=======
            print(self.Desc)
        else:
            print(self.ShortDesc)
        for door in self.Doors:
            door.examine()
>>>>>>> origin/GameEngine
        if len(self.Shelves) > 0:
            for shelf in self.Shelves:
                print("There is a " + shelf.Name + " here.")
        if len(self.Traps) > 0:
            for trap in self.Traps:
                print("There is a " + trap.Name + " here.")
        if len(self.Floor) > 0:
            print("There are a few items scattered about: ")
            for item in self.Floor:
                print(item.Name)

    def enter(self):
<<<<<<< HEAD
        print("You enter the " + self.Name)
        self.examine()
=======
        print("You enter ")
>>>>>>> origin/GameEngine
        if not self.Visited:
            self.Visited = True
        else:
            self.examine()


class Door:
    # init door with name, description, key value that will unlock it
    def __init__(self, name, desc, direction, destination, locked=False, lock_val=None, unlock_desc=None):
        self.Name = name
        self.Desc = desc
        self.UnlockDesc = unlock_desc
        self.Direction = direction
        self._LockVal = lock_val
        self.neighbor = destination
        self.Locked = locked

    def get_lock_val(self):
        return self._LockVal

    def examine(self):
            print(self.Desc + " lies to the " + self.Direction)

    # takes an Item as input, if the door is locked it compares the key value of the item passed against the key it
    # expects. If they match, it adds the room it stores (leads to) to the list of Rooms accessible from the room set as
    # the Door's location. (notably, location need not be the room where the player finds a door, and a door could be
    # implemented that doesn't change the room the player is in, but they must search to see what they have unlocked.)
    def use(self, input):
        key = input.KeyVal
        if self.Locked:
            if key == self._LockVal:
                self.Locked = False
                self.Desc = self.UnlockDesc
                print("Success! The passage opens to reveal: ")
                self.examine()
                return 1
            else:
                return 0
        else:
            print("That's already open.")
            return 0


class Shelf:
    # represents objects found in rooms that contain Items. Initializes with the name of the Shelf, a description,
    # weather or not the Shelf needs to be unlocked before the items in it can be accessed, and, if it does need to be
    # unlocked, what key value it is expecting to unlock it
    def __init__(self, name, desc, locked, lock_val=None):
        if locked and not lock_val:
            print("ERROR: locked status=True and lock_val=None, a locked door must have a key")
        self.Name = name
        self.Contents = []
        self.Desc = desc
        self._LockVal = lock_val
        self.Locked = locked

    def get_lock_val(self):
        return self._LockVal

    def use(self, input):
        key = input.KeyVal
        if self.Locked and key == self._LockVal:
            print("Success! The " + key.Name + " opens the " + self.Name)
            self.Locked = False
            self.examine()
            return 1
        else:
            print("That doesn't seem to do anything.")
            return 0

    def examine(self):
        if self.Locked:
            print(self.Desc)
            print("It seems like there may something in this, but you can't seem to get inside it.")
            return 0
        else:
            print("The " + self.Name + " contains:")
            for item in self.Contents:
                print(item.get_name())
            return 1


class Trap:
    # a trap that can spring when the player moves through the room it's in, killing them or sending them to a different
    # room. Initializes with a name, description, description of what happens to the player when the trap is sprung,
    # key value expected to disarm the trap, and the room the player is sent to when the trap is sprung.
    # if no destination is given, the trap simply kills the player.
    def __init__(self, name, desc, s_desc, lock_val, destination=None):
        self.Name = name
        self.Desc = desc
        self.Spring_desc = s_desc
        self._LockVal = lock_val
        self.Destination = destination
        self.Locked = True

    def get_lock_val(self):
        return self._LockVal

    def examine(self):
        print(self.Desc)
        if not self.Locked:
            print("It appears to be disarmed and safe to pass")

    def spring(self):
        print(self.Spring_desc)

    def use(self, input):
        key = input.getKeyVal()
        if self.Locked:
            if key == self._LockVal:
                output = "It works! The " + input.get_name() + " disarms the " + self.Name + \
                         ", it should be safe to pass now"
                print(output)
                self.Locked = False
                return 1
            else:
                print("That doesn't seem to do anything")
                return 0
        else:
            print("This trap is already disarmed.")
            return 0
