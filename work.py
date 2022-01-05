import sys
 
import pygame
from pygame.locals import *
from random import randint
 
pygame.init()
 
fps = 10000
fpsClock = pygame.time.Clock()
 
pillar, pillar_side, n = 40, 20, int(input("what should the length of the field be?\n"))
width, height = pillar_side * n, pillar * pillar_side
margin = 30

chan1, chan2, chan3 = [0] * n, [0] * n, [0] * n
agents = int(input("how many agents should there be?\n"))
moves = int(input("how many times should each agent move?\n"))
mx_val1 = 1
mx_val2 = 1
mx_val3 = 1
curr = (n + 1) // 2
curr_max = curr
curr_min = curr
left = moves

screen = pygame.display.set_mode((width + 2 * margin, height + 2 * margin))

def upd():
    global left, curr, curr_max, curr_min, mx_val1, mx_val2, mx_val3
    if left == 0:
        curr = min(n - 1, max(curr, 0))
        curr_min = min(n - 1, max(curr_min, 0))
        curr_max = min(n - 1, max(curr_max, 0))
        chan1[curr_max] += 1
        chan2[curr] += 1
        chan3[curr_min] += 1
        mx_val1 = max(mx_val1, chan1[curr_max])
        mx_val2 = max(mx_val2, chan2[curr])
        mx_val3 = max(mx_val3, chan3[curr_min])
        left = moves
        curr = (n + 1) // 2
        curr_max = curr
        curr_min = curr
        return
    left -= 1
    curr += randint(-1, 1)
    curr_max = max(curr, curr_max)
    curr_min = min(curr, curr_min)

for _ in range(agents):
    for _ in range(moves):
        upd()
print(*chan1, '\n', *chan2, '\n', *chan3, sep=' ')

def draw():
    for i in range(1, pillar + 1):
        for j in range(n):
            flag1 = (chan1[j] * pillar // mx_val1 >= i)
            flag2 = (chan2[j] * pillar // mx_val2 >= i)
            flag3 = (chan3[j] * pillar // mx_val3 >= i)
            screen.fill((flag1 * 255, flag2 * 255, flag3 * 255), 
            (j * pillar_side + margin, pillar_side * pillar - ((i - 1) * pillar_side) + margin, pillar_side, pillar_side))
    screen.fill((127, 127, 127), (curr * pillar_side + margin, pillar * pillar_side + margin, pillar_side, pillar_side))

# Game loop.
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  upd()
  
  draw()
  
  pygame.display.flip()
  if left:
    fpsClock.tick(fps)
  else:
    fpsClock.tick(3)
