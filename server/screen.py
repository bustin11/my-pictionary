


class Screen(object):
  WIDTH = HEIGHT = 512
  LINE_THICKNESS = 3 # 2*_FONT_SIZE+1 is the width of each draw

  def __init__(self):
    self.clear_screen()

  def blank_screen(self):
    return [[0] * self.WIDTH for _ in range(self.HEIGHT)]

  def clear_screen(self):
    self._screen = self.blank_screen()

  def update_screen(self, x, y, color):
    for (i, j) in self.neighbors(x, y):
      if 0 <= i < self.HEIGHT and 0 <= j < self.WIDTH:
        self._screen[i][j] = color

  def neighbors(self, x, y):
    neighbors = []
    for i in range(-self.LINE_THICKNESS, self.LINE_THICKNESS+1):
      for j in range(-self.LINE_THICKNESS, self.LINE_THICKNESS+1):
        neighbors.append((x+i, y+j))
    return neighbors

  def bucket_fill(self, x, y, color):
    pass 

  def get_screen(self):
    return self._screen
  



  