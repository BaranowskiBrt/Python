# Author: Bartłomiej Baranowski
# Client side of chess game


import pygame
import socket
import threading
import tkinter
from itertools import zip_longest
from tkinter import messagebox

import settings
from connection import waiting_screen, opponent_matching, connect, opponent_wait


class Figure:
    """Figure and it's characteristics"""
    def __init__(self, figure_type, x, y, pawn_jump=False):
        self.figure_type = figure_type
        self.x = x
        self.y = y
        self.pawn_jump = pawn_jump


class Grid:
    def __init__(self, screen, white_start, black_start, height, width, height_start, width_start, selected):
        self.screen = screen
        self.white_start = white_start
        self.black_start = black_start
        self.height = height
        self.width = width
        self.height_start = height_start
        self.width_start = width_start
        self.selected = selected
        self.can_castle = True
        self.your_king = None
        self.opponent_king = None
        self.position = []
        self.images = {}

    def initialize(self):
        """Load all the images"""
        for figure in self.white_start:
            self.images[figure] = pygame.image.load("./images/" + figure + ".png")
        for figure in self.black_start:
            self.images[figure] = pygame.image.load("./images/" + figure + ".png")
        self.images["white_pawn"] = pygame.image.load("./images/white_pawn.png")
        self.images["black_pawn"] = pygame.image.load("./images/black_pawn.png")
        self.images["chess_board"] = pygame.image.load("./images/chess_board.jpg").convert_alpha()


    def start(self):
        """Set grid to the starting position"""
        if settings.your_color == "white" or settings.your_color == "":
            for _ in range(8):
                self.position.append([])
            for i in range(8):
                self.position[0].append(Figure(self.black_start[i], i, 0))
                self.position[1].append(Figure("black_pawn", i, 1, True))
                for j in range(2, 6):
                    self.position[j].append(Figure(None, i, j))
                self.position[6].append(Figure("white_pawn", i, 6, True))
                self.position[7].append(Figure(self.white_start[i], i, 7))
            self.position = [[i for i in element] for element in list(zip_longest(*self.position))]

            # position of kings for check and mates
            self.your_king = self.position[4][7]
            self.opponent_king = self.position[4][0]


        elif settings.your_color == "black":
            self.images["chess_board"] = pygame.transform.rotate(self.images["chess_board"], 180)
            self.position = []
            for _ in range(8):
                self.position.append([])
            for i in range(8):
                self.position[0].append(Figure(self.white_start[-i-1], i, 0))
                self.position[1].append(Figure("white_pawn", i, 1, True))
                for j in range(2, 6):
                    self.position[j].append(Figure(None, i, j))
                self.position[6].append(Figure("black_pawn", i, 6, True))
                self.position[7].append(Figure(self.black_start[-i-1], i, 7))
            self.position = [[i for i in element] for element in list(zip_longest(*self.position))]

            # Position of kings for check and mates
            self.your_king = self.position[3][7]
            self.opponent_king = self.position[3][0]


    def blit_images(self):
        try:
            self.screen.blit(self.images.get("chess_board"), (0, 0))

            # blit every figure
            for i in range(8):
                for j in range(8):
                    if self.position[i][j].figure_type is not None:
                        figure = self.position[i][j]
                        self.screen.blit(self.images.get(figure.figure_type),
                                         (self.width_start+figure.x*self.width,
                                          self.height_start+figure.y*self.height))

            # blit selected field
            if self.selected is not None:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.width_start+self.width*self.selected.x,
                                                                       self.height_start+self.height*self.selected.y,
                                                                       self.width, self.height), 10)

            # display last moved figure
            if settings.last_move is not None:
                background = pygame.Surface((89, 90))
                background.set_alpha(128)
                background.fill((0, 0, 0))
                self.screen.blit(background, settings.last_move)
        except pygame.error:
            pass


    def try_move(self, x, y, s):
        """Move appropriately if possible"""
        field = self.select(x, y)
        figure_type = self.selected.figure_type

        # If selected empty field and figure is yours
        if (field is None or field.figure_type is None or not field.figure_type.startswith(settings.your_color))\
                and figure_type.startswith(settings.your_color):

            # Selected the figure, move, then check for check
            if figure_type.endswith("pawn"):
                moves = self.pawn_move() + self.pawn_hit()
                print(moves)
                for move in moves:
                    if field.x == move.x and field.y == move.y:
                        if not self.move(field, s):
                            continue
                        self.selected = field
                        moves = self.pawn_hit()
                        for move in moves:
                            if move.x == self.opponent_king.x and move.y == self.opponent_king.y:
                                root = tkinter.Tk()
                                root.withdraw()
                                messagebox.showinfo("Check", "You checked your opponent!")
                        self.selected = None


            elif figure_type.endswith("rook"):
                moves = self.linear_move()
                for move in moves:
                    if field.x == move.x and field.y == move.y:
                        if not self.move(field, s):
                            return
                        self.selected = field
                        moves = self.rook_move()
                        for move in moves:
                            if move.x == self.opponent_king.x and move.y == self.opponent_king.y:
                                root = tkinter.Tk()
                                root.withdraw()
                                messagebox.showinfo("Check", "You checked your opponent!")
                        self.selected = None


            elif figure_type.endswith("knight"):
                moves = self.knight_move()
                for move in moves:
                    if field.x == move.x and field.y == move.y:
                        if not self.move(field, s):
                            return
                        self.selected = field
                        moves = self.knight_move()
                        for move in moves:
                            if move.x == self.opponent_king.x and move.y == self.opponent_king.y:
                                root = tkinter.Tk()
                                root.withdraw()
                                messagebox.showinfo("Check", "You checked your opponent!")
                        self.selected = None

            elif figure_type.endswith("bishop"):
                moves = self.diagonal_move()
                for move in moves:
                    if field.x == move.x and field.y == move.y:
                        if not self.move(field, s):
                            return
                        self.selected = field
                        moves = self.diagonal_move()
                        for move in moves:
                            if move.x == self.opponent_king.x and move.y == self.opponent_king.y:
                                root = tkinter.Tk()
                                root.withdraw()
                                messagebox.showinfo("Check", "You checked your opponent!")
                        self.selected = None

            elif figure_type.endswith("queen"):
                moves = self.diagonal_move() + self.linear_move()
                for move in moves:
                    if field.x == move.x and field.y == move.y:
                        if not self.move(field, s):
                            return
                        self.selected = field
                        moves = self.diagonal_move() + self.linear_move()
                        for move in moves:
                            print(move.x, self.opponent_king.x, move.y, self.opponent_king.y)
                            if move.x == self.opponent_king.x and move.y == self.opponent_king.y:
                                root = tkinter.Tk()
                                root.withdraw()
                                messagebox.showinfo("Check", "You checked your opponent!")
                        self.selected = None

            elif figure_type.endswith("king"):
                moves = self.king_move()
                for move in moves:
                    if field.x == move.x and field.y == move.y:
                        if not self.move(field, s):
                            return
                        self.your_king = field
                        self.can_castle = False
                        self.selected = None


    def move(self, field, s, figure=None):

        # If there is no figure given take selected
        if figure is None:
            figure = self.selected

        field_type = field.figure_type

        # For sending to opponent
        move = str(field.x) + " " + str(field.y) + " " + str(figure.x) + " " + str(figure.y)

        self.position[field.x][field.y] = Figure(figure.figure_type, field.x, field.y)
        self.position[figure.x][figure.y] = Figure(None, figure.x, figure.y)

        if self.selected.figure_type.endswith("king"):
            self.your_king = self.position[field.x][field.y]


        # To allow check() to use self.selected
        selected_before = self.selected
        if self.check(True):
            # root = tkinter.Tk()
            # root.withdraw()
            # messagebox.showinfo("Check", "You cannot move there. That would be a check!")
            self.position[figure.x][figure.y] = Figure(figure.figure_type, figure.x, figure.y, figure.pawn_jump)
            self.position[field.x][field.y] = Figure(field.figure_type, field.x, field.y)
            self.selected = None
            self.blit_images()
            return False
        self.selected = selected_before

        # Short castling
        if self.can_castle and self.selected.figure_type.endswith("king") and field.x == 6 and field.y == 7:
            self.position[5][7] = Figure(self.position[7][7].figure_type, 5, 7)
            self.position[7][7] = Figure(None, 7, 7)


        settings.last_move = (self.width_start + self.width * figure.x, self.height_start + self.height * figure.y)

        s.sendall(move.encode())
        # Game over if king is defeated
        if field and field.figure_type and field.figure_type.endswith("king"):
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("You win", "You win!")
            settings.done = True

        settings.your_turn = False
        self.blit_images()
        pygame.display.update()
        threading.Thread(target=opponent_wait, args=(self, s)).start()
        return True


    def move_opponent(self, move, s):
        """Take move sent by an opponent and move on your copy of the grid"""
        try:
            field_x, field_y, figure_x, figure_y = move.split()
        except ValueError:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("Error", "Connection abolished")
            settings.done = True

        field = self.position[abs(int(field_x) - 7)][abs(int(field_y) - 7)]
        figure = self.position[abs(int(figure_x) - 7)][abs(int(figure_y) - 7)]
        settings.last_move = (self.width_start + self.width * figure.x, self.height_start + self.height * figure.y)

        # Game over if king is defeated
        if field is not None and field.figure_type is not None and field.figure_type.endswith("king"):
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo("You lose", "You lose!")
            settings.done = True

        # Short castling
        if figure is not None and figure.figure_type is not None and figure.figure_type.endswith("king") \
                and figure.x == 3 and figure.y == 0 and field.x == 1 and field.y == 0:
            print(self.position[0][0].figure_type)
            self.position[2][0] = Figure(self.position[0][0].figure_type, 2, 0)
            print(self.position[2][0].figure_type)
            self.position[0][0] = Figure(None, 0, 0)

        # Move opponent
        self.position[field.x][field.y] = Figure(figure.figure_type, field.x, field.y, figure.pawn_jump)
        self.position[figure.x][figure.y] = Figure(None, figure.x, figure.y)

        # Change position of opponent's king
        if figure.figure_type.endswith("king"):
            self.opponent_king = self.position[field.x][field.y]

        # Check if you are in check
        selected_before = self.selected
        self.check()
        self.selected = selected_before

        settings.your_turn = True
        self.blit_images()
        pygame.display.update()

    def display_possibilities(self, moves):
        """Display possible moves as circles"""
        for move in moves:
            pygame.draw.circle(self.screen, (0, 0, 255), (self.width_start + move.x * self.width+self.width//2,
                                                          self.height_start + move.y * self.height+self.height//2), 12)
            pygame.display.update()


    def select(self, x, y):
        """Select given field, d"""
        if self.width_start < x < settings.screen_width-self.width_start \
                and self.height_start < y < settings.screen_height - self.height_start:
            x_pos = (x-self.width_start)//self.width
            y_pos = (y-self.height_start)//self.height
            figure = self.position[x_pos][y_pos]

            # Calculate moves if your figure is selected
            if (figure is not None and figure.figure_type is not None\
                and figure.figure_type.startswith(settings.your_color)) or figure == self.selected:
                self.calculate_moves(figure)
            return figure

    def calculate_moves(self, figure):
        """Loop through the grid, search for opponent's figures, calculate their moves,
           check if they check your king"""

        previous = self.selected
        self.selected = figure
        self.blit_images()

        # If your figure was selected earlier redraw possibilities
        if previous is None or previous.figure_type is None or previous.figure_type.startswith(settings.your_color):
            if self.selected.figure_type.endswith("queen") or self.selected.figure_type.endswith("rook"):
                moves = self.linear_move()
                self.display_possibilities(moves)
            if self.selected.figure_type.endswith("queen") or self.selected.figure_type.endswith("bishop"):
                moves = self.diagonal_move()
            elif self.selected.figure_type.endswith("pawn"):
                moves = self.pawn_move() + self.pawn_hit()
            elif self.selected.figure_type.endswith("knight"):
                moves = self.knight_move()
            elif self.selected.figure_type.endswith("king"):
                moves = self.king_move()
            self.display_possibilities(moves)
        pygame.display.update()

    def check(self, trying=False):
        """Check if you are checked"""
        if settings.your_color == "white":
            color = "white"
        else:
            color = " black"
        for i in range(7):
            for j in range(7):
                self.selected = self.position[i][j]
                if self.selected is not None and self.selected.figure_type is not None and not\
                        self.selected.figure_type.startswith(settings.your_color):
                    if self.selected.figure_type.endswith("queen"):
                        moves = self.linear_move(color) + self.diagonal_move(color)
                    elif self.selected.figure_type.endswith("rook"):
                        moves = self.linear_move(color)
                    elif self.selected.figure_type.endswith("bishop"):
                        moves = self.diagonal_move(color)
                    elif self.selected.figure_type.endswith("pawn"):
                        moves = self.pawn_hit(color)
                    elif self.selected.figure_type.endswith("knight"):
                        moves = self.knight_move(color)
                    elif self.selected.figure_type.endswith("king"):
                        moves = self.king_move()
                    for move in moves:

                        if move.x == self.your_king.x and move.y == self.your_king.y:
                            if not trying:
                                root = tkinter.Tk()
                                root.withdraw()
                                messagebox.showinfo("Check", "Your king is checked!")
                            self.selected = None
                            return True
                self.selected = None
        return False


    def king_move(self):
        possible_moves = []
        unchecked_moves = ((self.selected.x + 1, self.selected.y + 1), (self.selected.x + 1, self.selected.y),
                           (self.selected.x + 1, self.selected.y -1), (self.selected.x, self.selected.y + 1),
                           (self.selected.x, self.selected.y -1), (self.selected.x - 1, self.selected.y + 1),
                           (self.selected.x - 1, self.selected.y), (self.selected.x - 1, self.selected.y - 1))
        for move in unchecked_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            fld = self.position[move[0]][move[1]]
            if fld is None or fld.figure_type is None or not fld.figure_type.startswith(settings.your_color):
                possible_moves.append(fld)
        if self.can_castle and not self.position[6][7].figure_type and not self.position[5][7].figure_type:
            possible_moves.append(self.position[6][7])
        return possible_moves

    def knight_move(self, color=None):
        if color == None:
            color = settings.your_color
        possible_moves = []
        unchecked_moves = ((self.selected.x + 2, self.selected.y + 1), (self.selected.x + 2, self.selected.y - 1),
                           (self.selected.x + 1, self.selected.y + 2), (self.selected.x + 1, self.selected.y - 2),
                           (self.selected.x - 1, self.selected.y + 2), (self.selected.x - 1, self.selected.y - 2),
                           (self.selected.x - 2, self.selected.y - 1), (self.selected.x - 2, self.selected.y + 1))
        for move in unchecked_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            fld = self.position[move[0]][move[1]]
            if fld is None or fld.figure_type is None or not fld.figure_type.startswith(color):
                possible_moves.append(fld)
        return possible_moves

    def pawn_move(self):
        possible_moves = []
        fld = self.position[self.selected.x][self.selected.y - 1]
        if fld is None or fld.figure_type is None:
            possible_moves.append(fld)
        fld = self.position[self.selected.x][self.selected.y - 2]
        if (fld is None or fld.figure_type is None) and self.selected.pawn_jump == True:
            possible_moves.append(fld)
        return possible_moves

    def pawn_hit(self, color=None):
        if color is None:
            color = settings.your_color
        possible_moves = []
        fld = None
        try:
            if color == settings.your_color:
                fld = self.position[self.selected.x - 1][self.selected.y - 1]
            else:
                fld = self.position[self.selected.x - 1][self.selected.y + 1]
        except:
            pass
        if fld is not None and fld.figure_type is not None and not fld.figure_type.startswith(color):
            possible_moves.append(fld)
        try:
            if color == settings.your_color:
                fld = self.position[self.selected.x + 1][self.selected.y - 1]
            else:
                fld = self.position[self.selected.x - 1][self.selected.y + 1]
        except:
            pass
        if fld is not None and fld.figure_type is not None and not fld.figure_type.startswith(color):
            possible_moves.append(fld)
        return possible_moves

    def linear_move(self, color=None):
        if color == None:
            color = settings.your_color
        possible_moves = []
        directions = (1, -1)
        for direction in directions:
            for i in range(1, 7):
                try:
                    x = self.selected.x + i * direction
                    y = self.selected.y
                    if x < 0 or y < 0:
                        break
                    fld = self.position[x][y]
                except (IndexError, AttributeError):
                    break
                if (fld is not None and fld.figure_type is None):
                    possible_moves.append(fld)
                elif not fld.figure_type.startswith(color):
                    possible_moves.append(fld)
                    break
                else:
                    break
            for i in range(1, 7):
                x = self.selected.x
                y = self.selected.y + i * direction
                if x < 0 or y < 0:
                    break
                try:
                    fld = self.position[x][y]
                except (IndexError, AttributeError):
                    break
                if (fld is not None and fld.figure_type is None):
                    possible_moves.append(fld)
                elif not fld.figure_type.startswith(color):
                    possible_moves.append(fld)
                    break
                else:
                    break
        return possible_moves

    def diagonal_move(self, color=None):
        if color == None:
            color = settings.your_color
        possible_moves = []
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        for direction in directions:
            for i in range(1, 7):
                x = self.selected.x + i * direction[0]
                y = self.selected.y + i * direction[1]
                if x < 0 or y < 0:
                    break
                try:
                    fld = self.position[x][y]
                except (IndexError, AttributeError):
                    break
                if (fld is not None and fld.figure_type is None):
                    possible_moves.append(fld)
                elif not fld.figure_type.startswith(color):
                    possible_moves.append(fld)
                    break
                else:
                    break
        return possible_moves



def main():

    # Set IP of the server here
    # ip = "192.168.1.3"
    ip = "10.129.242.209"
    settings.done = False
    height_start = 45
    width_start = 42
    height = 89
    width = 90
    white_start = ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop",
                   "white_knight", "white_rook"]
    black_start = ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop",
                   "black_knight", "black_rook"]


    # Start Pygame
    pygame.init()
    screen = pygame.display.set_mode((settings.screen_height, settings.screen_width))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess")
    selected = None
    grid = Grid(screen, white_start, black_start, height, width, height_start, width_start, selected)
    grid.initialize()
    grid.start()
    grid.blit_images()

    s = connect(ip)
    waiting_screen(screen)
    threading.Thread(target=opponent_matching, args=(s, grid)).start()
    while not settings.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and settings.your_turn is True and settings.your_color != "":
                if event.button == 1:
                    (x, y) = pygame.mouse.get_pos()
                    if grid.selected is not None and grid.selected.figure_type is not None:
                        grid.try_move(x, y, s)
                        pygame.display.update()
                    else:
                        grid.selected = None
                        grid.select(x, y)
        clock.tick(10)
    print("Done")
    s.close()


if __name__ == '__main__':
    main()
