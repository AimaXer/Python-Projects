
import pygame
import random

#GLOBAL VARS
screen_width = 1000
screen_height = 800
rects_pos = [[100,100],[200,100],[300,100],[400,100],[500,100],[600,100],[700,100],[800,100],[100,300],[300,300]]

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

class Rect():

    def rectangle(tabPos):

        obj = pygame.Rect(tabPos[0], tabPos[1], 50, 50)
        return obj

    def rectDraw(screen, obj):

        pygame.draw.rect(screen,(0,128,254), obj)


def main_function():

     while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        for i in rects_pos:
            rectangle = Rect.rectangle(i)
            Rect.rectDraw(screen, rectangle)
            
            for x in range(0, 10):
                rects_pos[x][0] += random.randint(-1, 1)
                rects_pos[x][1] += random.randint(-1, 1)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        screen.fill((0,0,0))

main_function()