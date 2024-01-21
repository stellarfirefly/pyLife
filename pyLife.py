import pygame
import bresenham

window_res_x = 800
window_res_y = 800
grid_size_x = 100
grid_size_y = 100
framerate = 60

def draw_cell(cell, x, y, size):
  rect = pygame.Rect(x * size, y * size, size, size)
  if(cell):
    pygame.draw.rect(screen, 'white', rect)
  else:
    pygame.draw.rect(screen, 'black', rect)

def draw_grid(grid):
  for i, row in enumerate(grid):
    for j, cell in enumerate(row):
      draw_cell(cell, i, j, cell_size)
  if is_paused and i > 3 and j > 3:   # i, j holds x_dim-1, y_dim-1
    xluc_red = pygame.Color(255, 0, 0, 64)    # translucent red color
    pause_rect_1 = pygame.Rect(cell_size, cell_size, cell_size, cell_size*3)
    pause_rect_2 = pygame.Rect(cell_size*3, cell_size, cell_size, cell_size*3)
    pygame.draw.rect(screen, xluc_red, pause_rect_1)
    pygame.draw.rect(screen, xluc_red, pause_rect_2)

def is_within_bounds(i, j):
  return i >= 0 and i < grid_size_y and j >= 0 and j < grid_size_x

def is_live(grid, i, j):
  return is_within_bounds(i, j) and grid[i][j]

def count_neighbors(grid, i, j):
  return [
    is_live(grid, i-1, j),
    is_live(grid, i+1, j),
    is_live(grid, i, j-1),
    is_live(grid, i, j+1),
    is_live(grid, i-1, j-1),
    is_live(grid, i-1, j+1),
    is_live(grid, i+1, j-1),
    is_live(grid, i+1, j+1)
  ].count(True)

def compute_new_state(grid):
  new_grid = []
  for i in range(0, len(grid)):
    row = []
    for j in range(0, len(grid[i])):
      count = count_neighbors(grid, i, j)
      cell = count == 3 or (count == 2 and grid[i][j])
      row.append(cell)
    new_grid.append(row)
  return new_grid

def calc_cell_pos(size):
  (mx, my) = pygame.mouse.get_pos()
  cx = int(mx / size)
  cy = int(my / size)
  return (cx, cy)

def get_cell_at_mouse(size):
  (cx, cy) = calc_cell_pos(size)
  if is_within_bounds(cx, cy):
    return (cx, cy)
  return (-1, -1)

#---- initialize the play grid
def init_grid(x, y):
  grid = []
  for i in range(0, x):
    row = []
    for j in range(0, y):
      row.append(0)
    grid.append(row)
  return grid

#---- calculate grid resolution
calc_x = int(window_res_x / grid_size_x)
calc_y = int(window_res_y / grid_size_y)
if calc_x < calc_y:   # cells are always square
  cell_size = calc_x  # so we use the smaller calculated size
else:
  cell_size = calc_y

grid = init_grid(grid_size_x, grid_size_y)

old_x = -1  # no line start yet
old_y = -1

pygame.init()
screen = pygame.display.set_mode((window_res_x, window_res_y))
is_running = True
is_paused = False
clock = pygame.time.Clock()

while is_running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      is_running = False
    if event.type == pygame.KEYDOWN:
      if event.key in [pygame.K_SPACE]:
        is_paused = not is_paused

  if not is_paused:
    grid = compute_new_state(grid)

  (m1, m2, m3) = pygame.mouse.get_pressed()
  if m3:
    grid = init_grid(grid_size_x, grid_size_y)
  if m1:
    (x, y) = get_cell_at_mouse(cell_size)
    if x >= 0:  # is a valid cell
      if old_x < 0:   # first point
        grid[x][y] = 1
      else:
        cells = bresenham.bresenham(old_x, old_y, x, y)
        for pt in cells:
          (xp, yp) = pt
          grid[xp][yp] = 1
      old_x = x
      old_y = y
  else:
    old_x = -1  # mouse button released, stop line drawing
    old_y = -1

  draw_grid(grid)
  pygame.display.flip()
  clock.tick(framerate)

pygame.quit()

