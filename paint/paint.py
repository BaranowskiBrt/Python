import pygame
import time
import math
import os
import tkinter as tk
def rounddown(x):
    '''returns argument decreased to the closest multiple of 20'''
    return int(math.floor(x/ 20.0))*20

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image


done = False
pressed = False
is_eraser = False
is_fill = False

# Size of screen
height = 600
width = 600


cyan = (0, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)
current_color = ["black", (0, 0, 0)]
selected_framing = ["gold", (255, 215, 0)]
palette = [
("black", (0,0,0)),
("red", (255, 0, 0)),
("gray", (128, 128, 128)),
("purple", (160,32,255)),
("blue", (0, 32, 255)),
("green", (0, 192, 0)),
("yellow", (255, 224, 32)),
("orange", (255, 127, 80)),
("brown", (160, 128,96))
]


pygame.init()
pygame.display.set_caption("Paint")
screen = pygame.display.set_mode((width, height))
screen.fill(white)


clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS', 20)
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
board=screen.subsurface(pygame.Rect(0, 0, 600, 500))
options=["E", "F", "B"]
caption=[]


# Colors and functions
bottom_surface = pygame.Surface((width, 100))
bottom_surface.fill(cyan)
for i in range(len(palette)):
    pygame.draw.rect(bottom_surface,palette[i][1], pygame.Rect(20+20*(i%3),
        20+20*(math.floor(i/3)), 20, 20))
pygame.draw.rect(bottom_surface, selected_framing[1], pygame.Rect(20, 20, 20, 20), 2)
pygame.draw.rect(bottom_surface,white, pygame.Rect(500,20,80,20))
pygame.draw.rect(bottom_surface,white, pygame.Rect(500,60,80,20))
for i in range(0,3):
    pygame.draw.circle(bottom_surface, white, ((150+100*i, 50)), 30)
    caption.append(font.render(options[i], True, black))
save = font.render("Save", True, black)
load = font.render("Load", True, black)
save_rect = save.get_rect(center=(540, 530))
load_rect = load.get_rect(center=(540, 570))




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                (x,y) = pygame.mouse.get_pos()
                print(x, y)
                if y>500 and x<80:
                    x=rounddown(x-20)
                    y=rounddown(y-520)
                    for i in range(len(palette)):
                        if x == 20*(i%3) and y == 20*(math.floor(i/3)):
                            for j in range(len(palette)):
                                pygame.draw.rect(bottom_surface,palette[j][1], pygame.Rect(20+20*(j%3),
                                    20+20*(math.floor(j/3)), 20, 20))
                            current_color = palette[i]
                            pygame.draw.rect(bottom_surface, selected_framing[1],
                             pygame.Rect(20+20*(i%3), 20+20*(math.floor(i/3)), 20, 20), 2)
                elif 500<x<580 and 520<y<540:
                    save_name = "image.png"
                    pygame.image.save(board, save_name)
                    print("File {} has been saved".format(save_name))
                elif 500<x<580 and 560<y<580:
                    load_name = "image.png"
                    screen.blit(get_image(load_name), (0, 0))
                elif (x-150)**2 +(y-530)**2<=900:
                    print("white")
                    is_fill = False
                    is_eraser = True
                elif (x-250)**2 +(y-530)**2<=900:
                    print("fill")
                    is_fill = True
                    is_eraser = False
                elif (x-350)**2 +(y-530)**2<=900:
                    print("brush")
                    is_fill = False
                    is_eraser = False
                else:
                    pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pressed = False


    if pressed:
        (x,y) = pygame.mouse.get_pos()
        if y<500 and is_eraser==False:
             pygame.draw.circle(screen, current_color[1], (x, y), 15)
        elif y<500 and is_eraser==True:
             pygame.draw.circle(screen, white, (x, y), 15)
        elif y<500 and is_fill==True:
             pygame.draw.circle(screen, white, (x, y), 15)
    if is_eraser==True and is_fill==True:
        raise Exception('two different painitng modes')

    pygame.display.flip()
    screen.blit(bottom_surface, (0, 500))
    screen.blit(save, save_rect)
    screen.blit(load, load_rect)
    for i in range(0,3):
        screen.blit(caption[i],(150+100*i, 530))

    clock.tick(1000)
pygame.quit()
