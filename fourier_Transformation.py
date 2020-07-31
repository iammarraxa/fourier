import pygame
import os
import math
from image import drawing

# Setting pos os Screen
height = 800
width = 1000

s_x = 220
s_y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = '1'

pygame.init()

# screen = pygame.display.set_mode((width, height))
fps = 60
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
screen.fill((0, 0, 0))

white = (230, 230, 230)
black = (28, 28, 28)
gray = (100, 100, 100)
green = (54, 255, 141)
gray2 = (80, 80, 100)

time = 0
path = []
x = []
y = []

posx = 400
posy = 520
offset = 300

file_path = 'D:\Ammar\python projects\PYGAMES\FOURIER\Transformation'

file = 'New Text Document.txt'


def dft(x):
    X = []
    N = len(x)
    k = 0
    while k < N:
        re = 0
        im = 0
        n = 0
        while n < N:
            phi = (math.pi * 2 * k * n) / N
            re += x[n] * math.cos(phi)
            im -= x[n] * math.sin(phi)
            n += 1

        re = re / N
        im = im / N

        freq = k
        amp = math.sqrt((re * re) + (im * im))
        phase = math.atan2(im, re)

        # print(X)
        X.append([re, im, freq, amp, phase])
        # print(X[k])
        k += 1
    return X


i = 0
skip = 1
with open(os.path.join(file_path, file), 'r') as fp:
    a = fp.read().split('\n')
while i < len(a):
    x.append(int(a[i].rstrip(')').lstrip('(').split(',')[0]))
    y.append(int(a[i].rstrip(')').lstrip('(').split(',')[1]))
    i += skip
# while i < len(drawing):
#     x.append(drawing[i].get('x'))
#     y.append(drawing[i].get('y'))
#     i += skip

fourierX = dft(x)
# print(fourierX)
fourierY = dft(y)


def epiCycles(circle_x, circle_y, rotation, fourier):
    for i in range(len(fourier)):
        prev_x = circle_x
        prev_y = circle_y
        freq = fourier[i][2]
        # print(freq)
        radius = fourier[i][3] / 3
        print(radius)
        phase = fourier[i][4]

        circle_x += int(radius * math.cos(freq * time + phase + rotation))
        circle_y += int(radius * math.sin(freq * time + phase + rotation))

        if int(radius) >= 1:
            circle_width = 1
        else:
            circle_width = 0
        pygame.draw.circle(screen, gray, (prev_x, prev_y), int(radius), circle_width)
        pygame.draw.line(screen, white, (prev_x, prev_y), (circle_x, circle_y), 3)
        pygame.draw.circle(screen, green, (circle_x, circle_y), 5)
    return [circle_x, circle_y]


running = True
while running:
    clock.tick(fps)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # circle_x = posx
    # circle_y = posy
    vx = epiCycles(800, 100, 0, fourierX)
    vy = epiCycles(150, 500, (math.pi / 2), fourierY)
    v = [vx[0], vy[1]]
    # path.insert(0, v)
    path.append(v)

    # print(path)
    #
    pygame.draw.line(screen, (255, 255, 255), (vx[0], vx[1]), (v[0], v[1]), 1)
    pygame.draw.line(screen, (255, 255, 255), (vy[0], vy[1]), (v[0], v[1]), 1)
    # pygame.draw.circle(screen, (255, 255, 255), (path[0][0], path[0][1]), 1, 0)
    connect = 0

    for j in range(len(path)):
        pygame.draw.circle(screen, (255, 255, 255), (path[j][0], path[j][1]), 1, 0)

        # if connect >= 1:
        #     pygame.draw.line(screen, (255, 255, 255), (path[j - 1][0], path[j - 1][1]), (path[j][0], path[j][1]), 1)
        # connect += 1

    dt = ((math.pi * 2) / len(fourierY))
    time += dt  # speed of circle

    # if len(path) > 800:
    #     path.pop()

    pygame.display.update()
pygame.quit()
