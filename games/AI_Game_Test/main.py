
import pygame
import random

#GLOBAL VARS
screen_width = 1000
screen_height = 800
rects_pos = [[100,100],[200,100],[300,100],[400,100],[500,100],[600,100],[700,100],[800,100],[100,300],[300,300]]

rect_size = [50,50]

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

class Rect():

    def rectangle(tabPos):
        obj = pygame.Rect(tabPos[0], tabPos[1], rect_size[0], rect_size[1])
        return obj

    def rectDraw(screen, obj):
        pygame.draw.rect(screen,(0,128,254), obj)


def check_outerlines_collision(pos):
    if pos[0] < 0:
        pos[0] = 0

    if pos[0] > screen_width - rect_size[0]:
        pos[0] = screen_width - rect_size[0] - 1

    if pos[1] < 0:
        pos[1] = 0

    if pos[1] > screen_height - rect_size[1]:
        pos[1] = screen_height - rect_size[1] - 1

    return pos

def main_function():

     while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        print(rects_pos[1][0])
        print(rects_pos[1][1])

        for i in rects_pos:
            rectangle = Rect.rectangle(i)
            Rect.rectDraw(screen, rectangle)
            
            for x in range(0, 10):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    rects_pos[x][0] += -1
                if keys[pygame.K_RIGHT]:
                    rects_pos[x][0] += 1
                if keys[pygame.K_UP]:
                    rects_pos[x][1] += -1
                if keys[pygame.K_DOWN]:
                    rects_pos[x][1] += 1

                # rects_pos[x][0] += random.randint(-1, 1)
                # rects_pos[x][1] += random.randint(-1, 1)

            i = check_outerlines_collision(i)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        screen.fill((0,0,0))

main_function()