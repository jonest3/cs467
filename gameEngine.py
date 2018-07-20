game_over = True


class Item:

    # initializes the item. name = the name of the item
    # desc = the description of the item provided when the player examines it
    # key_val = the value the item has as a key, passed to an object if this item is used on it
    # lock_val = the value compared with a given key value to see if this item reacts with an item being used on it
    # trans_id = an item that this item becomes after the correct key has been applied to it
    def __init__(self, name, desc, key_val, lock_val=None, trans_id=None):
        self.Name = name
        self.Desc = desc
        self.KeyVal = key_val
        self._LockVal = lock_val
        self._TransID = trans_id

    def get_lock_val(self):
        return self._LockVal

    def get_key_val(self):
        return self.KeyVal

    def get_trans_id(self):
        return self._TransID

    # use some object on this item to see if it does anything. If it does, turn into the relevant item
    # and return 1, if the items do not interact return 0
    def use(self, input):
        key = input.getKeyVal()
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


class Player:

    def __init__(self, location):
        self.Bag = []
        self._Location = location

    def take(self, item):
        for thing in self._Location.Floor:
            if thing.Name is item:
                self.Bag.append(thing)
                self._Location.Floor.remove(thing)
                print("You pick up the " + item + "and put it in your bag")
                return 1
        for shelf in self._Location.Shelves:
            for thing in shelf.Contents:
                if thing.Name is item:
                    self.Bag.append(thing)
                    self._Location.Floor.remove(thing)
                    print("You pick up the " + item + "and put it in your bag")
                    return 1
        print("There is no " + item + " here.")
        return 0

    def use(self, item, target):
        lock = None
        key = None
        for thing in self.Bag:
            if thing.Name is item:
                key = thing
            elif thing.Name is target:
                lock = thing
        for thing in self._Location.Doors:
            if thing.Name is target:
                lock = thing
        for thing in self._Location.Traps:
            if thing.Name is target:
                lock = thing
        for thing in self._Location.Shelves:
            if thing.Name is target:
                lock = thing
        if lock and key:
            lock.use(key)
        if not key:
            print("You do not have a " + item)
        elif not lock:
            print("There is no " + target + " to use your " + item + " on.")

    def look(self, target):
        for thing in self.Bag:
            if thing.Name is target:
                print(thing.Desc)
                return 1
        for thing in self._Location.Floor:
            if thing.Name is target:
                print(thing.Desc)
                return 1
        for thing in self._Location.Shelves:
            if thing.Name is target:
                print(thing.Desc)
                return 1
        for thing in self._Location.Traps:
            if thing.Name is target:
                print(thing.Desc)
                return 1
        for thing in self._Location.Doors:
            if thing.Name is target:
                print(thing.Desc)
                return 1
        print("There is no " + target + " here.")
        return 0

    def look_around(self):
        self._Location.look_around()

    def drop(self, item):
        for thing in self.Bag:
            if thing.Name is item:
                print("You drop your " + item + " on the floor")
                self._Location.additem(thing)
                self.Bag.remove(thing)
                return 1
        print("You do not have a " + item)
        return 0

    def move(self, room):
        global game_over
        for thing in self._Location.Neighbors:
            if thing.Name is room:
                for trap in self._Location.Traps:
                    if trap.Locked is True:
                        trap.spring()
                        if trap.Lethal is True:
                            game_over = True
                        else:
                            self._Location = trap.Destination
                        return 2
                thing.enter()
                self._Location = thing
                return 1
        print("You do not see a " + room + " to go to.")
        return 0


class Room:

    def __init__(self, name, desc):
        self.Name = name
        self.Desc = desc
        self.Floor = []
        self.Doors = []
        self.Shelves = []
        self.Traps = []
        self.Neighbors = []
        self.Visited = False

    def get_name(self):
        return self.Name

    def get_desc(self):
        return self.Desc

    def look_around(self):
        print(self.Desc + " through nearby doorways, you see: ")
        for room in self.Neighbors:
            print(room.Name)
        if len(self.Doors) > 0:
            for door in self.Doors:
                print("There is a " + door.Name + " here.")
        if len(self.Shelves) > 0:
            for shelf in self.Shelves:
                print("There is a " + shelf.Name + " here.")
        if len(self.Traps) > 0:
            for trap in self.Traps:
                print("There is a " + trap.Name + " here.")
        if len(self.Floor) > 0:
            print("There are a few items scattered about: ")
            for item in self.Floor:
                print(item.name)

    def enter(self):
        print("You enter the " + self.Name)
        if not self.Visited:
            self.look_around()
            self.Visited = True


class Door:
    # init door with name, description, value it expects to unlock, and the room it adds to the neighbor list when
    # unlocked
    def __init__(self, name, location, desc, lock_val, neighbor):
        self.Name = name
        self.Location = location
        self.Desc = desc
        self._LockVal = lock_val
        self.neighbor = neighbor
        self.Locked = True

    def get_lock_val(self):
        return self._LockVal

    def use(self, key):
        if self.Locked:
            if key == self._LockVal:
                print("Success! The door opens, and you can see that it leads to " + self.neighbor.Name)
                self.Location.add_neighbor(self.neighbor)
                self.Locked = False
                return 1
            else:
                return 0
        else:
            print("That's already unlocked. It leads to " + self.neighbor.Name)


class Shelf:
    def __init__(self, name, desc, locked, location, lock_val=None):
        self.Name = name
        self.Contents = []
        self.Desc = desc
        self._LockVal = lock_val
        self.Locked = locked
        self.Location = location

    def get_lock_val(self):
        return self._LockVal

    def use(self, key):
        if self.Locked and key is self._LockVal:
            self.Locked = False

    def search(self):
        if self.Locked:
            return 0
        else:
            print("The " + self.Name + " contains:")
            for item in self.Contents:
                print(item.get_name())


class Trap:
    def __init__(self, name, desc, s_desc, lock_val, destination, lethal):
        self.Name = name
        self.Desc = desc
        self.Spring_desc = s_desc
        self._LockVal = lock_val
        self.Destination = destination
        self.Locked = True
        self.Lethal = lethal

    def get_lock_val(self):
        return self._LockVal

    def spring(self):
        print(self.Spring_desc)

    def use(self, input):
        key = input.getKeyVal()
        if self.Locked and key is self._LockVal:
            output = "It works! The " + input.get_name() + " disarms the " + self.Name + \
                     ", it should be safe to pass now"
            print(output)
            self.Locked = False


def game():
    if __name__ == '__main__':
        tr = Room("Test Room", "a very boring white room")
        tp = Player(tr)
        i1 = Item("test1", "the 1st test object", "red")
        i2 = Item("test2", "The 2nd test object", "blue")
        i3 = Item("test3", "The 3rd test object", "green")
        tp.Bag.append(i1)
        tp.Bag.append(i2)
        tp.Bag.append(i3)
        tp.look("test2")


if __name__ == '__main__':
    game()
