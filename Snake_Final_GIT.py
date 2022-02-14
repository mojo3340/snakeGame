"""
Game: Snake
Creator: Mohammed Hussain
Last Modified: 14th February 2022
"""

import pygame
from random import randint
from sys import exit
import math

pygame.init()
game_active = False #start the game on the Welcome Screen
game_font = pygame.font.Font("font/Pixeltype.ttf", 100)
clock = pygame.time.Clock() #an object to track time, for fps


def display_surface():
    """function to create the main window"""
    disp_surface = pygame.display.set_mode(size = (610, 700))
    pygame.display.set_caption("Snake")
    return disp_surface
disp_surface = display_surface()

#Welcome Screen
def welcome_message(disp_surface, game_font, body):
    """function to display game name and action to play"""
    title1_surface = game_font.render(f'Snake', False, "White")
    title1_rectangle = title1_surface.get_rect(center = (305, 250))
    disp_surface.blit(title1_surface, title1_rectangle)

    title2_surface = game_font.render(f'Press SPACE to play', False, "White")
    title2_rectangle = title2_surface.get_rect(center = (305, 450))
    disp_surface.blit(title2_surface, title2_rectangle)

    score_surface = game_font.render(f'High Score: {len(body)-1}', False, "Red")
    score_rectangle = score_surface.get_rect(center = (290,550))
    disp_surface.blit(score_surface, score_rectangle)

#Create the snake() and food() class for the game
class snake(pygame.sprite.Sprite):
    def __init__(self, x_pos = 300, y_pos = 300):
        #Access the super class of Sprite
        super().__init__()
        image1 = pygame.image.load("graphics/snake1.png").convert_alpha()
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image = image1
        self.rect = self.image.get_rect(x = x_pos, y = y_pos)

    def update(self, x_pos, y_pos):
        """defines the movement of the snake using arrow keys"""
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

snakegroup = pygame.sprite.Group()
original_snake = snake()
snakegroup.add(original_snake)

class food(pygame.sprite.Sprite):
    """class to control food action"""
    def __init__(self):
        #access the Sprite super class methods
        super().__init__()
        food1 = pygame.image.load("graphics/food1.png").convert_alpha()

        x_pos = randint(50,600)
        y_pos = randint(50,650)
        self.image = food1
        self.rect = self.image.get_rect(x = x_pos,y = y_pos)

foods = pygame.sprite.GroupSingle()
foods.add(food())

#Create function to track the relative positions of the snake body
track = [(original_snake.x_pos, original_snake.y_pos)] #a mutable list, contains coordinates stored in tupples

def update_body(track, distance):
    body = snakegroup.sprites() #access the group of snakes
    no_of_parts = len(body)
    body[0].update(*track[0])    
    track_i = 1 #counter
    next_i = 1 #counter

    for i in range(1, no_of_parts):
        while track_i < len(track): #this only works once the snake has eaten food AT LEAST ONCE
            pos = track[track_i] #Stores the x/y of the TAIL of the snake
            track_i += 1
            dx, dy = body[i-1].x_pos - pos[0], body[i-1].y_pos - pos[1]
            if math.sqrt(dx*dx + dy*dy) >= distance:
                body[i].update(*pos)
                next_i = i + 1
                break
    while next_i < no_of_parts:
        body[next_i].update(*track[-1])
        next_i += 1
    del track[track_i:]
    return body 

body = update_body(track, 20)

direction = (0, 0)
speed = 1.7

while True:
    if original_snake.rect.left == 0 or original_snake.rect.top == 0 or original_snake.rect.right == 0 or original_snake.rect.bottom == 0:
        snakegroup.empty()
        snakegroup.add(original_snake)
        game_active = False

    """EVENT LOOP CODE"""
    for eachevent in pygame.event.get():
        if eachevent.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:   
            if eachevent.type == pygame.KEYDOWN:
                if eachevent.key == pygame.K_LEFT and direction[0] != 1:
                    direction = (-1, 0)
                if eachevent.key == pygame.K_RIGHT and direction[0] != -1:
                    direction = (1, 0)
                if eachevent.key == pygame.K_UP and direction[1] != 1:
                    direction = (0, -1)
                if eachevent.key == pygame.K_DOWN and direction[1] != -1:
                    direction = (0, 1)
            
        else:
            if eachevent.type == pygame.KEYDOWN:
                if eachevent.key == pygame.K_SPACE:
                    game_active = True

    """PYGAME EVENT CODE"""
    if game_active:
        disp_surface = display_surface()
        snakegroup.draw(disp_surface)
        foods.draw(disp_surface)
        
        track.insert(0, track[0][:]) #insert another tuple to the list position 0. at tupple 1, and for both x and y
        track[0] = (track[0][0] + direction[0] * speed) % disp_surface.get_width(), (track[0][1] + direction[1] * speed) % disp_surface.get_height() 
    
        body = update_body(track, 20)

        if pygame.sprite.spritecollideany(foods.sprite, snakegroup):
            foods.empty()
            foods.add(food())
            last_part = snakegroup.sprites()[-1] #store the last sprite in the sprite group

            snakegroup.add(snake(last_part.x_pos, last_part.y_pos)) #on collision, add a new snake using x/y of the last sprite in the group
            speed = speed

    else:
        disp_surface.fill((64,64,64))
        welcome_message(disp_surface, game_font, body)

    pygame.display.update() #update all the surfaces on each frame
    clock.tick(120) #fps
