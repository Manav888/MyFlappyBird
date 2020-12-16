import sys  # For closing the program sys.exit is used
import random  # Random numbers generation
import time  # For delaying frame 
import pygame # Module for running game in python
from pygame.locals import *  # Primary imports for python

#Defining global variables
frames_per_second = 32 # variable for maintaining frames per second of display
breadth_screen = 289 # width of the display
screen_length = 511 # height of the display
Display = pygame.display.set_mode((breadth_screen, screen_length)) # The display Screen
y_base = screen_length * 0.8 # y component of position of the base image
images_game = {} # a dictionary for all the images
sounds_game = {} # a dictionary for all the sounds used
jetman_player = 'gallery/images/jetman.png' # the player image
background_image = 'gallery/images/background_image.png' # the background image
covid_pipe = 'gallery/images/covid_pipe.png' # the image for pipe ( obstacles )


def starting_page(): # TO DISPLAY STARTING PAGE 
    x_player = int(breadth_screen / 5) # x component of position of player
    y_player = int((screen_length - images_game['player'].get_height()) / 2) # y component of position of player
    x_welcome = int((breadth_screen - images_game['welcome'].get_width()) / 2) # x component of position for welcome message
    y_welcome = int(screen_length * 0.13) # y component of position for welcome message

    while True:
        
        for event in pygame.event.get(): # A LOOP FOR USER INPUT
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): # for user to play game, input spacebar or Up arrow key
                return
            elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # for user to exit game, input Escape or cross button
                ''' 
                write_file_obj = open("score.txt","w")
                write_file_obj.write(str(0))
                write_file_obj.close()
                '''
                pygame.quit() # exit pygame
                sys.exit() # close system
            else:
                # displaying the main page until any input is recieved
                Display.blit(images_game['background_image'], (0, 0)) # function to display something on screen
                Display.blit(images_game['player'], (x_player, y_player))
                Display.blit(images_game['welcome'], (x_welcome, y_welcome))
                Display.blit(images_game['base'], (0, y_base))
                pygame.display.update() # a function to update the display as set
                FPSCLOCK.tick(frames_per_second) # a important function to maintain the smmothness of game by controlling fps


def game_main(): # THIS THE MAIN GAME
    score = 0 # variable t count score
    x_player = int(breadth_screen / 5) # x position of player
    y_player = int(breadth_screen / 2) # y position of player
    x_vel_pipe = -6 # x velocity of pipe
    y_vel_player = -9 # y velocity of player
    y_vel_player_max = 10 # max y velocity of player
    y_vel_player_min = -8 # min y velocity of player
    y_acc_player = 1 # acceleration to player while not flapping

    y_vel_flapping = -8  # y velocity of player while it is flapping
    player_flapped = False  # a boolean for check if the player has flapped or not

    # Creating pipes as obstacles to display
    new_pipe_1 = random_generate_pipe() # random function used to generate pipes for intresting blitting
    new_pipe_2 = random_generate_pipe()
    # Defining lower pipes as list
    lower_pipes = [
        {'x': breadth_screen + 200, 'y': new_pipe_1[1]['y']},
        {'x': breadth_screen + 200 + (breadth_screen / 2), 'y': new_pipe_2[1]['y']},
    ]
    # Defining upper pipes as list
    upper_pipes = [
        {'x': breadth_screen + 200, 'y': new_pipe_1[0]['y']},
        {'x': breadth_screen + 200 + (breadth_screen / 2), 'y': new_pipe_2[0]['y']},
    ]

    while True: # A Infinte loop for the game
        for event in pygame.event.get():
            # condition when player want to flap while playing
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if y_player > 0: # player is in air
                    y_vel_player = y_vel_flapping # player granted with velocity of flapping
                    player_flapped = True # boolean becomes true i.e player flapped.
                    sounds_game['fly'].play() # sound of flapping played
            # condition for player to exit game
            elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        score = score_calculation(x_player, score, upper_pipes) # A function for score calculation
        # Conditions for 
        if y_vel_player < y_vel_player_max and not player_flapped: # for no flapping, player connat reach max_vel 
            y_vel_player += y_acc_player
        elif player_flapped: # for multiple flapping
            player_flapped = False
        # A condition for player to not go below the base at any time
        height_player = images_game['player'].get_height()
        y_player = y_player + min(y_vel_player, y_base - y_player - height_player)
        # for blitting pipes
        pipe_handling(x_vel_pipe, upper_pipes, lower_pipes)
        display_running_game(upper_pipes, lower_pipes, x_player, y_player, score)
        Detecting_crash = collision_test(x_player, y_player, upper_pipes,lower_pipes)  # This function will return true if the player is crashed
                
        if Detecting_crash:
            time.sleep(2)
            endgame(score)
            time.sleep(3) 
            return

