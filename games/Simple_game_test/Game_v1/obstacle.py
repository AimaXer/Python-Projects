import pygame


class Obstacle():

    s_width = 0
    s_height = 0
    rectPosX = 0
    rectPosY = 0
    color = (0,128,0)
    sizeX = 0
    sizeY = 0

    def __init__(self, rpx, rpy, sofx, sofy, sw, sh):
        self.rectPosX = rpx
        self.rectPosY = rpy
        self.sizeX = sofx
        self.sizeY = sofy
        self.s_height = sh
        self.s_width = sw

    obj = pygame.Rect(rectPosX, rectPosY, sizeX, sizeY)

    @staticmethod
    def draw_object(screen, rectangle_par, color):
        pygame.draw.rect(screen, color, rectangle_par)
