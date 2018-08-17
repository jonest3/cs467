def highlight(name):
    return ("\033[93m{}\033[00m" .format(name))


def strong_match(input, target):
    # remove case
    target = target.lower()
    input = input.lower()
    if input == target:
        return 1
    return 0


def weak_match(input, target):
    if strong_match(input, target):
        return 1

    # Chcek word match
    target = target.lower().split(' ')
    input = input.lower()
    if input in target:
        return 1
    return 0


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
        self.hasSprung = False

    def get_lock_val(self):
        return self._LockVal

    def get_trans_id(self):
        return self._TransID

    def examine(self):
        print(self.Desc)

    # use some object on this item to see if it does anything. If it does, turn into the relevant item
    # and return 1, if the items do not interact return 0
    def use(self, obj):
        key = obj.KeyVal
        if self._LockVal is not None and key == self._LockVal:
            print("It works! The {objName} and the {sName} become a {transName}.\n".format(objName=highlight(obj.Name), sName=highlight(self.Name), transName=highlight(self._TransID.Name)))
            self.Name = self._TransID.Name
            self.Desc = self._TransID.Desc
            self.KeyVal = self._TransID.KeyVal
            self._LockVal = self._TransID.get_lock_val()
            self.Trap_Desc = None if not self._TransID.Trap_Desc else self._TransID.Trap_Desc
            self.Destination = self._TransID.Destination
            self._TransID = self._TransID.get_trans_id()
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
        foundItem = None
        for thing in self._Location.Floor:
            if strong_match(item, thing.Name):
                foundItem = thing
                self._Location.Floor.remove(thing)
                break
        if foundItem is None:
            for shelf in self._Location.Shelves:
                if not shelf.Locked:
                    for thing in shelf.Contents:
                        if strong_match(item, thing.Name):
                            foundItem = thing
                            shelf.Contents.remove(thing)
        if foundItem is None:
            print("There is no {item} here.\n".format(item=highlight(item)))
        else:
            self.Bag.append(foundItem)
            print("You pick up the {name} and put it in your bag.\n".format(name=highlight(foundItem.Name)))
            if foundItem.Trap_Desc and foundItem.hasSprung == False:
                foundItem.hasSprung = True
                print(foundItem.Trap_Desc)

                if foundItem.Destination:
                    foundItem.Destination.enter()
                    self._Location = foundItem.Destination
                    turns = self.Turns_Remaining - 12
                    if turns < 1:
                        turns = 1
                    return turns
                else:
                    return self.Turns_Remaining
        return 0

    # represents the player using an item from their inventory on another object (combining it with another item in
    # their inventory, using it to unlock a door, or shelf, or disarm a trap). Takes as argument the Name of the Item
    # the player wishes to use as item and the Name of the object they wish to use it on as target
    def use(self, item, target):
        lock = None
        key = None
        for thing in self.Bag:
            if strong_match(item, thing.Name):
                key = thing
            elif strong_match(target, thing.Name):
                lock = thing
        for thing in self._Location.Doors:
            if weak_match(target, thing.Name):
                lock = thing
        for thing in self._Location.Traps:
            if weak_match(target, thing.Name):
                lock = thing
        for thing in self._Location.Shelves:
            if weak_match(target, thing.Name):
                lock = thing
        if lock and key:
            if lock.use(key) == 1:
                self.Bag.remove(key)
                try:
                    if lock.Trap_Desc:
                        print(lock.Trap_Desc)
                        if lock.Destination:
                            lock.Destination.enter()
                            self._Location = lock.Destination
                        else:
                            return self.Turns_Remaining
                except:
                    pass

            else:
                print("You cannot use " + highlight(key.Name) + " on " + highlight(lock.Name) +".\n")

        if not key:
            print("You do not have a {item}.\n".format(item=highlight(item)))
        elif not lock:
            print("There is no " + highlight(target) + " to use your " + highlight(item) + " on.\n")
        return 0

    def inventory(self):
        content = (highlight(item.Name) for item in self.Bag)
        print("You are carrying: {content}.\n".format(content=", ".join(content)))

    # takes as argument the name of an object the player wishes to examine more closely. If the object is found, prints
    # the description of that object
    def look(self, target):
        if weak_match(target, self._Location.Name):
            self._Location.examine()
            return 0
        for thing in self.Bag:
            if strong_match(target, thing.Name):
                thing.examine()
                return 0
        for thing in self._Location.Floor:
            if strong_match(target, thing.Name):
                thing.examine()
                return 0
        for thing in self._Location.Shelves:
            if weak_match(target, thing.Name):
                thing.examine()
                return 0
            elif not thing.Locked:
                for item in thing.Contents:
                    if strong_match(target, item.Name):
                        item.examine()
                        return 0
        for thing in self._Location.Traps:
            if weak_match(target, thing.Name):
                thing.examine()
                return 0
        for thing in self._Location.Doors:
            if weak_match(target, thing.Name):
                thing.examine()
                return 0
        print("There is no " + highlight(target) + " here.\n")
        return 0

    # gives the player the more detailed text they receive upon first entering a room
    def look_around(self):
        self._Location.examine()

    # takes as argument the name of an Item the player wishes to remove from their bag
    def drop(self, item):
        for thing in self.Bag:
            if strong_match(item, thing.Name):
                print("You drop the " + highlight(item) + " on the floor.\n")
                self._Location.add_item(thing)
                self.Bag.remove(thing)
                return 0
        print("You do not have a(n) {item}.\n".format(item=highlight(item)))
        return 0

    # takes as argument the name of a room the player wishes to move to, and attempts to move there (if it can be found
    # and there are no traps preventing it)
    def move(self, user_input):
        for door in self._Location.Doors:
            options = [door.Destination.Name, door.Direction, door.Name]
            if any(weak_match(user_input, target) for target in options):
                if door.Locked:
                    print("You can't seem to get through the {name}.  You will need to find something to help you.\n".format(name=highlight(door.Name)))
                else:
                    for trap in self._Location.Traps:
                        if trap.Locked and self.Last_Loc.Name != door.Destination.Name:
                            trap.spring()
                            if trap.Destination:
                                trap.Destination.enter()
                                self._Location = trap.Destination
                                turns = self.Turns_Remaining - 12
                                if turns < 1:
                                    turns = 1
                                return turns
                            else: 
                                return self.Turns_Remaining
                    self.Last_Loc = self._Location
                    self._Location = door.Destination
                    self._Location.enter()
                    return 1

        print("You cannot get to {room} from here.\n".format(room=highlight(user_input)))
        return 0

    def jump(self):
        bag = [stuff.KeyVal for stuff in self.Bag]
        if self._Location.Name == "Waterfall" and "scepter" in bag:
            trap = self._Location.Traps[0]
            trap.spring()
            self._Location = trap.Destination
            return 1
        print("Why are you so jumpy?\n")
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
            shelves = (highlight(shelf.Name) for shelf in self.Shelves)
            print("You spot a(n) {shelf_list} close by.\n".format(shelf_list=(' and a(n) '.join(shelves))))
        if len(self.Traps) > 0:
            for trap in self.Traps:
                if trap.Locked:
                    if trap.Name == "Dragon":
                        print("You quiver in the shadow of the mighty " + highlight(trap.Name) + ".\n")
                    else:
                        print("You get an un easy feeling while looking at the " + highlight(trap.Name) + ".\n")
        if len(self.Floor) > 0:
            print("There are a few items scattered about the floor: ")
            items = (highlight(item.Name) for item in self.Floor)
            print(', '.join(items)+"\n")

    def enter(self):
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
        print("You see that the {dest} lies {direction} through the {name}.\n".format(dest=highlight(self.Destination.Name), direction=highlight(self.Direction), name=highlight(self.Name)))

    # takes an Item as input, if the door is locked it compares the key value of the item passed against the key it
    # expects. If they match, it adds the room it stores (leads to) to the list of Rooms accessible from the room set as
    # the Door's location. (notably, location need not be the room where the player finds a door, and a door could be
    # implemented that doesn't change the room the player is in, but they must search to see what they have unlocked.)
    def use(self, item):
        if self.Locked:
            key = item.KeyVal
            if key == self._LockVal:
                self.Locked = False
                self.Desc = self.UnlockDesc