'''        
def for_crash(upper_pipes, lower_pipes, x_player, score):
    for covid_pipe in upper_pipes:
        if (y_player <= height_pipe + covid_pipe['y'] and abs(x_player - covid_pipe['x']) > (images_game['covid_pipe'][0].get_width()/2 + 10)):
            Display.blit(images_game['background_image'], (0, 0))
            for up_pipe, down_pipe in zip(upper_pipes, lower_pipes):
                Display.blit(images_game['covid_pipe'][0], (up_pipe['x'], up_pipe['y']))
                Display.blit(images_game['covid_pipe'][1], (down_pipe['x'], down_pipe['y']))
            Display.blit(images_game['base'], (0, y_base))
            Display.blit(images_game['player'], (x_player, y_base - 29))
            display_score(score)
            pygame.display.update()
            FPSCLOCK.tick(frames_per_second)

'''
def pipe_handling(x_vel_pipe, upper_pipes, lower_pipes):
    for up_pipe, down_pipe in zip(upper_pipes, lower_pipes): # to move pipes
        up_pipe['x'] += x_vel_pipe #doubt
        down_pipe['x'] += x_vel_pipe

    if 0 < upper_pipes[0]['x'] < 6: # adding new pipe
        new_pipe = random_generate_pipe()
        upper_pipes.append(new_pipe[0])
        lower_pipes.append(new_pipe[1])

    if upper_pipes[0]['x'] < -images_game['covid_pipe'][0].get_width(): # removing pipe that went out of display
        upper_pipes.pop(0)
        lower_pipes.pop(0) 

def display_running_game(upper_pipes, lower_pipes, x_player, y_player, score):
    Display.blit(images_game['background_image'], (0, 0))
    for up_pipe, down_pipe in zip(upper_pipes, lower_pipes):
        Display.blit(images_game['covid_pipe'][0], (up_pipe['x'], up_pipe['y']))
        Display.blit(images_game['covid_pipe'][1], (down_pipe['x'], down_pipe['y']))
    Display.blit(images_game['base'], (0, y_base))
    Display.blit(images_game['player'], (x_player, y_player))
    display_score(score)
    pygame.display.update()
    FPSCLOCK.tick(frames_per_second)
    
    
def display_score(score): #displaying score while game is running
    all_numbers = [int(x) for x in list(str(score))]
    width = 0
    for number in all_numbers:
        width += images_game['numbers'][number].get_width()
        gap_display_score = (breadth_screen - width) / 2

    for number in all_numbers:
        Display.blit(images_game['numbers'][number], (gap_display_score, screen_length * 0.12))
        gap_display_score += images_game['numbers'][number].get_width()

def collision_test(x_player, y_player, upper_pipes, lower_pipes): # to test collison
    if y_player > y_base - 29 or y_player < 0:
        sounds_game['crash'].play()
        return True
    for covid_pipe in upper_pipes:
        height_pipe = images_game['covid_pipe'][0].get_height()
        if (y_player <= height_pipe + covid_pipe['y'] and abs(x_player - covid_pipe['x']) < (images_game['covid_pipe'][0].get_width()/2 + 10)):
            sounds_game['crash'].play()
            return True
    for covid_pipe in lower_pipes:
        if ((y_player + images_game['player'].get_height() + 7 >= covid_pipe['y']) and abs(x_player - covid_pipe['x']) < (images_game['covid_pipe'][0].get_width()/2 + 10)):
            sounds_game['crash'].play()
            return True
    return False

def score_calculation(x_player, score, upper_pipes): # for score calculation
    position_mid_player = x_player + images_game['player'].get_width() / 2
    for covid_pipe in upper_pipes:
        position_mid_pipe = covid_pipe['x'] + images_game['covid_pipe'][0].get_width() / 2
        if position_mid_pipe < position_mid_player < position_mid_pipe + 6:
            score += 1
            print(f"Your current score is {score}")
            sounds_game['score'].play()
    return score

def random_generate_pipe(): # for random pipe genration 
    height_pipe = images_game['covid_pipe'][0].get_height()
    gap_pipe = screen_length / 3
    y_down_pipe = gap_pipe + random.randrange(4, int(screen_length - images_game['base'].get_height() - 1.1 * gap_pipe))
    x_pipe = breadth_screen + 10
    y_up_pipe = height_pipe - y_down_pipe + gap_pipe
    covid_pipe = [
        {'x': x_pipe, 'y': -y_up_pipe},  # covid_pipe upper
        {'x': x_pipe, 'y': y_down_pipe}  # covid_pipe lower
    ]
    return covid_pipe
