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
# blob images
blob_up = pygame.image.load('images/angry_blob.png')
blob_down = pygame.image.load('images/angry_blob_down.png')
blob_left = pygame.image.load('images/angry_blob_left.png')
blob_right = pygame.image.load('images/angry_blob_right.png')

# heart images
enemy_image = pygame.image.load('images/heart.png')
enemy_image_needsclick = pygame.image.load('images/heart_red.png')
enemy_image_clicked = pygame.image.load('images/heart_blue.png')

# background images
screen_image = pygame.image.load('images/screen.png')
game_image = pygame.image.load('images/gameplay.png')

# initialize audio files
blip = pygame.mixer.Sound('audio/Blip_Select.wav') # sound played when key pressed in game
hurt = pygame.mixer.Sound('audio/Hit_Hurt2.wav') # sound when player lost all lives or deletes save data
lost_life_sound = pygame.mixer.Sound('audio/Hit_Hurt4.wav') # sound when player loses a life
start_sound = pygame.mixer.Sound('audio/Jump.wav') # sound when game starts
toggle_sound = pygame.mixer.Sound('audio/Pickup_Coin2.wav') # sound when the toggle for noise/music is enabled
other_toggle_sound = pygame.mixer.Sound('audio/Pickup_Coin4.wav') # sound when the toggle for noise/music is disabled

pygame.mixer.music.set_volume(0.7)


# load font
font = pygame.font.Font('other-files/OpenDyslexic3-Regular.ttf', 20)

#initialize global variables
score = 0 # how many hearts the player has copped
lives = 3 # how many lives the player has
last_angered = None # the heart that was last red
time_angy = 0 # how long there has been a lack of input
blob = None # the picture that the blob is
noise = True # toggle for whether or not there are bleeps (noise)
music = True # toggle for music

with open('other-files/save-data.txt') as sd:
    high_score = int(sd.read())


# make angy square bois
class Enemy:
    # initialize the class
    def __init__(self, rct, key, blob_image):
        self.rectangle = rct
        self.key = key
        self.blob_image = blob_image
        self.image = enemy_image
        self.needsClick = False
        self.isBlue = False
        self.framesBlue = 0

    # change the image to the square that needs to be clicked
    def get_angy(self):
        global blob
        if not self.needsClick:
            self.needsClick = True
            self.image = enemy_image_needsclick
            blob = self.blob_image


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

            if noise:
                blip.play()
        # if not, end the game
        else:
            if lives > 1:
                if noise:
                    lost_life_sound.play()
                lives -= 1
            else:
                if score == high_score:
                    with open('other-files/save-data.txt', 'w') as sd:
                        sd.write(str(high_score))
                lives_gone()

            self.isBlue = True


    # if the wrong button is picked, turn the heart blue for a moment
    def blue(self):
        if self.isBlue:
            # max number of frames blue
            if self.framesBlue < 6:
                self.image = enemy_image_clicked
                self.framesBlue += 1
            else:
                self.isBlue = False
                self.image = enemy_image
                self.framesBlue = 0


# draw the window and all the stuff in it
def draw_window(center, e1, e2, e3, e4, score):
    global lives
    dis.blit(game_image, (0, 0))

    dis.blit(blob, (center.x, center.y))

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


# causes a random square to be activated if there are no others
def anger(enemies):
    global last_angered, lives, time_angy

    # check if there is already an angered heart
    none_angy = True
    for e in enemies:
        if e.needsClick:
            none_angy = False
    # add a new red heard that cant be the last one if there is none already
    if none_angy:
        time_angy = 0
        approved = False
        while not approved:
            chosen = random.choice(enemies)
            if chosen is not last_angered:
                last_angered = chosen
                approved = True
                chosen.get_angy()
    # if the key isnt pressed fast enough, lose a life
    else:
        time_angy += 1
        if time_angy > 120:
            time_angy = 0
            lives -= 1
            if lives < 1:
                lives_gone()
            if noise:
                lost_life_sound.play()


# send the player back to the menu
def lives_gone():
    global lives, score
    score = 0
    lives = 3
    pygame.mixer.music.stop()
    if noise:
        hurt.play()
    end_screen()


# game over screen
def end_screen():
    global high_score, play_time, noise, music
    # play music if it is enabled
    if music:
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
                # key to start the game
                if event.key == pygame.K_UP:
                    main()
                # key to exit the game
                if event.key == pygame.K_ESCAPE:
                    run = False
                # key to reset the save data
                if event.key == pygame.K_r:
                    if noise:
                        lost_life_sound.play()
                    high_score = 0
                    with open('other-files/save-data.txt', 'w') as sd:
                        sd.write(str(high_score) + '\n')
                # toggle bleeps
                if event.key == pygame.K_n:
                    # enable noise
                    if noise:
                        noise = False
                        other_toggle_sound.play()
                    # disable noise
                    else:
                        noise = True
                        toggle_sound.play()
                # toggle music
                if event.key == pygame.K_m:
                    # disable music
                    if music:
                        music = False
                        pygame.mixer.music.stop()
                        other_toggle_sound.play()
                    # enable music
                    else:
                        music = True
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('audio/FranticLevel.wav')
                        pygame.mixer.music.play(-1)
                        toggle_sound.play()

        # display the background
        dis.blit(screen_image, (0, 0))

        # display text and stuff
        words = 'Most Hearts Copped: ' + str(high_score)
        textsurface = font.render(words, False, white)

        more_words = 'Press the up arrow to play.'
        other_textsurface = font.render(more_words, False, white)

        dis.blit(textsurface, (15, 15))
        dis.blit(other_textsurface, (15, 40))

        pygame.display.update()

    # exit the game
    pygame.quit()
    quit()


# main loop
def main():
    global score, high_score, last_heart
    # create rectangles, starting with the center character
    center = pygame.Rect(235, 215, 150, 150)

    # decide where the hearts go
    enemy1rect = pygame.Rect(250, 50, 100, 100)
    enemy2rect = pygame.Rect(250, 450, 100, 100)
    enemy3rect = pygame.Rect(50, 250, 100, 100)
    enemy4rect = pygame.Rect(450, 250, 100, 100)

    #initialize enemy classes
    e1 = Enemy(enemy1rect, 'up', blob_up)
    e2 = Enemy(enemy2rect, 'down', blob_down)
    e3 = Enemy(enemy3rect, 'left', blob_left)
    e4 = Enemy(enemy4rect, 'right', blob_right)

    # a list of enemies for easier processing
    enemies = [e1, e2, e3, e4]

    # initialize the last heart picked so that loop can function properly
    last_heart = random.choice(enemies)

    # only play music if the toggle is enabled
    if music:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('audio/Calm.wav')
        pygame.mixer.music.play(-1)

    # only play noise if the toggle is enabled
    if noise:
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

        # checks for processing input (or lack of it)
        for e in enemies:
            if key_pressed == e.key:
                e.calm_down()
            e.blue()

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
