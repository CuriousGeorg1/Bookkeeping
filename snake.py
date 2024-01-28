import pygame
import time
import random
  
window_x = 720
window_y = 480

red = (255, 0, 0)
fruit_red = (181, 38, 38)
white = (237, 230, 206)
green = (47, 120, 38)
black = (0, 0, 0)

score = 0
high_score = 0

# defining snake properties
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
snake_speed = 15
snake_position = [100, 50]

# snake starting direction
direction = 'RIGHT'
change_to = direction

# Initialising pygame and window
pygame.init()
game_window = pygame.display.set_mode((window_x, window_y))
 
fps = pygame.time.Clock()

fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                  random.randrange(1, (window_y//10)) * 10]
 
fruit_spawn = True

# read high score from file
with open("highscore.txt") as score_file:
    file_score = score_file.read()
    if file_score != "":
        high_score = int(file_score)
    
# score and speed rendering functions
def show_score(choice, color, font, size):
    # score font
    score_font = pygame.font.SysFont(font, size)
    # render surface with font and text
    score_surface = score_font.render('Score : ' + str(score), True, color)
    # create a canvas for score
    score_rect = score_surface.get_rect()
    # canvas position
    score_rect.midleft = (0, 15)
    # display
    game_window.blit(score_surface, score_rect)

def show_high_score(choice, color, font, size):
    # render high score
    high_score_font = pygame.font.SysFont(font, size)
    high_score_surface = high_score_font.render("High Score : " + str(high_score), True, color)
    high_score_rect = high_score_surface.get_rect()
    high_score_rect.midtop = (window_x/2, 0)
    game_window.blit(high_score_surface, high_score_rect)
 
def show_speed(choice, color, font, size):
    # render current speed
    speed_font = pygame.font.SysFont(font,size)
    speed_surface = speed_font.render('Speed : ' + str(snake_speed), True, color)
    speed_rect = speed_surface.get_rect()
    speed_rect.midright = (window_x, 15)
    game_window.blit(speed_surface, speed_rect)

# End game menu
def end_screen():
    # Restart and quit text rendering
    game_window.fill(white)
    end_font = pygame.font.SysFont('comic sans', 50)
    again_surface = end_font.render('Press R to restart', True, fruit_red)
    end_surface = end_font.render('Press Q to quit', True, fruit_red)

    again_rect = again_surface.get_rect()
    end_rect = end_surface.get_rect()

    again_rect.midtop = (window_x/2, window_y/4)
    end_rect.midtop = (window_x/2, window_y/2)

    game_window.blit(again_surface, again_rect)
    game_window.blit(end_surface, end_rect)
    pygame.display.flip()

    # Monitor keybard button presses for restar or quit
    restart = False

    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Game over function
def game_over():
    global snake_speed
    global snake_position
    global high_score
    global snake_body
    global direction
    global score
    global change_to

    snake_speed = 0

    # save new high score to file
    if score > high_score:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
        high_score = score

    # Render your score and high score texts
    my_font = pygame.font.SysFont('comic sans', 50)
    
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    high_score_surface = my_font.render(
        'High Score : ' + str(high_score), True, red)
    
    game_over_rect = game_over_surface.get_rect()
    high_score_rect = high_score_surface.get_rect()
    
    game_over_rect.midtop = (window_x/2, window_y/4)
    high_score_rect.midtop = (window_x/2, window_y/2)
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(high_score_surface, high_score_rect)
    pygame.display.flip()

    time.sleep(2)
    # Restart or quit screen
    end_screen()

    # resetting the snake and score
    score = 0
    snake_speed = 15
    snake_position = [100, 50]
    direction = 'RIGHT'
    change_to = direction
    snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
 
# Main Function
while True:
    
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
        if event.type == pygame.QUIT:
            exit()
 
    # If two keys pressed simultaneously
    # we don't want snake to move into two 
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
 
    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
 
    # Snake body growing mechanism
    # collision -> growth
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
        snake_speed += 0.5
    else:
        snake_body.pop()
         
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
         
    fruit_spawn = True
    game_window.fill(white)
     
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, fruit_red, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))
 
    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()
    
    

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    
    # scoreboards and speed
    show_score(1, black, 'comic sans', 20)
    show_speed(1, black, 'comic sans', 20)
    show_high_score(1, black, 'comic sans', 20)
 

    pygame.display.update() 
    fps.tick(snake_speed)
