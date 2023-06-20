import pygame
from button import Button, TextButton
from top_bar import TopBar
from leaderboard import Leaderboard
from screen import Screen
from player import Player
from pallete import Pallete
from chat_box import ChatBox


class Game:
    BG = (0,	115,	207)
    COLORS = { # generated from chatgpt
      (255, 0, 0): 0, # Red
      (0, 255, 0): 1, # Green
      (0, 0, 255): 2, # Blue
      (255, 255, 0): 3, # Yellow
      (255, 255, 255): 4,# White
      (0, 0, 0): 5, # Black
      (128, 0, 128): 6, # Purple
      (255, 165, 0): 7, # Orange
      (0, 128, 0): 8 # Dark Green
    }
    HEIGHT = 720
    WIDTH = 1280

    def __init__(self, connection=None):

      self.connection = connection
      self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
      self.window.fill(self.BG)
      self.leaderboard = Leaderboard(50,50)
      self.screen = Screen(self.HEIGHT/5,self.WIDTH/4, self.COLORS)
      self.top_bar = TopBar(10, self.WIDTH/4,self.screen.WIDTH, self.HEIGHT/10)
      self.top_bar.set_round(1)
      self.draw_color = (0,0,0)
      self.drawing = False
      self.players = [Player("Bustin"), Player("Jonathan"), Player("Michael"), Player("Kevin")]
      for player in self.players:
        self.leaderboard.add_player(player)
      self.pallete = Pallete(100, self.screen.dx + self.screen.HEIGHT - 120, 120, 120, self.COLORS, self)
      self.chat_box = ChatBox(self.screen.dx + self.screen.WIDTH + 250, 50,300, self.HEIGHT * 6 / 7)
      self.chat_box.add_message("hello world!")
      self.chat_box.add_message("hello world!")
      self.draw_color = (0,0,0)

    def add_player(self, player):
      self.players.append(player)
      self.leaderboard.add_player(player)
    
    def render(self):
      self.window.fill(self.BG)
      self.leaderboard.render(self.window)
      self.top_bar.render(self.window)
      self.screen.render(self.window)
      self.pallete.render(self.window)
      self.chat_box.render(self.window)
      pygame.display.update()

    def handle_button(self):
      self.pallete.handle_click()
      mouse = pygame.mouse.get_pos()
      coord = self.screen.translate(mouse)
      if coord:
          self.screen.update_screen(coord, self.draw_color)

    def run(self):
      run = True
      clock = pygame.time.Clock()
      while run:
        clock.tick(60) # 60 fps
        self.render()
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False
            break 
          if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_button()
      pygame.quit()


if __name__ == "__main__":
  # set pygame background color to blue


  pygame.font.init()
  g = Game()
  g.run()
