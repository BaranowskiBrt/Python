import pygame
import tkinter as tk
from tkinter import messagebox
import sys
import math
import time

from settings import *

# Variables

open = []
closed = []


############################################# CLASES ########################################
class Grid:
    def __init__(self, screen, width, height, rows, cols, start, end):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.block_width = self.width//self.cols
        self.block_height = self.height//self.rows
        self.grid = []

    def draw(self,color=blue):
        x = 0
        for i in range(self.cols):
            y = 0
            self.grid.append([])
            for j in range(self.rows):
                pygame.draw.rect(self.screen, color, pygame.Rect(x+1, y+1,
                    self.block_width-1, self.block_height-1))
                self.grid[i].append(Block(i, j))
                y += self.height//self.rows
            x += self.width//self.cols
    def get_position(self, pos):
        return (pos[0]//(self.block_width), pos[1]//(self.block_height))

    def eraser_mode(self, x, y):
        if self.grid[x][y].obstacle == True:
            return True
        else:
            return False

    def erase(self, x, y):
        self.grid[x][y].erase_obstacle()
        pygame.draw.rect(self.screen, blue, pygame.Rect(self.block_width*x+1,
         self.block_height*y+1, self.block_width-1, self.block_height-1))

    def turn(self, x, y):
        self.grid[x][y].make_obstacle()
        pygame.draw.rect(self.screen, grey, pygame.Rect(self.block_width*x+1,
        self.block_height*y+1, self.block_width-1, self.block_height-1))

    def evaluate(self, x, y, distance):
        open.append(Block(x, y, self.grid[x][y].is_obstacle(), distance,abs(end[0]-x)+abs(end[1]-y)+distance))
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(12 * x, 12 * y, 12, 12))

    def check_obstacle(self, pos):
        return self.grid[pos[0]][pos[1]].is_obstacle()


    def get_block(self, pos):
        return self.grid[pos[0]][pos[1]]

class Block:
    def __init__(self, col, row, obstacle=False, start_distance=-1, rating=-1):
        self.row = row
        self.col = col
        self.obstacle = obstacle
        self.rating = rating
        self.distance = start_distance
    def erase_obstacle(self):
        self.obstacle = False
    def make_obstacle(self):
        self.obstacle = True
    def is_obstacle(self):
        return self.obstacle
    def change_distance(self, distance):
        self.distance = distance


############################################# FUNCTIONS ########################################

def find_neighbours(x, y):
    neighbours = [(x+1, y), (x-1, y), (x+1, y+1), (x-1, y-1), (x, y+1), (x, y-1), (x-1,y+1), (x+1, y-1)]
    for neighbour in neighbours[:]:
        if neighbour[0]<0 or neighbour[1]<0 or neighbour[0]>49 or neighbour[1]>49 or grid.check_obstacle(neighbour):
            neighbours.remove(neighbour)
            continue
        for op in open:
            if neighbour[0] == op.col and neighbour[1] == op.row:
                try:
                    neighbours.remove(neighbour)
                except:
                    pass
        for close in closed:
            if neighbour[0] == close.col and neighbour[1] == close.row:
                try:
                    neighbours.remove(neighbour)
                except:
                    pass
    return neighbours

def mark_ends(start, end, start_color=(34, 139, 34), end_color=(250, 160, 122)):
    pygame.draw.rect(screen, start_color, pygame.Rect(i*start[0], j*start[1],i, j))
    pygame.draw.rect(screen, end_color, pygame.Rect(i*end[0], j*end[1],i, j))



############################################# TKINTER ########################################
master = tk.Tk()
def ret(event=None):
    global start, end, steps_on
    start = (int(startx.get()),int(starty.get()))
    end = (int(endx.get()),int(endy.get()))
    steps_on = var.get()
    master.destroy()
tk.Label(master, text="Input coordinates", font="Courier").grid(row=0, column=1, sticky=tk.N)
tk.Label(master, text="Start point").grid(row=1)
tk.Label(master, text="Destination point").grid(row=2)


startx = tk.Entry(master)
starty = tk.Entry(master)
endx = tk.Entry(master)
endy = tk.Entry(master)

startx.grid(row=1, column=1)
starty.grid(row=1, column=2)
endx.grid(row=2, column=1)
endy.grid(row=2, column=2)
var = tk.BooleanVar()

tk.Checkbutton(master, text="Show steps", variable=var).grid(row=3, column=2, sticky=tk.W)

button = tk.Button(master, text="Submit", command=ret).grid(row=4, column=1, sticky=tk.S)
master.bind('<Return>', ret)

master.mainloop()
def distance_message(distance):
    master = tk.Tk()
    master.withdraw()
    messagebox.showinfo("Distance", "Calculated distance is equal: {}".format(distance))
def not_found():
    master = tk.Tk()
    master.withdraw()
    messagebox.showinfo("No path", "There is no path to the destination")

if start[0]>cols-1 or start[1]>rows-1 or end[0]>cols-1 or end[1]>rows-1:
    sys.exit("Coordinates out of range")
if start == end:
    print("Distance is equal to 0")
    exit()
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Pathfinder")
screen = pygame.display.set_mode((width, height))
grid = Grid(screen, width, height, rows, cols, start, end)
grid.draw()
mark_ends(start, end)
done = False


############################################# MAIN LOOP ########################################


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                calculate = True
                current = grid.get_block(start)
                grid.evaluate(start[0], start[1], 0)
                closed.append(current)

        if event.type ==pygame.MOUSEBUTTONDOWN and calculate == False:
            if event.button == 1:
                mouse_pressed = True
                (x, y) = grid.get_position(pygame.mouse.get_pos())
                erase = grid.eraser_mode(x, y)
        if event.type == pygame.MOUSEBUTTONUP and calculate == False:
            if event.button == 1:
                mouse_pressed = False
                erase = False
    if mouse_pressed == True:
        (x, y) = grid.get_position(pygame.mouse.get_pos())

        if erase:
            grid.erase(x, y)
        else:
            if (x, y) != start and (x, y) != end:
                grid.turn(x, y)
    if calculate == True:

        for neighbour in find_neighbours(current.col, current.row):
            if  neighbour not in open:
                grid.evaluate(neighbour[0], neighbour[1], current.distance+1)
        if len(open) == 0:
            not_found()
            sys.exit()
        lowest = open[0].rating
        lowest_block = open[0]
        for option in open:
            if option.rating < lowest:
                lowest = option.rating
                lowest_block = option
        open.remove(lowest_block)
        closed.append(lowest_block)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(12 * lowest_block.col, 12 * lowest_block.row, 12, 12))
        current = lowest_block
        if lowest_block.col == end[0] and lowest_block.row == end[1]:
            distance_message(lowest_block.distance+1)
            done = True

    pygame.display.flip()
    if calculate == True and steps_on == True:
        clock.tick(30)
    else:
        clock.tick(500)
