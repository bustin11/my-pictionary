import pygame


class Screen(object):
  ROWS = COLS = 64 # 8 * 64 = 512, since game is too laggy
  SPLASH = 8
  WIDTH = HEIGHT = 512 # PIXELS
  LINE_THICKNESS = 3 # 2*_FONT_SIZE+1 is the width of each draw
  BORDER_WIDTH = 4

  def __init__(self, dx, dy, colors):
    self.dx = dx
    self.dy = dy
    self.colors = colors
    self.clear_screen()

  def clear_screen(self):
    self._screen = [[(200,200,200)] * self.ROWS for _ in range(self.COLS)]
    self._scrn = [[0] * self.ROWS for _ in range(self.COLS)]

  def update_screen(self, x, y, c):
    self._screen[x][y] = c

  def unzip_screen(self):
    for i in range(self.ROWS):
      for j in range(self.COLS):
        self._screen[i][j] = self.colors[self._scrn[i][j]]

  def in_bounds(self, coords):
    return 0 <= coords[0] < self.COLS and 0 <= coords[1] < self.ROWS

  def translate(self, coords):
    if not self.in_bounds(coords):
      return ()
    return ((self.dx + coords[0]) / self.SPLASH, (self.dy + coords[1]) / self.SPLASH)
    
  def render(self, window):
    # outer border
    pygame.draw.rect(window, (0,0,0), \
      (self.dy-self.BORDER_WIDTH/2, self.dx - self.BORDER_WIDTH/2, \
        self.WIDTH + self.BORDER_WIDTH, self.HEIGHT + self.BORDER_WIDTH), \
          self.BORDER_WIDTH)
    # drawing
    for i in range(self.ROWS):
      for j in range(self.COLS):
        pygame.draw.rect(window, self._screen[i][j], (self.dy + j*self.SPLASH, self.dx + i*self.SPLASH, self.SPLASH, self.SPLASH), 0)

  def update_screen(self, x, y, color):
    for (i, j) in self.neighbors(x, y):
      if self.in_bounds((i,j)):
        self._screen[i][j] = color

  def neighbors(self, x, y):
    neighbors = []
    for i in range(-self.LINE_THICKNESS, self.LINE_THICKNESS+1):
      for j in range(-self.LINE_THICKNESS, self.LINE_THICKNESS+1):
        neighbors.append((x+i, y+j))
    return neighbors
