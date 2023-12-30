import pygame
import random
import os 


pygame.init()
pygame.mixer.init()

screen_width = 1280
screen_height = 720

# creating window
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("snake")

# loading images

bgimg = pygame.image.load("assets\\background2.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
stimg = pygame.image.load("assets\\home.jpeg")
stimg = pygame.transform.scale(stimg,(screen_width,screen_height)).convert_alpha()
ovimg = pygame.image.load("assets\\over.jpeg")
ovimg = pygame.transform.scale(ovimg,(screen_width,screen_height)).convert_alpha()


font = pygame.font.SysFont(None,55 )
clock = pygame.time.Clock()


# color

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
board_color = (0,230,118)
yellow = (255,234,0)
orange = (230,74,25)
liblue = (41, 121, 255)


# screen score
def screen_score(text, color , x , y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])


# plotting snake from coordinates in snakelist
def plot_snake(gameWindow,color,snake_list, snake_size):
    '''Plots snake'''
    for x, y in snake_list:
        pygame.draw.rect(gameWindow,color,[x , y, snake_size, snake_size])

def start():
    '''Home screen'''
    exit_game = False
    while not exit_game:
        gameWindow.fill(liblue)
        gameWindow.blit(stimg,(0,0))
        screen_score("Snake Game",orange,300,200)
        screen_score("Press UP key to Play",orange,250,250)
       
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            gameloop()  
        pygame.display.update()
        clock.tick(60)   
           
   
# game loop
def gameloop():
    pygame.mixer.music.load("assets\\bg.mp3")
    pygame.mixer.music.play(-1)
    
    # variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 20
    velocity_x = 0
    velocity_y = 0
    food_size = 20
    init_velocity = 5
    score = 0
    food_x = random.randint(20,screen_width//2)
    food_y = random.randint(20,screen_height//2)
    snake_list = []
    snake_length = 1
    FPS = 60
    # check if highscore
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

           
         
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(yellow)
            gameWindow.blit(ovimg,(0,0))
            screen_score("Game Over!Press enter to play again",red,140,250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()  
            
        else:       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
            snake_x+=velocity_x
            snake_y+=velocity_y  
            if (abs(snake_x - food_x ) < 12) and (abs(snake_y - food_y) < 12 ):
                score+=10
                score_sound = pygame.mixer.Sound("assets\\score.mp3")
                
                score_sound.play()
               
                food_x = random.randint(20,screen_width//2)
                food_y = random.randint(20,screen_height//2)
                snake_length+=5
                
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(board_color)
            gameWindow.blit(bgimg, (0, 0))
            screen_score("Score:"+str(score),yellow,20,20)
            screen_score( "Hiscore:"+ str(highscore) ,yellow,650,20)
            pygame.draw.rect(gameWindow,red,[food_x, food_y, food_size, food_size])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snake_length:
                del snake_list[0]
            
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("assets\\gameover.wav")
                pygame.mixer.music.play()
            if snake_x < 0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True 
                pygame.mixer.music.load("assets\\gameover.wav")  
                pygame.mixer.music.play(1)
                
            plot_snake(gameWindow,blue , snake_list, snake_size)
            # pygame.draw.rect(gameWindow,blue,[snake_x, snake_y, snake_size, snake_size])
            # pygame.draw.circle(gameWindow, blue, (snake_x, snake_y), snake_size)
            # pygame.draw.circle(gameWindow,red,(food_x, food_y),food_size)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()    
start()