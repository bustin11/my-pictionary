import pygame

class Button(object):
  BORDER_WIDTH = 2
  def __init__(self, x, y, w, h, color=(200,200,200), border_color=(0,0,0)):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.color = color
    self.border_color = border_color
 
  def render(self, window):
    if self.border_color:
      pygame.draw.rect(window, self.border_color, (self.x, self.y, self.w, self.h), self.BORDER_WIDTH)
    pygame.draw.rect(window, self.color, (
    self.x + self.BORDER_WIDTH, self.y + self.BORDER_WIDTH, self.w - self.BORDER_WIDTH * 2,
    self.h - self.BORDER_WIDTH * 2))

  def pressed(self, coords):
    if coords[0] > self.x and coords[0] < self.x + self.w and coords[1] > self.y and coords[1] < self.y + self.h:
      return True
    return False

  def get_color(self):
    return self.color



class TextButton(Button):
  def __init__(self, x, y, w, h, color, text, border_color=(0,0,0)):
    super().__init__(x, y, w, h, color, border_color)
    self.text = text
    self.text_font = pygame.font.SysFont("Arial", 30)

  def change_font_size(self, size):
    self.text_font = pygame.font.SysFont("Arial", size)

  def render(self, window):
    super().render(window)
    txt = self.text_font.render(self.text, 1, (0,0,0))
    window.blit(txt, (self.x + self.w/2 - txt.get_width()/2, self.y + self.h/2 - txt.get_height()/2))