#                print("Success! The passage opens to reveal: ")
                self.examine()
                return 1
            else:
                print("That doesn't seem to do anything.\n")
                return 0
        else:
            print("That's already open.\n")
            return 0


class Shelf:
    # represents objects found in rooms that contain Items. Initializes with the name of the Shelf, a description,
    # weather or not the Shelf needs to be unlocked before the items in it can be accessed, and, if it does need to be
    # unlocked, what key value it is expecting to unlock it
    def __init__(self, name, desc, locked, lock_val=None):
        if locked and not lock_val:
            print("ERROR: locked status=True and lock_val=None, a locked door must have a key.")
        self.Name = name
        self.Contents = []
        self.Desc = desc
        self._LockVal = lock_val
        self.Locked = locked

    def add_item(self, item):
        self.Contents.append(item)

    def get_lock_val(self):
        return self._LockVal

    def use(self, item):
        key = item.KeyVal
        if self.Locked and key is self._LockVal:
            print("Success! The {key} opens the {lock}.\n".format(key=highlight(key.Name), lock=highlight(self.Name)))
            self.Locked = False
            return 1
        else:
            print("Hmm... that didn't seem to do anything.")
            return 0

    def examine(self):
        print(self.Desc)
        if self.Locked:
            print("It seems like something might be in this, but you can't seem to get inside it.\n")
            return 0
        elif len(self.Contents) > 0:
            print("The " + highlight(self.Name) + " contains:")
            contents = (highlight(item.Name) for item in self.Contents)
            print(', '.join(contents)+"\n")
            return 1
        else:
            return 0

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
            print("It appears to be disarmed and safe to pass.\n")

    def spring(self):
        print(self.Spring_desc)
        self.Locked = False

    def use(self, item):
        if self.Locked:
            key = item.KeyVal
            if key == self._LockVal:
#                output = "It works! The " + highlight(item.Name) + " disarms the " + highlight(self.Name) + \
#                         ", it should be safe to pass now.\n"
#                print(output)
                print(self.DisarmDesc)
                self.Locked = False
                return 1
            else:
                print("Uh oh, that doesn't seem to do anything.\n")
                return 0
        else:
            print("You don't need to worry about this anymore.  It is safe here now.\n")
            return 0
