# import and initialize pygame
import pygame, random
pygame.init()

# set up the screen
dis_w = 600
dis_h = 600
dis_size = (dis_w, dis_h)

dis = pygame.display.set_mode(dis_size)
pygame.display.set_caption('Pyweek 31')

# create a color
black = (0, 0, 0)

# invent time
clock = pygame.time.Clock()

# create the images used
center_image = pygame.image.load('images/placeholder_center.png')
enemy_image = pygame.image.load('images/placeholder_enemy.png')
enemy_image_needsclick = pygame.image.load('images/placeholder_enemy_needsclick.png')

# load the audio files
blip = pygame.mixer.Sound('audio/Blip_Select.wav')
hurt = pygame.mixer.Sound('audio/Hit_HUrt2.wav')

# make angy square bois
class Enemy:
    # initialize the class
    def __init__(self, rct, key):
        self.rectangle = rct
        self.key = key
        self.image = enemy_image
        self.needsClick = False

    # change the image to the square that needs to be clicked
    def get_angy(self):
        if not self.needsClick:
            self.needsClick = True
            self.image = enemy_image_needsclick

    # if the square needed to be clicked,
    def calm_down(self):
        # checks if the corresponding square needs to be clicked
        if self.needsClick:
            self.needsClick = False
            self.image = enemy_image
            blip.play()
        # if not, end the game
        else:
            hurt.play()
            end_screen()



# draw the window and all the stuff in it
def draw_window(center, e1, e2, e3, e4):
    dis.fill(black)

    dis.blit(center_image, (center.x, center.y))

    dis.blit(e1.image, (e1.rectangle.x, e1.rectangle.y))
    dis.blit(e2.image, (e2.rectangle.x, e2.rectangle.y))
    dis.blit(e3.image, (e3.rectangle.x, e3.rectangle.y))
    dis.blit(e4.image, (e4.rectangle.x, e4.rectangle.y))
    pygame.display.update()


# game over screen
def end_screen():
    print('Game ended')
    run = True
    while run:
        # track events
        for event in pygame.event.get():
            # detect when exit button pressed
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # detect key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main()

        dis.fill(black)
        pygame.display.update()


# causes a random square to be activated if there are no others
def anger(enemies):
    none_angy = True
    for e in enemies:
        if e.needsClick:
            last_angered = e
            none_angy = False
    if none_angy:
        choice = random.choice(enemies).get_angy()


# main loop
def main():
    # create rectangles
    center = pygame.Rect(250, 250, 100, 100)

    enemy1rect = pygame.Rect(287, 100, 26, 26)
    enemy2rect = pygame.Rect(287, 474, 26, 26)
    enemy3rect = pygame.Rect(100, 278, 26, 26)
    enemy4rect = pygame.Rect(474, 275, 26, 26)

    #initialize enemy classes
    e1 = Enemy(enemy1rect, 'up')
    e2 = Enemy(enemy2rect, 'down')
    e3 = Enemy(enemy3rect, 'left')
    e4 = Enemy(enemy4rect, 'right')

    enemies = [e1, e2, e3, e4]

    # loop
    run = True
    while run:
        key_pressed = ''
        # track events
        for event in pygame.event.get():
            # detect when exit button pressed
            if event.type == pygame.QUIT:
                run = False
            # detect key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_pressed = 'up'
                if event.key == pygame.K_DOWN:
                    key_pressed = 'down'
                if event.key == pygame.K_LEFT:
                    key_pressed = 'left'
                if event.key == pygame.K_RIGHT:
                    key_pressed = 'right'

        # trigger calm down for each corresponding square
        if key_pressed != '':
            for e in enemies:
                if key_pressed == e.key:
                    e.calm_down()

        # activate a square if there needs to be one
        anger(enemies)

        # draw the window
        draw_window(center, e1, e2, e3, e4)
        # cap framerate
        clock.tick(60)

    # quit the game
    pygame.quit()


# make sure correct one starts
if __name__ == "__main__":
    main()
