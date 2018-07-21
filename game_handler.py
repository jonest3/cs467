import pickle
import os
from gameEngine import Item, Player

def createDirectory(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print('Error: Creating directory: ' + directory)
		

def saveObj(obj, filename):
	try:
		createDirectory("./saved_objs");
		save_file = "./saved_objs/{filename}.save".format(filename=filename)
		pickle.dump(obj, open(save_file, 'wb'))
	except:
		print("Error: Could not save game.")


def loadObj(obj_file):
	path = "./saved_objs/{filename}.save".format(filename=obj_file)
	if os.path.exists(path):
		try: 
			loadedGame = pickle.load(open(path, 'rb'))
			return loadedGame
		except pickle.UnpicklingError:
			print("Error: Could not load game.");
	else:
		print("Error: {filename} does not exist.".format(filename=obj_file))
		return None

	
#obj = {"player": {"name":"Taylor", "age":26}, "currentRoom": "Helicopter_Pad"}

obj = Item('Taylor', 'She was a small town girl...', 'Bronze');
print("%s" % obj.KeyVal);

saveObj(obj, "item_obj");


saved_obj = loadObj("item_obj") 

if saved_obj is not None:
	print("%s" % saved_obj.KeyVal)
#	print(saved_obj["player"]["name"])

obj = Player('Basement', 12)
print("%s" % obj._Location);
saveObj(obj, "player_obj");
saved_obj = loadObj("player_obj");

if saved_obj is not None:
	print("%s" % saved_obj._Location);
