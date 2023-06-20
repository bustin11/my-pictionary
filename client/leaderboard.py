"""
Represents the leaderboard object for the client side of the game.
"""
import pygame


class Leaderboard(object):
  BORDER_WIDTH = 3
  WIDTH = 200
  HEIGHT_ENTRY = 60

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.players = []
    self.name_font = pygame.font.SysFont("Arial", 20,bold=True)
    self.score_font = pygame.font.SysFont("Arial", 20)
    self.rank_font = pygame.font.SysFont("Arial", 25)

  def render(self, window):
    scores = [(player.name, player.score) for player in self.players]
    scores.sort(key=lambda x: -x[1])

    for i, score in enumerate(scores):
      if i % 2 == 0: # alternate pattern
        color = (255,255,255)
      else:
        color = (200,200,200)
      pygame.draw.rect(window, color,(self.x, self.y + i*self.HEIGHT_ENTRY, self.WIDTH, self.HEIGHT_ENTRY))

      # Text
      rank = self.rank_font.render("#" + str(i+1), 1, (0,0,0))
      window.blit(rank, (self.x + 10, self.y + i*self.HEIGHT_ENTRY + self.HEIGHT_ENTRY/2 - rank.get_height()/2)) #centralize

      name = self.name_font.render(score[0], 1, (0,0,0))
      window.blit(name, (self.x - name.get_width()/2 + self.WIDTH/2, self.y + i*self.HEIGHT_ENTRY + self.HEIGHT_ENTRY/4))

      score = self.score_font.render("Score: " + str(score[1]), 1, (0, 0, 0))
      window.blit(score, (self.x - name.get_width()/2 + self.WIDTH/2, self.y + i*self.HEIGHT_ENTRY + self.HEIGHT_ENTRY/2 + self.BORDER_WIDTH))

      pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT_ENTRY * len(scores)),
                        self.BORDER_WIDTH)

  def add_player(self, player):
      self.players.append(player)

  def remove_player(self, player):
      self.players.remove(player)
