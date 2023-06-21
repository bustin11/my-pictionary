


class Screen(object):
  ROWS = COLS = 128
  WIDTH = HEIGHT = 512 # not needed, same as client
  LINE_THICKNESS = 1 # not needed, same as client

  def __init__(self):
    self.clear_screen()

  def blank_screen(self):
    return [[0] * self.COLS for _ in range(self.ROWS)]

  def clear_screen(self):
    self._screen = self.blank_screen()

  def update_screen(self, x, y, color):
    for (i, j) in self.neighbors(x, y):
      if 0 <= i < self.ROWS and 0 <= j < self.COLS:
        self._screen[i][j] = color

  def neighbors(self, x, y):
    neighbors = []
    for i in range(-self.LINE_THICKNESS, self.LINE_THICKNESS+1):
      for j in range(-self.LINE_THICKNESS, self.LINE_THICKNESS+1):
        neighbors.append((x+i, y+j))
    return neighbors

  def bucket_fill(self, x, y, color):
    raise NotImplementedError()

  def get_screen(self):
    return self._screen
  



  