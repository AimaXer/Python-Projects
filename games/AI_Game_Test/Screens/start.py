
import pygame, time

bttn_w  = 300
bttn_h = 100

class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class main():

    @staticmethod
    def main(screen, screen_width, screen_height):

        exit_img_x = screen_width / 2 - bttn_w / 2
        exit_img_y = screen_height / 2
        start_img_x = screen_width / 2 - bttn_w / 2
        start_img_y = screen_height / 4

        start_loop = True
        # while start_loop:
        while start_loop:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            mouse = pygame.mouse.get_pos()

            if start_img_x < mouse[0] < start_img_x + bttn_w and start_img_y < mouse[1] < start_img_y + bttn_h:
                Start_Button = Image('Screens\\Start_jpeg\\Start_game_big.jpg', [start_img_x-25, start_img_y-10])
                screen.blit(Start_Button.image, Start_Button.rect)
                if pygame.mouse.get_pressed() == (1,0,0):
                    start_loop = False

            if exit_img_x < mouse[0] < exit_img_x + bttn_w and exit_img_y < mouse[1] < exit_img_y + bttn_h:
                Exit_Button = Image('Screens\\Start_jpeg\\Exit_game_big.jpg', [exit_img_x-25, exit_img_y-10])
                screen.blit(Exit_Button.image, Exit_Button.rect)
                if pygame.mouse.get_pressed() == (1,0,0):
                    pygame.quit()
                    quit()

            pygame.time.Clock().tick(30)
            pygame.display.flip()
            pygame.display.update()

            Start_Button = Image('Screens\\Start_jpeg\\Start_game.jpg', [start_img_x, start_img_y])
            Exit_Button = Image('Screens\\Start_jpeg\\Exit_game.jpg', [exit_img_x, exit_img_y])
            BackGround = Image('Screens\\Start_jpeg\\Background.jpg', [0, 0])
            screen.blit(BackGround.image, BackGround.rect)
            screen.blit(Start_Button.image, Start_Button.rect)
            screen.blit(Exit_Button.image, Exit_Button.rect)

            # time.sleep(2)

if __name__ == '__main__':
    main.main()