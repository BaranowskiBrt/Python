import pygame
import random
import tkinter as tk
from tkinter import messagebox

height = 600
width = 600
cols = 10
rows = 10
run = True
snake_position = []
snack_position = (0, 0)
FPS, timer = 120, 0
block_height = height//rows
block_width = width//cols
direction = "RIGHT"
grid = []
positions = []
for i in range(cols):
    for j in range(rows):
        positions.append((i*block_width, j*block_height))
class Grid:
    def __init__(self, height, width, cols, rows):
        self.height = height
        self.width = width
        self.cols = cols
        self.rows = rows
        self.block_height = height//rows
        self.block_width = width//cols

    def draw_grid(self):
        for i in range(cols):
            for j in range(rows):
                pygame.draw.rect(screen, (144,255,255), pygame.Rect(i*self.block_height+1,
                    j*self.block_width+1, self.block_height-1, self.block_width-1))
                # grid[i].append(Block(i, j))

class Block:
    def __init__(col, row, snake=False):
        self.col = col
        self.row = row
        self.snake = snake
    def turn(self):
        if snake == False:
            snake = True
        elif snake == True:
            snake = False
def end_of_snake(position):
    pygame.draw.rect(screen, (144,255,255), pygame.Rect(position[0]+1,
        position[1]+1, block_height-1, block_width-1))
def display_snake(position):
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(position[0]+1,
        position[1]+1, block_height-1, block_width-1))
def display_snack():
    global snack_position
    choices = [position for position in positions if position not in snake_position]
    snack_position = random.choice(choices)
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(snack_position[0]+1,
        snack_position[1]+1, block_height-1, block_width-1))
def message():
    master = tk.Tk()
    master.withdraw()
    messagebox.showinfo("Game Over", "Length of your snake: {}".format(len(snake_position)))
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((height, width))
grid = Grid(height, width, cols, rows)
grid.draw_grid()
snake_position.append(random.choice(positions))
display_snake(snake_position[0])
display_snack()
choice = direction
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if direction != "DOWN":
                    choice = "UP"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if direction != "UP":
                    choice = "DOWN"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if direction != "LEFT":
                    choice = "RIGHT"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if direction != "RIGHT":
                    choice = "LEFT"
    if timer%20 == 0:
        direction = choice
        timer = 0
        if direction == "UP":
            for pos in snake_position:
                if (snake_position[0][0], snake_position[0][1]-block_height) == pos:
                    message()
                    exit()
            if (snake_position[0][0], snake_position[0][1]-block_height) == snack_position:
                snake_position.insert(0, snack_position)
                display_snack()
                continue
            else:
                snake_position.insert(0, (snake_position[0][0], snake_position[0][1]-block_height))
                end_of_snake(snake_position.pop(-1))
        if direction == "DOWN":
            for pos in snake_position:
                if (snake_position[0][0], snake_position[0][1]+block_height) == pos:
                    message()
                    exit()
            if (snake_position[0][0], snake_position[0][1]+block_height) == snack_position:
                snake_position.insert(0, snack_position)
                display_snack()
                continue
            else:
                snake_position.insert(0, (snake_position[0][0], snake_position[0][1]+block_height))
                end_of_snake(snake_position.pop(-1))
        if direction == "RIGHT":
            for pos in snake_position:
                if (snake_position[0][0]+block_width, snake_position[0][1]) == pos:
                    message()
                    exit()
            if (snake_position[0][0]+block_width, snake_position[0][1]) == snack_position:
                snake_position.insert(0, snack_position)
                display_snack()
                continue
            else:
                snake_position.insert(0, (snake_position[0][0]+block_width, snake_position[0][1]))
                end_of_snake(snake_position.pop(-1))
        if direction == "LEFT":
            for pos in snake_position:
                if (snake_position[0][0]-block_width, snake_position[0][1]) == pos:
                    message()
                    exit()
            if (snake_position[0][0]-block_width, snake_position[0][1]) == snack_position:
                snake_position.insert(0, snack_position)
                display_snack()
                continue
            else:
                snake_position.insert(0, (snake_position[0][0]-block_width, snake_position[0][1]))
                end_of_snake(snake_position.pop(-1))
        if snake_position[0][0] < 0:
            snake_position[0] =(snake_position[0][0]+width,snake_position[0][1])
        if snake_position[0][1] < 0:
            snake_position[0] =(snake_position[0][0],snake_position[0][1]+height)
        if snake_position[0][0] >= 600:
            snake_position[0] =(snake_position[0][0]-width,snake_position[0][1])
        if snake_position[0][1] >= 600:
            snake_position[0] =(snake_position[0][0],snake_position[0][1]-height)
        for segment in snake_position:
            display_snake(segment)

    timer+=1
    clock.tick(FPS)
    pygame.display.flip()
