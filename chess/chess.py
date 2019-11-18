# Author: Bartłomiej Baranowski
# Server side of chess game
# Allows for parallel matches
# Router and firewall have to be adjusted


import socket
import random
import threading
import time


PORT = 1105  # Packets are send through this port
connected = True


def convey(s1, s2):
    """Convey the packets from one player to the other"""
    while True:
        try:
            message = s2.recv(1024)
        except (ConnectionAbortedError, ConnectionResetError):
            s1.close()
            break
        if message != b'':
            s1.sendall(message)
        else:
            s1.close()
            break
        print("sent")


def play():
    """Wait for connections, randomly choose colors and send"""
    global connected
    player1 = connect()
    print("player1 connected")
    player2 = connect()
    print("player2 connected")
    connected = True
    colors = ["black", "white"]
    player1_color = random.choice(colors)
    player1.sendall(player1_color.encode())
    if player1_color == "white":
        player2.sendall("black".encode())
    else:
        player2.sendall("white".encode())
    threading.Thread(target=convey, args=(player1, player2)).start()  # New thread for each player
    convey(player2, player1)


def connect():
    """Look for connections"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen()
    while True:
        c, addr = s.accept()
        print("Connection established")
        return c


def main():
    global connected
    while True:
        if connected is True:
            threading.Thread(target=play).start()
            connected = False
        time.sleep(0.5)


if __name__ == '__main__':
    main()
