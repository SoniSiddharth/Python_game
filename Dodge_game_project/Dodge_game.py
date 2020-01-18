# DO NOT RUN THIS FILE TO START THE GAME, RUN THE "restart.py" FILE TO ENJOY THE GAME
# If you will run this file then game will run only for once and will not restart
# Reference: the main concept and code of the basic game has been taken from the https://www.youtube.com/watch?v=-8n91btt5d8 
# it is from line 129 to 173 and 193 to 211
# Reference: https://www.pygame.org/docs/ 
import pygame,sys,json,random,pygame.mixer,os  

pygame.init()

WIDTH = 900
HEIGHT = 700

# defining the different colors
RED = (255,0,0)
BACKGROUND_COLOR = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
DARKBLUE = (0,0,139)

# position(pos) and sizes of player and obstacles
# "obs" is used in place of obstacle

player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

obs_size = 50
obs_pos = [random.randint(0,WIDTH-obs_size), 0]
obs_list = [obs_pos]
bonus_size = 40
bonus_pos = [random.randint(0,WIDTH-bonus_size), 0]
bonus_list = [bonus_pos]
flag_mode=False

# defining speed of the obstacles and the bonus bag
SPEED = 10
coin_speed = 10

# following is the command for the background window of the game 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0
highscore = 0
Hscore_list = []
clock = pygame.time.Clock()
# creating a text file to store the scores and use it for getting the highscore
hsfile = open('hs.txt','r')
Hscore_list = json.loads(hsfile.read()) # loading the text file using json module
hsfile.close()

#following codes are loading the music and images used in this game
coinimg  = pygame.image.load("images/coin.png")
highscore = max(Hscore_list)
spikeimage=pygame.image.load("images/spikes.png")
bgimage = pygame.image.load("images/bgimage1.jpg")
backgroundmusic = pygame.mixer.Sound("sound/bgmusic.wav")
century_sound = pygame.mixer.Sound('sound/Rise01.wav')
end_sound = pygame.mixer.Sound('sound/DeathFlash.wav')
b_sound = pygame.mixer.Sound("sound/bonussound.wav")

mode = 1
# the background image changes and a sound occurs at the time of completing a half century with the following function
def checking_score(score):
    global flag_mode
    if score%50==0 and score != 0 and ( not flag_mode):
        global bgimage
        global mode 
        century_sound.play()
        mode += 1 
        if mode == 4:
            mode = 1
        bgimage=pygame.image.load("images/bgimage"+str(mode)+".png")
        flag_mode=True
    # the following code is to make sure that the background image do not fluctuate between the score 50 and 51 
    # because the game involves the working of the frames
    if 1<score%50:
        flag_mode=False
          
# to initialize the font
myFont = pygame.font.SysFont("monospace",35)

# defining a function for the building different levels or we can say increasing the difficulty
def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    else:
        SPEED = score/4 +1
    return SPEED

# to create the bonus bag 
def draw_bonus(bonus_list):
    for bonus_pos in bonus_list:
        coinimg.set_colorkey((255,255,255))
        screen.blit(coinimg,(bonus_pos[0], bonus_pos[1]))

# the following functions are to create and drop the bonus bag randomly 
def drop_bonus(bonus_list):
    delay = random.random()
    if len(bonus_list) < 1 and delay < 0.1:
        x_pos = random.randint(0,WIDTH - bonus_size)
        y_pos = 0
        bonus_list.append([x_pos, y_pos])

def update_bonus_positions(bonus_list):
    for idx, bonus_pos in enumerate(bonus_list):
        if bonus_pos[1] >= 0 and bonus_pos[1] < HEIGHT:
            bonus_pos[1] += coin_speed
        else:
            bonus_list.pop(idx)
            
