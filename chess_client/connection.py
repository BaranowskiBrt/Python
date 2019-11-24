# Author: Bartłomiej Baranowski
# Client side connection establishment for chess game.

# Convention of message between clients is: "yd, xd, yf, yd",
# where xd and yd are coordinates of the destination, xf and yf of selected figure.
# Coordinates are modified by the receiving side, Taking into account the
# differences in field numbers (other side of chessboard).

import pygame
import tkinter
import threading
import socket
from tkinter import messagebox
import settings


def waiting_screen(screen):
    """Display waiting screen."""
    background = pygame.Surface((400, 100))
    background.set_alpha(128)
    background.fill((0, 0, 0))
    screen.blit(background, (200, 350))
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Waiting for an opponent...', False, (255, 255, 255))
    screen.blit(text, (220, 385))
    pygame.display.update()


def opponent_matching(s, grid):
    """Set color returned from server."""
    try:
        settings.your_color = s.recv(1024).decode("utf-8")
    except (ConnectionAbortedError, ConnectionResetError):
        if settings.done is not True:
            settings.done = True

    if settings.your_color == "white":
        settings.your_turn = True
    elif settings.your_color == "black":
        grid.height_start = 39
        grid.width_start = 36
        grid.start()
        threading.Thread(target=opponent_wait, args=(grid, s)).start()
    grid.blit_images()
    pygame.display.update()


def connect():
    """"Make socket connection with server"""
    port = 1105
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((settings.ip, port))
    return s


def opponent_wait(grid, s):
    """Wait for opponent to send his move(threaded)"""
    try:
        move = s.recv(1024).decode("utf-8")
        print(move)
        grid.move_opponent(move, s)
    except (ConnectionAbortedError, ConnectionResetError):
        if settings.done is not True:
            settings.done = True
    if settings.your_color == "":
        settings.done = True
