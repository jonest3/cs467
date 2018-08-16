import os
'''
Class to parse and interpret input from command line
When taking input, first argument is always an action
(use, go, take, etc.). This should match a function call
via dicitionary. The remaining input will be interpreted
by the function logic.

'''

feedback = {
    "24": "The walls groan and the floor creaks...",
    "18": "You feel the castle shake...",
    "12": "The ground begins to shift...",
    "6": "The walls literally crumble around you...",
    "0": "The castle collapses around you"
}

class inputParser:

    def __init__(self, game, handler):
        self.game = game
        self.handler = handler

    def run(self):
        os.system("clear")
        game_cont = 1
        self.game.player._Location.enter()
        while game_cont and self.game.player.Turns_Remaining > 0:
            if feedback.get(str(self.game.player.Turns_Remaining)):
                print(feedback[str(self.game.player.Turns_Remaining)])
                del feedback[str(self.game.player.Turns_Remaining)]
#            print("You have {turns} turns left.".format(turns=self.game.player.Turns_Remaining))
            raw_input = input("\nInput a command: ")
            args = raw_input.split(" ")
            os.system("clear")
            action = self.parse(args[0].upper())
            try:
                game_cont = action(args)
            except KeyError:
                print ("Not sufficient number of arguments.")
            except ValueError as e:
                self.badInput(args)
            except Exception as e:
                print (str(e))

        if  self.game.player.Turns_Remaining <= 0:
            print("Game Over")

    def parse(self, action):

        valid_commands = {


            # Player.use(item, target) verbs
            "USE": self.use,
            "EXPEND": self.use,
            "SPEND": self.use,
            "COMBINE": self.use,
            "MIX": self.use,
            "PUT": self.use,
            "UNLOCK": self.use,


            # Player.take(item) verbs
            "TAKE": self.take,
            "STEAL": self.take,
            "OBTAIN": self.take,
            "PICK": self.take,

            # Player.look(item), Player.look_around(),  verbs
            "LOOK": self.look,
            "EXAMINE": self.look,
            "READ": self.look,

            # Player.drop(item) verbs
            "DROP": self.drop,
            "DUMP": self.drop,
            "ABANDON": self.drop,

            # Player.move(item) verbs
            "GO": self.move,
            "MOVE": self.move,
            "PASS": self.move,
            "TRAVEL": self.move,

            "UP": self.move,
            "UPSTAIRS": self.move,
            "DOWN": self.move,
            "DOWNSTAIRS": self.move,
            "NORTH": self.move,
            "SOUTH": self.move,
            "EAST": self.move,
            "WEST": self.move,
            "NORHTWEST": self.move,
            "NORTHEAST": self.move,
            "SOUTHWEST": self.move,
            "SOUTHEAST": self.move,

            # Player.jump() verb
            "JUMP": self.jump,

            # GameHandler.saveGame(game) verbs
            "SAVEGAME": self.save,

            # GameHandler.loadGame() verbs
            "LOADGAME": self.load,

            # Quit
            "QUIT": self.quit,
            "EXIT": self.quit
        }

        return valid_commands.get(action, self.badInput)

    def look(self, args):
        if args[1] == 'at' or args[1] == 'in':
            target = " ".join(args[2:])
        else:
            target = " ".join(args[1:])

        if target == 'around':
            self.game.player.look_around()
            return 1

        elif target == 'bag' or target == 'inventory':
            self.game.player.inventory()
            return 1

        self.game.player.Turns_Remaining -= self.game.player.look(target)
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
        self.game.player.Turns_Remaining -= self.game.player.use(item, target)
        return 1

    def move(self, args):
        directions = ["NORTH", "SOUTH", "WEST", "EAST",
            "NORTHWEST", "NORTHEAST", "SOUTHWEST", "SOUTHEAST", "UP", "UPSTAIRS", "DOWN", "DOWNSTAIRS"]

        if args[0].upper() in directions:
            target = args[0]
        elif args[1] == 'to':
            target = " ".join(args[2:])
        else:
            target = " ".join(args[1:])
        self.game.player.Turns_Remaining -= self.game.player.move(target)
        if self.game.player.Turns_Remaining > 0:
            print("You have {turns} turns left.".format(turns=self.game.player    .Turns_Remaining))
        return 1

    def take(self, args):
        if args[1] == 'up':
            target = " ".join(args[2:])
        else:
            target = " ".join(args[1:])

        self.game.player.Turns_Remaining -= self.game.player.take(target)
        return 1

    def drop(self, args):
        target = " ".join(args[1:])
        self.game.player.Turns_Remaining -= self.game.player.drop(target)
        return 1

    def quit(self, args):
        return 0

    def jump(self, args):
        if self.game.player.jump():
            print ("You Escaped! Congratulations!")
            self.game.player.Turns_Remaining = 0
        return 1

    def save(self, args):
        self.handler.saveGame(self.game)
        return 1

    def load(self, args):
        self.game = self.handler.loadGame() or self.game
        return 1

    def badInput(self, args):
        print("'{verb}' not valid command".format(verb=args[0]))
        return 1