# how to collect t to he bonus? 
# the player simply have to go and collect it and the bag will disappear with a sound
def getting_bonus(player_pos, bonus_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    b_x = bonus_pos[0]
    b_y = bonus_pos[1]

    if (b_x >= p_x and b_x < (p_x + player_size)) or (p_x >= b_x and p_x < (b_x + bonus_size)):
        if (b_y >= p_y and b_y < (p_y + player_size)) or (p_y >= b_y and p_y < (b_y + bonus_size)):
            return True
    return False

def getting_bonus2(bonus_list, player_pos):
    for bonus_pos in bonus_list:
        if getting_bonus(bonus_pos, player_pos):
            bonus_list.pop(bonus_list.index(bonus_pos))
            b_sound.play()
            return True
    return False

# drawing the shape of obstacle
def draw_obstacles(obs_list):
    for obs_pos in obs_list:
        screen.blit(spikeimage,(obs_pos[0], obs_pos[1]))

#for having multiple obstacles in the path
def drop_obstacles(obs_list):
    delay = random.random()
    if len(obs_list) < 10 and delay < 0.1:
        x_pos = random.randint(0,WIDTH - obs_size)
        y_pos = 0
        obs_list.append([x_pos, y_pos])

# updating the obstacle's position
def update_obs_positions(obs_list, score):
    for idx, obs_pos in enumerate(obs_list):
        if obs_pos[1] >= 0 and obs_pos[1] < HEIGHT:
            obs_pos[1] += SPEED
        else:
            obs_list.pop(idx)
            score +=1
    return score

def detect_collision(player_pos, obs_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    o_x = obs_pos[0]
    o_y = obs_pos[1]

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obs_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obs_size)):
            return True
    return False

# condition for the collision of obstacle with the player using the above function detect_collision
def collision_check(obs_list, player_pos, highscore, Hscore_list):
    for obs_pos in obs_list:
        if detect_collision(obs_pos, player_pos):
            Hscore_list.append(score)
            pygame.mixer.Channel(0).fadeout(500)
            pygame.mixer.Channel(1).play(end_sound,0)
            highscore = max(Hscore_list)
            return True 
    return False

# implementing the initial background image and the player image
def Start():
    BackImg=pygame.image.load("images/startimg.png")
    screen.blit(BackImg,(0,0))
    pygame.display.flip()
    pygame.time.delay(3000)

def images():
    boyimage=pygame.image.load("images/boy.png")
    boyimage.set_colorkey((255,255,255))
    screen.blit(boyimage,(player_pos[0], player_pos[1]) )

# main game loop
quit=False
while not quit:

    Start()
    pygame.mixer.Channel(0).play(backgroundmusic)
    while not game_over:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                os._exit(0)

            # defining the working of keys (left and right) as an event
            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]

                if event.key == pygame.K_LEFT and x>=player_size:   
                    x -= player_size
                if event.key == pygame.K_RIGHT and x<WIDTH-player_size: 
                    x += player_size

                player_pos = [x,y]

        # calling the functions and placing the score and high score on the screen     
        screen.blit(bgimage,(0,0))
        drop_bonus(bonus_list)
        drop_obstacles(obs_list)
        update_bonus_positions(bonus_list)
        getting_bonus(player_pos, bonus_pos)
        score = update_obs_positions(obs_list, score)
        SPEED = set_level(score, SPEED)
        
        text = "SCORE: " + str(score)
        myFont.set_bold(True)
        label = myFont.render(text, 1, DARKBLUE)
        screen.blit(label, (WIDTH-250, HEIGHT-40))

        hscore = "HIGH SCORE: " + str(highscore)
        myFont.set_bold(True)
        label2 = myFont.render(hscore, 1, DARKBLUE)
        screen.blit(label2, (WIDTH-400, HEIGHT-640))
        checking_score(score)
        
        # increment in the score by 5 points as the player catches the bonus bag
        if getting_bonus2(bonus_list, player_pos):
            score += 5 
        
        # defining how the game ends by calling the function
        if collision_check(obs_list, player_pos, highscore, Hscore_list):
            game_over = True
            myFont.set_bold(True)
            label3 = myFont.render("Press space to restart", 1, (0,0,0))
            screen.blit(label3, (WIDTH/2 - 200, HEIGHT/2))
            pygame.display.update()
            break
        
        draw_bonus(bonus_list)
        draw_obstacles(obs_list)
        images()
        clock.tick(30)
        
        # to update the display window 
        pygame.display.update()
    
    hsfile = open('hs.txt', 'w')
    hsfile.write(json.dumps(Hscore_list))
    hsfile.close()

    quit=True


