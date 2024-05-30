import pygame
import random
import os
import time 
import sys
from enum import Enum
pygame.mixer.init()

pygame.init()


WHITE = (255,255,255)
RED = (255, 0 , 0)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
BROWN = (186, 74, 0)
GREEN = (46, 204, 113)
DEEP_GREEN = (11, 83, 69)
BLUE = (46, 134, 193)
LIGHT_BLUE = (174, 214, 241)
height = 750
width = 1200
border= 50
clock = pygame.time.Clock()
#create window
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("snake game")

font = pygame.font.SysFont(None,50)


def resource_path(relative_path):
    """Get absolute path to resourse, works for dev and for pyinstaller"""
    try:
        # pyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

def screen_score(text,color,x,y):
    screen_text = font.render(text,True,color)
    screen.blit(screen_text,[x,y])
    
def text_on(text,color,font_size = 70):
    gameover_font = pygame.font.Font(None,font_size)
    gameover_font.set_italic(True)
    screen_text = gameover_font.render(text,True,color)
    text_rect = screen_text.get_rect()
    text_rect.center = (width // 2, height // 2)
    screen.blit(screen_text,text_rect)
    
def normal_text(text,color,y,font_size = 30):
    normal_font = pygame.font.Font(None,font_size)
    screen_text = normal_font.render(text,True,color)
    text_rect = screen_text.get_rect()
    text_rect.center = (width // 2, (height // 2)+y)
    screen.blit(screen_text,text_rect)
    
        
def plot_snake(screen,color,snake_list,snake_size):
    for x,y in snake_list:
        pygame.draw.rect(screen,color,[x,y,snake_size,snake_size])

def print_keys_pressed():
    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Iterate over all keys
    for key, state in enumerate(keys):
        if state:
            # Print the name of the key
            key_name = pygame.key.name(key)
            print("Key pressed:", key_name)

  
#create game loops
def gameloop(): 
    #game specific variables
    exit_game = False
    game_over = False
    snake_x = 60
    snake_y = 60
    snake_size = 20
    food_size = 12
    big_food_size = 18
    fps = 60
    velocity_x = 0
    velocity_y = 0
    velocity = 5
    snake_list = []
    snake_length = 1
    score = 0
    food_time = 1
    food_x = random.randint(2*border+30,width-(2*border)-30)
    food_y = random.randint(2*border+30,height-(2*border)-30)
    
    big_food_x = random.randint(2*border+36,width-(2*border)-36)
    big_food_y = random.randint(2*border+36,height-(2*border)-36)
    with open((resource_path(r"resource\highscore.txt")),'r') as f:
        high_score = f.read()
    
    while not exit_game:
        if game_over:
            with open((resource_path(r"resource\highscore.txt")),'w') as f:
                f.write(str(high_score))
    
            screen.fill(YELLOW)
            text_on("Game over!",RED)
            normal_text("Enter to play the game",RED,85)
            normal_text("Your Score : "+str(score),BLACK,120)
            normal_text('High Score : '+str(high_score),BLACK,160)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome_screen()
        else: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                      
                # controls 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        velocity_x = velocity
                        velocity_y = 0  
                    if event.key == pygame.K_a:
                        velocity_x = -velocity
                        velocity_y = 0
                    if event.key == pygame.K_w:
                        velocity_y = -velocity
                        velocity_x = 0
                    if event.key == pygame.K_s:
                        velocity_y = velocity
                        velocity_x = 0
                print_keys_pressed()
            #snake and food position || snake eat food             
            snake_x = snake_x+velocity_x
            snake_y = snake_y+velocity_y
            if abs(snake_x - food_x)<22 and abs(snake_y-food_y)<22:
                score = score+10
                food_time = food_time+1
                # print(food_time)
                pygame.mixer.music.load(resource_path(r"resource\normal_point_collect.mp3"))
                pygame.mixer.music.play()
                if score>int(high_score):
                    high_score = score
                # print(score*10) 
                food_x = random.randint(border+30,width-(2*border)-30)
                food_y = random.randint(border+30,height-(2*border)-30)
                snake_length += 5 
               
            #screen    
            screen.fill(BROWN)
            pygame.draw.rect(screen,LIGHT_BLUE,[border,border,width-2*border,height-2*border])
            screen_score("Score : "+str(score)+"   "+"High Score : "+str(high_score),BLACK,10,10)
            
            pygame.draw.circle(screen,RED,[food_x,food_y],food_size)    
            if (food_time%5==0):
                pygame.draw.circle(screen,YELLOW,[big_food_x,big_food_y],big_food_size)
                
                if abs(snake_x - big_food_x)<18 and abs(snake_y-big_food_y)<18:
                    score = score+15
                    food_time = food_time+1
                    pygame.mixer.music.load(resource_path(r"resource\bonus_point.mp3"))
                    pygame.mixer.music.play()
                    if score>int(high_score):
                        high_score = score
                    # print(score*10) 
                    big_food_x = random.randint(2*border+36,width-(2*border)-36)
                    big_food_y = random.randint(2*border+36,height-(2*border)-36)
                    snake_length += 10
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            
            if len(snake_list)>snake_length:
                del snake_list[0]
            
            #collision 
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load(resource_path(r"resource\game_over.mp3"))
                pygame.mixer.music.play()
            if snake_x<border or snake_x >width-(border+20) or snake_y<border or snake_y>height-(border+20):
                # print("Game orver ")
                game_over = True
                pygame.mixer.music.load(resource_path(r"resourcegame_over.mp3"))
                pygame.mixer.music.play()
            plot_snake(screen,DEEP_GREEN,snake_list,snake_size)
        # snake = pygame.draw.rect(screen,BLACK,[snake_x,snake_y,snake_size,snake_size])
        pygame.display.update() #TO SEE UPDATED DISPLAY
        clock.tick(fps)
    
    pygame.quit()
    
def welcome_screen():
    exit_game = False
    while not exit_game:
        pygame.mixer.music.load(resource_path(r"resource\start_sound.mp3"))
        pygame.mixer.music.play()
        screen.fill(BLUE)
        pygame.draw.rect(screen, GREEN,[70,70,width-140,height-140])
        text_on("Wellcome to Snake game",YELLOW,80)
        normal_text("Press Enter to play the game ",YELLOW,60,40)
        normal_text("A simple snake game by Hyperstrom",BLACK,280,25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit_game = True 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()       
        pygame.display.update()
        clock.tick(60)
welcome_screen()
