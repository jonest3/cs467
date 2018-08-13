class Item:

    # initializes the item. name = the name of the item
    # desc = the description of the item provided when the player examines it
    # key_val = the value the item has as a key, passed to an object if this item is used on it
    # lock_val = the value compared with a given key value to see if this item reacts with an item being used on it
    # trans_id = an item that this item becomes after the correct key has been applied to it
    def __init__(self, name, desc, key_val, lock_val=None, trans_id=None, trap_desc=None, destination=None):
        self.Name = name
        self.Desc = desc
        self.KeyVal = key_val
        self._LockVal = lock_val
        self._TransID = trans_id
        self.Trap_Desc = trap_desc
        self.Destination = destination

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
            output = "It works! The " + input.Name + " and the " + self.Name + " become a " \
                     + self._TransID.Name
            print(output)
            self.Name = self._TransID.Name
            self.Desc = self._TransID.Desc
            self.KeyVal = self._TransID.KeyVal
            self._LockVal = self._TransID.get_lock_val()
            self._TransID = self._TransID.get_trans_id()
            self.Trap_Desc = self._TransID.Trap_Desc
            self.Destination = self._TransID.Destination
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
                print("You pick up the " + item + " and put it in your bag")
                return 1
        for shelf in self._Location.Shelves:
            if not shelf.Locked:
                for thing in shelf.Contents:
                        if thing.Name == item:
                            self.Bag.append(thing)
                            shelf.Contents.remove(thing)
                            print("You pick up the " + item + " and put it in your bag")
                            if thing.Trap_Desc is not None:
                                print(thing.Trap_Desc)
                                try:
                                    if thing.destination: # is not None:
                                        self.Turns_Remaining = 12
                                        self.move(thing.Destination)
                                except:
                                    self.Turns_Remaining = 0
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
            else:
                print("You cannot use " + key.Name + " on " + lock.Name +".")
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
        print("\n")
        print(self._Location.Desc)

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
    def move(self, user_input):
        for door in self._Location.Doors:
#            if not door.Locked:
            if door.Destination.Name == user_input or door.Direction == user_input or door.Name == user_input:
                if door.Locked:
                    print("{name} seems to be locked.  You will need to find a key to get through this way.".format(name=door.Name))
                else:
                    for trap in self._Location.Traps:
                        if trap.Locked is True:
                            trap.spring()
                            if trap.Destination:
                                self._Location = trap.Destination
                                self.Turns_Remaining = 12
                            else:
                                self.Turns_Remaining = 0
                            return 2
                    self.Last_Loc = self._Location
                    self._Location = door.Destination
                    self._Location.enter()
                    return 1

        print("You cannot get to {room} from here".format(room=user_input))
        return 0


class Room:
    # Represents the discrete spaces found within the dungeon. Initializes with a name and a description, as well as
    # empty lists to contain the Items, Doors, Shelves, Traps, and other Rooms that can be accessed from this room
    def __init__(self, name, desc, short_desc):
        self.Name = name
        self.Desc = desc
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
            print(self.ShortDesc)
        else:
            print(self.Desc)
        for door in self.Doors:
            door.examine()
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
        print("You enter ")
        self.examine()
        if not self.Visited:
            self.Visited = True


class Door:
    # init door with name, description, key value that will unlock it
    def __init__(self, name, desc, direction, destination, locked=False, lock_val=None, unlock_desc=None):
        self.Name = name
        self.Desc = desc
        self.UnlockDesc = unlock_desc
        self.Direction = direction
        self._LockVal = lock_val
        self.Destination = destination
        self.Locked = locked

    def get_lock_val(self):
        return self._LockVal

    def examine(self):
            print(self.Desc)
            print("The " + self.Destination.Name + " lies " + self.Direction + " through the " + self.Name)

    # takes an Item as input, if the door is locked it compares the key value of the item passed against the key it
    # expects. If they match, it adds the room it stores (leads to) to the list of Rooms accessible from the room set as
    # the Door's location. (notably, location need not be the room where the player finds a door, and a door could be
    # implemented that doesn't change the room the player is in, but they must search to see what they have unlocked.)
    def use(self, input):
        if self.Locked:
            key = input.KeyVal
            if key == self._LockVal:
                self.Locked = False
                self.Desc = self.UnlockDesc
                print("Success! The passage opens to reveal: ")
                self.examine()
                return 1
            else:
                print("That doesn't seem to do anything.")
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

    def add_item(self, item):
        self.Contents.append(item)

    def get_lock_val(self):
        return self._LockVal

    def use(self, input):
        key = input.KeyVal
        if self.Locked and key is self._LockVal:
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
                print(item.Name)
            return 1


class Trap:
    # a trap that can spring when the player moves through the room it's in, killing them or sending them to a different
    # room. Initializes with a name, description, description of what happens to the player when the trap is sprung,
    # key value expected to disarm the trap, and the room the player is sent to when the trap is sprung.
    # if no destination is given, the trap simply kills the player.
    def __init__(self, name, desc, s_desc, lock_val, d_desc, destination=None):
        self.Name = name
        self.Desc = desc
        self.Spring_desc = s_desc
        self._LockVal = lock_val
        self.DisarmDesc = d_desc
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
        self.Locked = False

    def use(self, input):
        key = input.getKeyVal()
        if self.Locked:
            if key is self._LockVal:
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
