import pygame

def controlPanel(rectangle):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and rectangle.moveX > 0):
                    rectangle.moveX = -rectangle.moveX
                if (event.key == pygame.K_RIGHT and rectangle.moveX < 0):
                    rectangle.moveX = -rectangle.moveX
                if (event.key == pygame.K_DOWN and rectangle.moveY < 0):
                    rectangle.moveY = -rectangle.moveY
                if (event.key == pygame.K_UP and rectangle.moveY > 0):
                    rectangle.moveY = -rectangle.moveY