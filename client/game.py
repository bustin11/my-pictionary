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

      self.players = []
      for name in list(players.values())[0]:
        self.add_player(name)
      self.name = player_name
      self.top_bar.set_max_round(len(self.players))

      self.pallete = Pallete(100, self.screen.dx + self.screen.HEIGHT - 120, 120, 120, copy.deepcopy(self.COLORS), self)

      self.chat_box = ChatBox(self.screen.dx + self.screen.WIDTH + 250, 50,300, self.HEIGHT * 6 / 7)
      self.draw_color = (0,0,0)

    def add_player(self, name):
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
        self.connection.send({Msg.DRAW: [self.INV_COLORS[self.draw_color], int(coord[1]), int(coord[0])]})

    def handle_key(self, event):
      if not self.drawing: # can only guess if not drawing
        if event.key == pygame.K_RETURN:
          self.connection.send({Msg.GUESS, [self.chat_box.typed]})
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
          if event.type == pygame.KEYDOWN:
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

        response = self.connection.send(payload)
        # get word
        self.top_bar.set_word(response[str(Msg.GET_WORD)])

        # send word
        # response = self.connection.send(Msg.GUESS, [self.text]) 

        # get chatbox (will update the the word sent)
        # response = self.connection.send(Msg.GET_CHAT_BOX, [])
        # response = list(response.values())[0]
        # self.chat_box.replace(response)

        # # grab screen
        if str(Msg.GRAB_SCREEN) in response: # optimization
          print('updating the screen')
          self.screen._scrn = response[str(Msg.GRAB_SCREEN)] 
          self.screen.unzip_screen()

        # # get time
        self.top_bar.set_time(response[str(Msg.TIME_LEFT)])

        # # get round
        # response = self.connection.send(Msg.GET_ROUND, [])
        # self.top_bar.set_round(list(response.values())[0])

        # # get players
        # response = self.connection.send(Msg.GET_PLAYERS, [])
        # response = list(response.values())[0]
        # new_players = []
        # for player in self.players:
        #   if player.name in response:
        #     new_players.append(player)
        # self.players = new_players
        # self.leaderboard.players = new_players
        
        # # get score
        # response = self.connection.send(Msg.GET_SCORE, [])
        # response = list(response.values())[0]
        # for player, dx in zip(self.players, response):
        #   player.update_score(dx)

        if self.players[self.round_number-1].name == self.name:
          self.drawing = True

        self.render()

      pygame.quit()


if __name__ == "__main__":
  pygame.font.init()
  g = Game()
  g.run()
