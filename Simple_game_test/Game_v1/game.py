import pygame
import time
from rectangle import Rectangle
from controls import controlPanel
from obstacle import Obstacle

pygame.init()
#GLOBAL VARS
s_width = 800
s_height = 500
screen = pygame.display.set_mode((s_width, s_height))


def main_fun():

    rectangle = Rectangle( -3, 3, 300, 300, (0,128,254), 50, 50, s_width, s_height)
    obstacle = Obstacle(375, 225, 200, 200, s_width, s_height)

    done = False
    while not done:
        done = controlPanel(rectangle)
        
        rectangle.collisionDetection(rectangle, obstacle)

        rectangle.update_object_state(rectangle, rectangle.moveX, rectangle.moveY)

        rectangle.draw_object(screen, rectangle.obj, rectangle.color)
        obstacle.draw_object(screen, obstacle.obj, obstacle.color)

        print(rectangle.obj.x)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        screen.fill((0,0,0))

main_fun()