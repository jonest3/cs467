from enum import Enum
'''
Class to parse and interpret input from command line
When taking input, first argument is always an action
(use, go, take, etc.). This should match a function call
via dicitionary. The remaining input will be interpreted
by the function logic.

'''

class ErrorType(Enum):
    key_error = 1
    value_error = 2
    unknown_error = 3


class inputParser:

    def __init__(self, game):
        self.game = game

    def run(self):
        game_cont = 1
        while game_cont:
            raw_input = input("Input a command: ")
            args = raw_input.split(" ")
            action = self.parse(args[0].upper())
            try:
                game_cont = action(args)
            except KeyError:
                print ("Not sufficient number of arguments.")
            except ValueError as e:
                print (str(e))
            except Exception as e:
                print ("Unkown error occured.")

    def parse(self, action):

        valid_commands = {


            # Player.use(item, target) verbs
            "USE": self.use,
            "EXPEND": self.use,
            "SPEND": self.use,
            "COMBINE": self.use,
            "MIX": self.use,
            "PUT": self.use,


            # Player.take(item) verbs
            "TAKE": self.take,
            "STEAL": self.take,
            "OBTAIN": self.take,

            # Player.look(item) and Player.look_arount() verbs
            "LOOK": self.look,
            "EXAMINE": self.look,

            # Player.drop(item) verbs
            "DROP": self.drop,
            "DUMP": self.drop,
            "ABANDON": self.drop,

            # Player.move(item) verbs
            "GO": self.move,
            "MOVE": self.move,
            "PASS": self.move,
            "TRAVEL": self.move,

            "NORTH": self.move,
            "SOUTH": self.move,
            "EAST": self.move,
            "WEST": self.move,
            "NORHTWEST": self.move,
            "NORTHEAST": self.move,
            "SOUTHWEST": self.move,
            "SOUTHEAST": self.move,

            # GameSetup.saveGame(game) verbs
            "SAVE": self.save,

            # Quit
            "QUIT": self.quit,
        }

        return valid_commands.get(action, self.badInput)

    def look(self, args):
        if args[1] == "around":
            self.game.player.look_around()

        elif args[1] == 'at':
            target = " ".join(args[2:])
            self.game.player.look(target)

        else:
            target = " ".join(args[1:])
            self.game.player.look(target)

        return 1

    def use(self, args):
        pronoun = None
        if 'on' in args:
            pronoun = 'on'
        elif 'with' in args:
            pronoun = 'with'
        else:
            print ("Usage: {verb} [item] on|with [target]".format(verb=args[0]))
            return 1

        index = args.index(pronoun)
        item = " ".join(args[1:index])
        target =  " ".join(args[index+1:])
        self.game.player.use(item, target)
        return 1

    def move(self, args):
        directions = ["NORTH", "SOUTH", "WEST", "EAST",
            "NORTHWEST", "NORTHEAST", "SOUTHWEST", "SOUTHEAST"]

        if args[0].upper() in directions:
            target = args[0]
        elif args[1] == 'to':
            target = " ".join(args[2:])
        else:
            target = " ".join(args[1:])
        self.game.player.move(target)
        return 1

    def take(self, args):
        target = " ".join(args[1:])
        self.game.player.take(target)
        return 1

    def drop(self, args):
        target = " ".join(args[1:])
        self.game.player.drop(target)
        return 1

    def quit(self, args):
        return 0

    def save(self, args):
        self.game.saveGame(self.game)
        return 1

    def badInput(self, args):
        print("'{verb}' not valid command".format(verb=args[0]))
        return 1