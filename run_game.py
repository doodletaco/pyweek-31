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
white = (245, 245, 245)

# invent time
clock = pygame.time.Clock()

# create the images used
center_image = pygame.image.load('images/angry_blob.png')
enemy_image = pygame.image.load('images/heart.png')
enemy_image_needsclick = pygame.image.load('images/heart_red.png')
screen_image = pygame.image.load('images/screen.png')
game_image = pygame.image.load('images/gameplay.png')

# initialize audio files
blip = pygame.mixer.Sound('audio/Blip_Select.wav')
hurt = pygame.mixer.Sound('audio/Hit_Hurt2.wav')
lost_life_sound = pygame.mixer.Sound('audio/Hit_Hurt4.wav')
start_sound = pygame.mixer.Sound('audio/Jump.wav')

pygame.mixer.music.set_volume(0.5)


# load fonts
font = pygame.font.Font('other-files/OpenDyslexic3-Regular.ttf', 20)

#initialize global variables
score = 0
lives = 3
last_angered = None

with open('other-files/save-data.txt') as sd:
    high_score = int(sd.read())


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
        global score, high_score, lives
        # checks if the corresponding square needs to be clicked
        if self.needsClick:
            self.needsClick = False
            self.image = enemy_image
            score += 1
            if score > high_score:
                high_score = score

            blip.play()
        # if not, end the game
        else:
            if lives > 1:
                lost_life_sound.play()
                lives -= 1
            else:
                if score == high_score:
                    with open('other-files/save-data.txt', 'w') as sd:
                        sd.write(str(high_score))
                score = 0
                lives = 3
                pygame.mixer.music.stop()
                hurt.play()
                end_screen()


# draw the window and all the stuff in it
def draw_window(center, e1, e2, e3, e4, score):
    global lives
    dis.blit(game_image, (0, 0))

    dis.blit(center_image, (center.x, center.y))

    dis.blit(e1.image, (e1.rectangle.x, e1.rectangle.y))
    dis.blit(e2.image, (e2.rectangle.x, e2.rectangle.y))
    dis.blit(e3.image, (e3.rectangle.x, e3.rectangle.y))
    dis.blit(e4.image, (e4.rectangle.x, e4.rectangle.y))

    score_text = 'Hearts Copped: ' + str(score)
    score_surface = font.render(score_text, False, white)
    dis.blit(score_surface, (15, 15))

    lives_counter = 'Lives: '
    for i in range(lives):
        lives_counter += 'X'
    lives_surface = font.render(lives_counter, False, white)
    dis.blit(lives_surface, (15, 45))

    pygame.display.update()


# game over screen
def end_screen():
    global high_score, play_time
    pygame.mixer.music.stop()
    pygame.mixer.music.load('audio/FranticLevel.wav')
    pygame.mixer.music.play(-1)
    run = True
    while run:
        # track events
        for event in pygame.event.get():
            # detect when exit button pressed
            if event.type == pygame.QUIT:
                run = False
            # detect key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main()

        dis.blit(screen_image, (0, 0))
        # display text and stuff
        words = 'Most Hearts Copped: ' + str(high_score)
        textsurface = font.render(words, False, white)

        more_words = 'Press the up arrow to play.'
        other_textsurface = font.render(more_words, False, white)

        dis.blit(textsurface, (15, 15))
        dis.blit(other_textsurface, (15, 40))

        pygame.display.update()

    pygame.quit()
    quit()


# causes a random square to be activated if there are no others
def anger(enemies):
    global last_angered
    none_angy = True
    for e in enemies:
        if e.needsClick:
            none_angy = False
    if none_angy:
        approved = False
        while not approved:
            chosen = random.choice(enemies)
            if chosen is not last_angered:
                last_angered = chosen
                approved = True
                chosen.get_angy()

# main loop
def main():
    global score, high_score, last_heart
    # create rectangles
    center = pygame.Rect(235, 215, 150, 150)

    enemy1rect = pygame.Rect(250, 50, 100, 100)
    enemy2rect = pygame.Rect(250, 450, 100, 100)
    enemy3rect = pygame.Rect(50, 250, 100, 100)
    enemy4rect = pygame.Rect(450, 250, 100, 100)

    #initialize enemy classes
    e1 = Enemy(enemy1rect, 'up')
    e2 = Enemy(enemy2rect, 'down')
    e3 = Enemy(enemy3rect, 'left')
    e4 = Enemy(enemy4rect, 'right')

    enemies = [e1, e2, e3, e4]

    last_heart = random.choice(enemies)

    pygame.mixer.music.stop()
    pygame.mixer.music.load('audio/Calm.wav')
    pygame.mixer.music.play(-1)

    start_sound.play()

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
        draw_window(center, e1, e2, e3, e4, score)
        # cap framerate
        clock.tick(60)

    # quit the game
    pygame.quit()
    quit()


# make sure correct one starts
if __name__ == "__main__":
    end_screen()
