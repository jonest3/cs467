
'''
Class to parse and interpret input from command line
When taking input, first argument is always an action
(use, go, take, etc.). This should match a function call
via dicitionary. The remaining input will be interpreted
by the function logic.

'''

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
                game_cont = self.badInput()

    def parse(self, action):

        valid_commands = {


            # Player.use(item) verbs
            "USE": self.use,
            "CONSUME": self.use,

            # Player.take(item) verbs
            "TAKE": self.take,
            "STEAL": self.take,
            "OBTAIN": self.take,

            # Player.look(item) and Player.look_arount() verbs
            "LOOK": self.look,
            "EXAMINE": self.look,

            # Player.drop(item) verbs
            "DROP": self.drop,

            # Player.move(item) verbs
            "GO": self.move,
            "MOVE": self.move,

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
        target =  " ".join(args[1:])
        self.game.player.use(target)
        return 1

    def move(self, args):
        if args[1] == 'to':
            target = " ".join(args[2:])
            self.game.player.move(target)
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
        print("Bad input")
        return 1
