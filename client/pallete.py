from button import *

class Pallete(object):

  BORDER_WIDTH = 4

  def __init__(self, dx, dy, width, height, colors, game):
    self.dx = dx
    self.dy = dy
    self.width = width
    self.height = height
    self.colors = colors
    del self.colors[0] # remove the eraser color
    self.game = game
    self.dh = int(len(colors)**.5)
    self.dw = int(len(colors)/self.dh)
    self.clear_button = TextButton(self.dx - 50, self.dy + self.height, 100, 40, (100,100,100), "Clear")
    self.eraser = TextButton(self.dx + 50, self.dy + self.height, 100, 40, (100,100,100), "Eraser")
    self.buttons = [[None for _ in range(self.dh)] for _ in range(self.dw) ]
    self.init_colors(colors)

  def init_colors(self, colors):
    for i, color in enumerate(self.colors.values()):
      x = i // self.dw
      y = i % self.dw
      self.buttons[y][x] = Button(self.dx + x * self.width / 3, self.dy + y * self.height / 3, self.width / 3, self.height / 3, color, border_color=None)

  def render(self, window):
    x = y = 0
    pygame.draw.rect(window, (0,0,0), 
      (self.dx - self.BORDER_WIDTH/2, self.dy - self.BORDER_WIDTH/2, 
      self.width + self.BORDER_WIDTH, self.height + self.BORDER_WIDTH), self.BORDER_WIDTH)
    for i, color in enumerate(self.colors. values()):
      x = i // self.dw
      y = i % self.dw
      pygame.draw.rect(window, color, \
        (self.dx + x * self.width / 3, 
        self.dy + y * self.height / 3, 
        self.width / 3, self.height / 3))
    self.clear_button.render(window)
    self.eraser.render(window)
        
  def handle_click(self):
    coord = pygame.mouse.get_pos()
    for button_row in self.buttons:
      for button in button_row:
        if button.pressed(coord):
          self.game.draw_color = button.get_color()

    if self.clear_button.pressed(coord):
      self.game.screen.clear_screen()

    if self.eraser.pressed(coord):
      self.game.draw_color = (200,200,200) # background for the screen color


