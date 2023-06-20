import pygame

class ChatBox(object):
  BG = (200, 200, 200)
  BORDER_WIDTH = 4
  MAX_NUM = 20

  def __init__(self, dx, dy, width, height):
    self.dx = dx
    self.dy = dy
    self.width = width
    self.height = height
    self.chat_history = []
    self.dh = self.height / self.MAX_NUM
    self.font = pygame.font.SysFont("comicsans", 20)

  def add_message(self, message):
    self.chat_history.append(message) 
  
  def get_messages(self):
    return self.chat_history

  def get_chat(self):
    return self.chat_history

  def clear(self):
    self.chat_history = []

  def render(self, window):
    pygame.draw.rect(window, (0,0,0), 
    (self.dx - self.BORDER_WIDTH/2, self.dy - self.BORDER_WIDTH/2, 
    self.width + self.BORDER_WIDTH, self.height + self.BORDER_WIDTH), self.BORDER_WIDTH)


    pygame.draw.rect(window, self.BG, (self.dx, self.dy, self.width, self.height))
    
    i = 0
    for message in self.chat_history:
      if len(message) > 30:
        message = message[:30] + "..."
      i += 1
      if i > self.MAX_NUM:
        break

      bg_color = (255, 255, 255)
      if i % 2 == 0:
        bg_color = (200, 200, 200)
      
      pygame.draw.rect(window, bg_color, (self.dx, self.dy + self.BORDER_WIDTH + i * self.dh, self.width, self.dh))
      text = self.font.render(message, 1, (0,0,0))
      window.blit(text, (self.dx + self.BORDER_WIDTH, self.dy + self.BORDER_WIDTH + i * self.dh - text.get_height()))

  
    