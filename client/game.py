import pygame
from button import Button, TextButton
from top_bar import TopBar
from leaderboard import Leaderboard
from screen import Screen
from player import Player
from pallete import Pallete
from chat_box import ChatBox
from msg import Msg
import copy
'''
TODO: fix the clearing function

'''

class Game:
    BG = (0,	115,	207)
    COLORS = {
      0: (200, 200, 200), # screen background
      1: (255, 0, 0), # Red
      2: (0, 255, 0), # Green
      3: (0, 0, 255), # Blue
      4: (255, 255, 0), # Yellow
      5: (255, 255, 255),# White
      6: (0, 0, 0), # Black
      7: (128, 0, 128), # Purple
      8: (255, 165, 0), # Orange
      9: (0, 128, 0) # Dark Green
    }
    INV_COLORS = { # generated from chatgpt
      (200, 200, 200) : 0, # screen background
      (255, 0, 0): 1, # Red
      (0, 255, 0): 2, # Green
      (0, 0, 255): 3, # Blue
      (255, 255, 0): 4, # Yellow
      (255, 255, 255): 5,# White
      (0, 0, 0): 6, # Black
      (128, 0, 128): 7, # Purple
      (255, 165, 0): 8, # Orange
      (0, 128, 0): 9 # Dark Green
    }
    HEIGHT = 720
    WIDTH = 1280

    def __init__(self, player_name, players, connection=None):

      self.connection = connection

      self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
      self.window.fill(self.BG)

      self.leaderboard = Leaderboard(50,50)

      self.screen = Screen(self.HEIGHT/5,self.WIDTH/4, self.COLORS)

      self.top_bar = TopBar(10, self.WIDTH/4,self.screen.WIDTH, self.HEIGHT/10)
      self.top_bar.set_round(1)
      self.round_number = 1

      self.draw_color = (0,0,0)
      self.drawing = False
      self.game_ended = False

      self.players = []
      for name in players:
        self.add_player(name)
      self.name = player_name
      self.top_bar.set_max_round(len(self.players))

      self.pallete = Pallete(100, self.screen.dx + self.screen.HEIGHT - 120, 120, 120, copy.deepcopy(self.COLORS), self)

      self.chat_box = ChatBox(self.screen.dx + self.screen.WIDTH + 250, 50,300, self.HEIGHT * 6 / 7)
      self.draw_color = (0,0,0)

    def add_player(self, name):
      print(name)
      print("adding player {name}".format(name=name))
      self.players.append(Player(name))
      self.leaderboard.add_player(Player(name))
    
    def render(self):
      self.window.fill(self.BG)
      self.leaderboard.render(self.window)
      self.top_bar.render(self.window)
      self.screen.render(self.window)
      if self.drawing:
        self.pallete.render(self.window)
      self.chat_box.render(self.window)
      pygame.display.update()

    def handle_button(self):
      # changing color
      self.pallete.handle_click()

    def handle_drawing(self):
      # handle drawing
      mouse = pygame.mouse.get_pos()
      coord = self.screen.translate(mouse)
      if coord and self.drawing:
        self.screen.update_screen(*coord, self.draw_color)
        if self.connection and not self.game_ended:
          self.connection.send({Msg.DRAW: [self.INV_COLORS[self.draw_color], int(coord[1]), int(coord[0])]})

    def handle_key(self, event):
      if not self.drawing or True: # can only guess if not drawing
        if event.key == pygame.K_RETURN:
          if self.connection and not self.game_ended:
            self.connection.send({Msg.GUESS : [self.chat_box.typed]})
          self.chat_box.typed = ""
        else:
          # gets the key name
          key_name = pygame.key.name(event.key)

          # converts to uppercase the key name
          key_name = key_name.lower()
          self.chat_box.type(key_name)

    def run(self):
      run = True
      clock = pygame.time.Clock()
      while run:
        clock.tick(60) # 60 fps
          
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
            break 
          if event.type == pygame.MOUSEBUTTONDOWN: # one time click
            self.handle_button()
            self.handle_drawing()
          if event.type == pygame.KEYDOWN and not self.drawing:
            self.handle_key(event)
          if pygame.mouse.get_pressed()[0]: # can support dragging
            self.handle_drawing()

        payload = {}
        payload[Msg.GET_WORD] = []
        payload[Msg.GET_CHAT_BOX] = []
        payload[Msg.GRAB_SCREEN] = []
        payload[Msg.TIME_LEFT] = []
        payload[Msg.GET_ROUND] = []
        payload[Msg.GET_PLAYERS] = []
        payload[Msg.GET_SCORE] = []

        response = {}
        if self.connection and not self.game_ended:
          response = self.connection.send(payload) # need a game over tag to check, since this is blocking

        # get round number
          
        # get word
        if str(Msg.GET_WORD) in response: # optimization
          self.top_bar.set_word(response[str(Msg.GET_WORD)], hidden=not self.drawing and not self.game_ended)

        # get chatbox (will update the the word sent)
        if str(Msg.GET_CHAT_BOX) in response:
          self.chat_box.replace(response[str(Msg.GET_CHAT_BOX)])

        # grab screen
        if str(Msg.GRAB_SCREEN) in response: # optimization
          self.screen._scrn = response[str(Msg.GRAB_SCREEN)] 
          self.screen.unzip_screen()

        # get time
        if str(Msg.TIME_LEFT) in response: # optimization
          self.top_bar.set_time(response[str(Msg.TIME_LEFT)])

        # get round
        if str(Msg.GET_ROUND) in response: # optimization
          self.round_number = response[str(Msg.GET_ROUND)]
          self.top_bar.set_round(self.round_number)

        # get players
        if str(Msg.GET_PLAYERS) in response: # optimization
          new_players = []
          for player in self.players:
            if player.name in response[str(Msg.GET_PLAYERS)]:
              new_players.append(player)
          self.players = new_players
          self.leaderboard.players = new_players
        
        # get score
        if str(Msg.GET_SCORE) in response: # optimization
          for player, x in zip(self.players, response[str(Msg.GET_SCORE)]):
            player.update_score(x)

        if self.players[self.round_number-1].name == self.name:
          self.drawing = True
        else:
          self.drawing = False

        self.render()

        if str(-2) in response:
          self.game_ended = True

      pygame.quit()


if __name__ == "__main__":
  pygame.font.init()
  g = Game('Bustin', ['Bustin'])
  g.run()
