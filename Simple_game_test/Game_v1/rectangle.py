import pygame

class Rectangle():

    s_width = 800
    s_height = 500
    moveX = 3
    moveY = -3
    rectPosX = 300
    rectPosY = 300
    color = (0,128,254)
    sizeX = 50
    sizeY = 50

    def __init__(self, mX, mY, rPX, rPY, col, sofX, sofY, sW, sH):
        self.moveX = mX
        self.moveY = mY
        self.rectPosX = rPX
        self.rectPosY = rPY
        self.color = col
        self.sizeX = sofX
        self.sizeY = sofY
        self.s_height = sH
        self.s_width = sW

    obj = pygame.Rect(rectPosX, rectPosY, sizeX, sizeY)

    @staticmethod
    def update_object_state(rectangle_par, moveX, moveY):
        rectangle_par.obj.left = rectangle_par.obj.left + moveX
        rectangle_par.obj.top = rectangle_par.obj.top + moveY

    @staticmethod
    def draw_objectt(screen, rectangle_par, color):
        pygame.draw.rect(screen, color, rectangle_par)

    @staticmethod
    def collisionDetection(rectangle_par, rock):

        if rectangle_par.obj.x < rock.obj.x + rock.sizeX and rectangle_par.obj.x + rectangle_par.sizeX > rock.obj.x and rectangle_par.obj.y < rock.obj.y + rock.sizeY and rectangle_par.obj.y + rectangle_par.sizeY > rock.obj.y:
                
                rectangle_par.moveX = -rectangle_par.moveX
                
                rectangle_par.moveY = -rectangle_par.moveY

        if rectangle_par.obj.x+rectangle_par.sizeX > rectangle_par.s_width:
            rectangle_par.moveX = -rectangle_par.moveX
        elif rectangle_par.obj.x < 0:
            rectangle_par.moveX = -rectangle_par.moveX
        elif rectangle_par.obj.y < 0:
            rectangle_par.moveY = -rectangle_par.moveY
        elif rectangle_par.obj.y+rectangle_par.sizeY > rectangle_par.s_height:
            rectangle_par.moveY = -rectangle_par.moveY

        
