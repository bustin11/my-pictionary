from round import Round
from screen import Screen
import random 
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logging.root.name = "Game"

logging.root.setLevel(logging.WARNING)

class Game(object):
  MIN_NUM_PLAYERS = 2
  def __init__(self, players, game_id):
    self.round_number = 0
    self.players = players
    self.current_round = None
    self.drawing_player_id = -1
    self.used_words = set()
    self.screen = Screen()
    self.game_id = game_id
    self.game_over = False
    self.begin_round()

  def begin_round(self):
    self.round_number += 1
    self.drawing_player_id += 1
    random_word = self.generate_random_word_from_file('words.txt')
    self.screen.clear_screen()  
    self.current_round = Round(random_word.lower(), self.round_number, self.players[self.drawing_player_id], self)

  def generate_random_word_from_file(self, file_path):
    words_list = []
    with open(file_path, 'r') as f:
      for line in f:
        word = line.strip()
        if word not in self.used_words:
          words_list.append(word)
    
    return random.choice(words_list)

  def round_has_ended(self):
    return self.current_round.round_has_ended
        
  def make_player_guess(self, player, guess):
    if self.current_round.make_player_guess(player, guess):
        
      # self.end_round()
      # if (self.round_number == len(self.players)):
      #   self.end_game()
      # self.begin_round()
      return True
    return False 

  def player_disconnected(self, player):
    self.current_round.player_disconnected(player)
    self.players.remove(player)
    self.current_round.chat_box.add_message(f"{player.name} has left the game")

    if (len(self.players) < self.MIN_NUM_PLAYERS):
      self.current_round.chat_box.add_message("< f{self.MIN_NUM_PLAYERS} players are remaining -- ending game")
      self.end_game()

  def end_game(self):
    logging.info(f"Game {self.game_id} has ended") # server side 
    for player in self.players:
      player.game = None 
  
  def update_screen(self, x, y, color):
    self.screen.update_screen(x, y, color)

  def get_scores(self):
    return self.current_round.get_scores()

  def end_game(self):
    if not self.game_over:
      self.current_round.chat_box.add_message("Game Has Ended!")
      self.game_over = True