def final_scoring(score, best_score): # for displaying final pipe

    best_score_number = [int(x) for x in list(str(best_score))]
    length = 0
    for num in best_score_number:
        length += images_game['final_scoring'][num].get_width()
        gap_display_score = ((breadth_screen - length) / 2) + 64

    for num in best_score_number:
        Display.blit(images_game['final_scoring'][num], (gap_display_score, screen_length * 0.43))
        gap_display_score += images_game['final_scoring'][num].get_width()

    all_numbers = [int(x) for x in list(str(score))]
    width = 0
    print(all_numbers)
    for number in all_numbers: 
        width += images_game['final_scoring'][number].get_width()
        gap_display_score = ((breadth_screen - width) / 2) + 62

    for number in all_numbers:
        Display.blit(images_game['final_scoring'][number], (gap_display_score, screen_length * 0.352))
        gap_display_score += images_game['final_scoring'][number].get_width()

def endgame(score): # endgame page
    read_file_object = open("score.txt","r")  # object to read the file
    best_score = read_file_object.read(3) #read function reads the file (3) i.e first three characters of the file

    Display.blit(images_game['final'], (0, 0))
    Display.blit(images_game['base'], (0, y_base))
    
    if(int(best_score)<score):
        write_file_object = open("score.txt","w") # object to write in the file
        write_file_object.write(str(score)) # writes the best score in the score.txt file
        best_score = score
        write_file_object.close()
        read_file_object.close()
        Display.blit(images_game['new_best_score'], (162, screen_length * 0.4))
    final_scoring(score, best_score)
    if 0 < score < 5:
        Display.blit(images_game['bronze'],(58, screen_length*0.375))
    elif 5 <= score < 10 :
        Display.blit(images_game['silver'],(58, screen_length*0.375))
    elif score >= 10:
        Display.blit(images_game['gold'],(58, screen_length*0.375))

    pygame.display.update()
    FPSCLOCK.tick(frames_per_second)
    
        
if __name__ == "__main__": # game starts here
    pygame.init()  # Initialising modules of python
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Clone')
    images_game['numbers'] = (
        pygame.image.load('gallery/images/0.png').convert_alpha(),
        pygame.image.load('gallery/images/1.png').convert_alpha(),
        pygame.image.load('gallery/images/2.png').convert_alpha(),
        pygame.image.load('gallery/images/3.png').convert_alpha(),
        pygame.image.load('gallery/images/4.png').convert_alpha(),
        pygame.image.load('gallery/images/5.png').convert_alpha(),
        pygame.image.load('gallery/images/6.png').convert_alpha(),
        pygame.image.load('gallery/images/7.png').convert_alpha(),
        pygame.image.load('gallery/images/8.png').convert_alpha(),
        pygame.image.load('gallery/images/9.png').convert_alpha(),
    )
    images_game['final_scoring'] = (
        pygame.image.load('gallery/images/final_scoring/0.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/1.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/2.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/3.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/4.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/5.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/6.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/7.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/8.png').convert_alpha(),
        pygame.image.load('gallery/images/final_scoring/9.png').convert_alpha(),
    )

    images_game['welcome'] = pygame.image.load('gallery/images/welcome.png').convert_alpha()
    images_game['base'] = pygame.image.load('gallery/images/base.png').convert_alpha()
    images_game['new_best_score'] = pygame.image.load('gallery/images/new.png').convert_alpha()
    images_game['covid_pipe'] = (pygame.transform.rotate(pygame.image.load(covid_pipe).convert_alpha(), 180),
                            pygame.image.load(covid_pipe).convert_alpha()
                            )
    images_game['final'] = pygame.image.load('gallery/images/final.png')
    images_game['bronze'] = pygame.image.load('gallery/images/bronze.png')
    images_game['silver'] = pygame.image.load('gallery/images/silver.png')
    images_game['gold'] = pygame.image.load('gallery/images/gold.png')    

    sounds_game['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    sounds_game['crash'] = pygame.mixer.Sound('gallery/audio/crash.wav')
    sounds_game['score'] = pygame.mixer.Sound('gallery/audio/score.wav')
    sounds_game['fly'] = pygame.mixer.Sound('gallery/audio/fly.wav')

    images_game['background_image'] = pygame.image.load(background_image).convert()
    images_game['player'] = pygame.image.load(jetman_player).convert_alpha()
    
    while True:
        starting_page() 
        game_main() 
        starting_page()