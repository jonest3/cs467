


class inputParser:
    def __init__(self, raw_input):
        args = raw_input.split(" ")
        try:
            self.command = args[0].upper()
            self.direct_object = args[1].upper()
        except IndexError:
            print ("Not enough arguments!")
        #TODO: add indirect object (optional)
        #TODO: skip or read preposition types (from, to, down, etc)

        self.valid_commands = {

            # Inventory verbs
            "USE": self.inventory,
            "CONSUME": self.inventory,
            "SPEND": self.inventory,
            "EXPEND": self.inventory,
            "THROW": self.inventory,
            "GIVE": self.inventory,

            # Travel verbs
            "GO": self.travel,
            "MOVE": self.travel,

            # Observe
            "LOOK": self.observe,
            "EXAMINE": self.observe,

            # Interact
            "TAKE": self.interact,
            "STEAL": self.interact,
            "OBTAIN": self.interact,
            "MAKE": self.interact,

            # Save

            "SAVE": self.save,

            # Quit
            "QUIT": self.quit,
        }

    def observe(self):
        print("observe")

    def inventory(self):
        print("inventory")

    def travel(self):
        print("travel")

    def interact(self):
        print("interact")

    def quit(self):
        print("quit")

    def save(self):
        print("save")

    def badInput(self):
        print ("Bad Input!")

    def run(self):
        self.valid_commands.get(self.command, self.badInput)()


def main():
    command = ''
    while command.upper() != "QUIT":
        command = input("Input a command: ")
        parser = inputParser(command)
        parser.run()



if __name__ == "__main__":
    main()
