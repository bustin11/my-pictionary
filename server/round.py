
import time 
from chat_box import ChatBox
from _thread import start_new_thread


# server round
class Round(object):

  def __init__(self, current_word, round_number, player_drawing, game):
    self.current_word = current_word
    self.round_number = round_number
    self.player_drawing = player_drawing
    self.game = game
    self.round_has_ended = False
    
    self.chat_box = ChatBox()
    self.start_round()
    start_new_thread(self.timer, ())

  def get_scores(self):
    return [score for score in self.player_scores.values()]

  def calculate_score(self):
    return self.time_left

  def make_player_guess(self, player, guess):
    # real time, so immediately return yes or no if it's correct 
    if guess == self.current_word:
      player.update_score(self.calculate_score())
      self.correct_player_guesses.append(player)
      self.chat_box.add_message(f"{self.player_drawing.name} guessed correctly!")
      return True
    else:
      # don't have this to not flood the server
      self.chat_box.add_message(f"{self.player_drawing.name} guessed {guess}")
      return False

  def timer(self):
    while self.time_left > 0:
      time.sleep(1)
      self.time_left -= 1
    self.end_round("Times up!")

  def start_round(self):
    self.time_left = 20 # in seconds
    self.correct_player_guesses = []
    self.player_scores = {player : 0 for player in self.game.players} # collate the playesr scores
    self.chat_box.clear()
    self.chat_box.add_message(f"Round {self.round_number} starting!")
    self.chat_box.add_message(f"{self.player_drawing.name} is drawing")

  def end_round(self, message):
    if message: 
      self.chat_box.add_message(message)
    self.chat_box.add_message(f"The word was {self.current_word}")
    for player in self.correct_player_guesses:
      self.player_scores[player] = player.score # more time left = higher score 
    # make sure to call a round has ended function in the game object 
    self.round_has_ended = True


  def player_disconnected(self, player):

    del self.player_scores[player]
    if player in self.correct_player_guesses:
      self.correct_player_guesses.remove(player)
    
    if player == self.player_drawing:
      self.chat_box.add_message("Player f{self.player_drawing.name} disconnected.")
      self.end_round("Player drawing left")