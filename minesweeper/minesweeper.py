import pygame as pg
import os
import math
import random
import time

def rounddown(x):
    return int(math.floor(x/ 20.0))*20
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pg.image.load(canonicalized_path)
                _image_library[path] = image
        return image
_sound_library = {}
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()
def show(x, y):
    for value in values:
        if x==value[0] and y==value[1]:
            values.remove((x, y, value[2]))
            checked.append((x, y, value[2]))
            if value[2]==0:
                neighbourhood = [(x-20,y-20), (x,y-20), (x+20,y-20), (x-20,y),
                     (x+20,y), (x-20,y+20), (x,y+20),(x+20,y+20)]
                for neighbour in neighbourhood:
                    for check in checked:
                        if neighbour[0]==check[0] and neighbour[1]==check[1]:
                            neighbourhood.remove(neighbour)
                for neighbour in neighbourhood:
                    show(neighbour[0],  neighbour[1])



coordinates = [(20*x, 20*y) for x in range(0, 20) for y in range(0, 15)]
bombs = random.sample(coordinates, 24)
flagged = []
values = []
checked = []
done = False
color = ((0, 156, 225))

for x, y in coordinates:
    neighbourhood = [(x-20,y-20), (x,y-20), (x+20,y-20), (x-20,y),
         (x+20,y), (x-20,y+20), (x,y+20),(x+20,y+20)]
    value = 0
    if((x, y) in bombs):
        values.append((x,y, -1))
        continue
    for neighbour in neighbourhood:
        if(neighbour in bombs):
            value+=1
    values.append((x, y, value))

pg.init()

font = pg.font.Font(None, 30)
screen = pg.display.set_mode((400,300))
clock = pg.time.Clock()


while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        (a, b) = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                round_a=rounddown(a)
                round_b=rounddown(b)
                if (round_a, round_b) in bombs:
                    done = True
                show(round_a, round_b)
            if event.button == 3:
                round_a=rounddown(a)
                round_b=rounddown(b)
                print(round_a, round_b)
                for flag in flagged:
                    if flag[0]==round_a and flag[1]==round_b:
                        values.append(flag)
                        flagged.remove(flag)
                        break
                else:
                    for value in values:
                        if value[0]==round_a and value[1]==round_b:
                            values.remove(value)
                            flagged.append(value)



    screen.fill((0, 0, 0))

    if set(bombs)==set((flag[0], flag[1]) for flag in flagged):
        done=True
    for x, y, value in values:
        screen.blit(get_image('mine.jpg'), (x, y))
        pg.draw.rect(screen, color, pg.Rect(x, y, 20, 20), 1)
    for x, y, value in checked:
        value_display = "{}".format(value)
        text = font.render(value_display, True, (0, 128, 0))
        screen.blit(text, (x, y))
        if value==-1:
            screen.blit(get_image('sweeped.png'), (x, y))
    for flag in flagged:
        screen.blit(get_image('flag.png'), (flag[0], flag[1]))
    pg.display.flip()
    clock.tick(60)
time.sleep(0.500)
