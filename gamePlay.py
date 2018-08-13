from gameSetup import GameComponents
from input_parsing import inputParser
from gameHandler import GameHandler


game_components = GameComponents()
game_handler = GameHandler()
input_parser = inputParser(game_components, game_handler)
input_parser.run()
