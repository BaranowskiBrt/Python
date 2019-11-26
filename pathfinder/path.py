import pygame
import tkinter as tk
from tkinter import messagebox
import sys
import math
import time

import settings
from gui import start_screen, distance_message, not_found

open = []
closed = []


class Grid:
    def __init__(self, screen, start, end):
        self.screen = screen
        self.block_width = settings.width//settings.cols
        self.block_height = settings.height//settings.rows
        self.start = start
        self.end = end
        self.grid = []

    def draw(self,color=settings.blue):
        x = 0
        for i in range(settings.cols):
            y = 0
            self.grid.append([])
            for j in range(settings.rows):
                pygame.draw.rect(self.screen, color, pygame.Rect(x+1, y+1,
                    self.block_width-1, self.block_height-1))
                self.grid[i].append(Block(i, j))
                y += settings.height//settings.rows
            x += settings.width//settings.cols
    def get_position(self, pos):
        return (pos[0]//(self.block_width), pos[1]//(self.block_height))

    def eraser_mode(self, x, y):
        if self.grid[x][y].obstacle == True:
            return True
        else:
            return False

    def erase(self, x, y):
        self.grid[x][y].erase_obstacle()
        pygame.draw.rect(self.screen, settings.blue, pygame.Rect(self.block_width*x+1,
         self.block_height*y+1, self.block_width-1, self.block_height-1))

    def turn(self, x, y):
        self.grid[x][y].make_obstacle()
        pygame.draw.rect(self.screen, settings.grey, pygame.Rect(self.block_width*x+1,
        self.block_height*y+1, self.block_width-1, self.block_height-1))

    def evaluate(self, x, y, distance):
        open.append(Block(x, y, self.grid[x][y].is_obstacle(), distance,abs(self.end[0]-x)+abs(self.end[1]-y)+distance))
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(12 * x, 12 * y, 12, 12))

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


def find_neighbours(grid, x, y):
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

def mark_ends(screen, start, end, start_color=(34, 139, 34), end_color=(250, 160, 122)):
    i = settings.width//settings.cols
    j = settings.height//settings.rows
    pygame.draw.rect(screen, start_color, pygame.Rect(i*start[0], j*start[1],i, j))
    pygame.draw.rect(screen, end_color, pygame.Rect(i*end[0], j*end[1],i, j))




def main():
    start, end = start_screen()
    if start[0]>settings.cols-1 or start[1]>settings.rows-1 or end[0]>settings.cols-1 or end[1]>settings.rows-1:
        sys.exit("Coordinates out of range")
    if start == end:
        print("Distance is equal to 0")
        exit()
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pathfinder")
    screen = pygame.display.set_mode((settings.width, settings.height))
    grid = Grid(screen, start, end)
    grid.draw()
    mark_ends(screen, start, end)
    done = False
    calculate = False


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
                    settings.mouse_pressed = True
                    (x, y) = grid.get_position(pygame.mouse.get_pos())
                    erase = grid.eraser_mode(x, y)
            if event.type == pygame.MOUSEBUTTONUP and calculate == False:
                if event.button == 1:
                    settings.mouse_pressed = False
                    erase = False
        if settings.mouse_pressed == True:
            (x, y) = grid.get_position(pygame.mouse.get_pos())

            if erase:
                grid.erase(x, y)
            else:
                if (x, y) != start and (x, y) != end:
                    grid.turn(x, y)
        if calculate == True:

            for neighbour in find_neighbours(grid, current.col, current.row):
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
        if calculate == True and settings.steps_on == True:
            clock.tick(30)
        else:
            clock.tick(500)

if __name__ == "__main__":
    main()
