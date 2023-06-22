import pygame 


class TopBar(object):
  BORDER_WIDTH = 2

  def __init__(self, dx, dy, width, height, max_round=8, time=60):
    self.dx = dx
    self.dy = dy
    self.width = width
    self.height = height
    self.max_round = max_round
    self.word = ""
    self.round = 0
    self.time = time
    self.font = pygame.font.SysFont('Arial', 20)

  def render(self, window):
    pygame.draw.rect(window, (200,200,200), (self.dy, self.dx, self.width, self.height))
    pygame.draw.rect(window, (0,0,0), (self.dy, self.dx, self.width, self.height), self.BORDER_WIDTH)

    # text
    text = self.font.render(f"Round {self.round}/{self.max_round}", 1, (0,0,0))
    window.blit(text, (self.dy + 10, self.dx + self.height/2 - text.get_height()/2))

    # word
    word = self.word
    text = self.font.render(word, 1, (0,0,0))
    window.blit(text, (self.dy + self.width/2 - text.get_width()/2, self.dx + self.height/2 - text.get_height()/2 + 10)) # centralize

    pygame.draw.circle(window, (0,0,0), (self.dy + self.width - 50, self.dx + round(self.height/2)), self.height/2-10, self.BORDER_WIDTH)
    timer = self.font.render(str(self.time), 1, (0,0,0))
    window.blit(timer, (self.dy + self.width - 50 - timer.get_width()/2, self.dx + self.height/2 - timer.get_height()/2))


  @staticmethod
  def underscore_text(word):
    new_str = ""
    for char in word:
      if char != " ":
        new_str += " _ "
      else:
        new_str += "   "
    return new_str

  def set_word(self, word, hidden=True):
    if not hidden:
      self.word = word
    else:
      self.word = TopBar.underscore_text(word)

  def set_round(self, round):
    self.round = round

  def set_max_round(self, max_round):
    self.max_round = max_round

  def set_time(self, time):
    self.time = time