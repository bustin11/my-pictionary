from game import Game

# Player on the server 
class Player(object):
  def __init__(self, name):
    self.name = name
    self.score = 0
    self.game = None 

  def attach_game(self, game):
    self.game = game

  def update_score(self, dx):
    self.score += dx 

  def make_guess(self, guess):
    return self.game.player_make_guess(self, guess)

  def is_drawing(self):
    return self.game.players[self.game.drawing_player_id] == self

  