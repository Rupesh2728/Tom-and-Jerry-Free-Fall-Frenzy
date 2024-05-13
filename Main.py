import pygame
import random

pygame.init()
pygame.mixer.init()  #Useful for adding sound and music
WIDTH = 500
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('assets/Terserah.ttf', 42)
font = pygame.font.Font('assets/Terserah.ttf', 24)   # Setting up Font and Font Size
pygame.display.set_caption('Tom and Jerry\'s Free Fall Frenzy')  # Set title for window
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Make the window for the game
bg = (135, 206, 235)    #Background-color

# Clouds
clouds_coordinates = [[300, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
cloud_images = []
for i in range(1, 4):
    img = pygame.image.load(f'assets/clouds/cloud{i}.png')
    cloud_images.append(img)


#cheese variables
cheese_img = pygame.transform.scale(pygame.image.load('assets/cheese.png'), (70, 50))
cheese_coordinates = [[100, 670, 1]]



# Game Over Variable
game_over = False

#Player variables
player_x = 240
player_y = 40
jerry = pygame.transform.scale(pygame.image.load('assets/jerry.png'), (110, 170))
direction = -1    # Falling down ---> -1 , Bouncing Back Up ---> +1
y_speed = 0
x_speed = 3
x_direction = 0
gravity = 0.2


# Enemies
tom = pygame.transform.scale(pygame.image.load('assets/tom_to_left.png'), (220, 220))
enemies_coordinates = [[-234, random.randint(400, HEIGHT - 100), -1]]

# Score Variables
score = 0
total_distance = 0
file = open('High_Score.txt', 'r')
read = file.readlines()
first_high_score = int(read[0])
high_score = first_high_score

# Sounds and Music
bounce = pygame.mixer.Sound('assets/bounce2.wav')
end_sound = pygame.mixer.Sound('assets/game_over1.wav')


# Clouds creation function
def draw_clouds(cloud_coordinates_list, images):
    platforms = []
    for j in range(len(cloud_coordinates_list)):
        image = images[cloud_coordinates_list[j][2] - 1]
        platform = pygame.rect.Rect((cloud_coordinates_list[j][0] + 5, cloud_coordinates_list[j][1] + 30), (130, 10))
        screen.blit(image, (cloud_coordinates_list[j][0], cloud_coordinates_list[j][1]))
        # pygame.draw.rect(screen, 'gray', platform)
        platforms.append(platform)

    return platforms


def draw_cheese(cheese_coordinates_list, cheese_image):
    cheese_platforms_list = []
    for j in range(len(cheese_coordinates_list)):
            image = cheese_image
            platform = pygame.rect.Rect((cheese_coordinates_list[j][0] + 20, cheese_coordinates_list[j][1] + 10),(40, 10))
            screen.blit(image, (cheese_coordinates_list[j][0], cheese_coordinates_list[j][1]))
            # pygame.draw.rect(screen, 'gray', platform)
            cheese_platforms_list.append(platform)

    return cheese_platforms_list

# Player creation function
def draw_player(x_pos, y_pos, player_img, direc):
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos + 30, y_pos + 120), (50, 10))
    # pygame.draw.rect(screen, 'green', player_rect, 3)
    return player_rect

# Placing Enemies
def draw_enemies(enemies_list, tom_img):
    enemy_rects = []
    for j in range(len(enemies_list)):
        enemy_rect = pygame.rect.Rect((enemies_list[j][0] + 10, enemies_list[j][1] + 80), (200, 90))
        # pygame.draw.rect(screen, 'orange', enemy_rect, 3)
        enemy_rects.append(enemy_rect)
        if enemies_list[j][2] == -1:
            screen.blit(tom_img, (enemies_list[j][0], enemies_list[j][1]))
        elif enemies_list[j][2] == 1:
            screen.blit(pygame.transform.flip(tom_img, 1, 0), (enemies_list[j][0], enemies_list[j][1]))
    return enemy_rects


def move_enemies(enemy_list, current_score):
    enemy_speed = 2 + current_score//15
    for j in range(len(enemy_list)):
        if enemy_list[j][2] == 1:
            if enemy_list[j][0] < WIDTH:
                enemy_list[j][0] += enemy_speed
            else:
                enemy_list[j][2] = -1

        elif enemy_list[j][2] == -1:
            if enemy_list[j][0] > -235:
                enemy_list[j][0] -= enemy_speed
            else:
                enemy_list[j][2] = 1

        if enemy_list[j][1] < -100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)

    return enemy_list


def update_objects(cloud_list, play_y, enemies_list, cheese_list):
    lowest_cloud = 0
    update_speed = 10
    if play_y > 200:    # This is done to move the clouds up...
        play_y -= update_speed   # Until the play_y > 200 , the screen dont move up

        for j in range(len(enemies_list)):
            enemies_list[j][1] -= update_speed

        # This for loop is used to find the bottom most cloud coordinates
        for j in range(len(cloud_list)):
            cloud_list[j][1] -= update_speed
            lowest_cloud = max(lowest_cloud, cloud_list[j][1])

        for j in range(len(cheese_list)):  # this loop is to move the cheeses up...
            cheese_list[j][1] -= update_speed

        if lowest_cloud < 750:  # Screen Height is 800...then creates new clouds
            num_clouds = random.randint(1, 2)  # Randomly generating 1 or 2 clouds, that should be as we go down
            if num_clouds == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
                cheese_list.append([(x_pos + 200) % WIDTH, y_pos - 50, 1])
            else:  # The 2 clouds should not overlap...So each cloud is seperated
                x_pos = random.randint(0, WIDTH // 2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])  # Appending the new cloud coordinates to the existing list

                x_pos2 = random.randint(WIDTH // 2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type2 = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
                cloud_list.append([x_pos2, y_pos2, cloud_type2]) # Appending the new cloud's coordinates to the existing list

                cheese_list.append([random.randint(x_pos + 20, x_pos2 - 20), random.randint(HEIGHT + 200, HEIGHT + 300), 1])

    return play_y, cloud_list, enemies_list, cheese_list  # Returning the clouds coordinates and updated play_y value
    # We are directly updating the Clouds coordinates list...So no use of returning cloud_list


# Intro page variable and Sound
pygame.mixer.music.load('assets/Intro.mp3')
pygame.mixer.music.play()
Intro = pygame.transform.scale(pygame.image.load('assets/LandingImg.png'), (450, 500))
bgImg = pygame.transform.scale(pygame.image.load('assets/background.jpg'), (WIDTH, HEIGHT))
title = pygame.transform.scale(pygame.image.load('assets/title.png'), (400, 120))
heading = pygame.transform.scale(pygame.image.load('assets/heading.png'), (500, 190))
pygame.mixer.music.set_volume(0.7)

start_page = True
run = True
while start_page:   # Intro Page loop
    screen.fill(bg)  # Fill the display screen with bg
    timer.tick(fps)
    # screen.blit(bgImg, (0, 0))
    screen.blit(heading, (0, 10))
    screen.blit(Intro, (0, 50))
    screen.blit(title, (60, 550))
    end_text = font.render('Press "SPACEBAR" to enter the game', True, 'black')
    screen.blit(end_text, (50, HEIGHT - 120))
    for event in pygame.event.get():    # When Exit is pressed(Red color Cross)...While
        if event.type == pygame.QUIT:   # loop terminates
            start_page = False
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_page = False

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('assets/Intro.mp3')
        pygame.mixer.music.play()

    pygame.display.flip()


pygame.mixer.music.load('assets/tom-e-jerry-1.mp3')
pygame.mixer.music.play()   # Music Playing while playing the game
pygame.mixer.music.set_volume(0.4)
Cheese = 0
old_pos_y = None

while run:  # Game page loop
    screen.fill(bg)  # Fill the display screen with bg
    timer.tick(fps)

    cloud_platforms = draw_clouds(clouds_coordinates, cloud_images)  # Gets back the cloud_platform coordinates
    cheese_platforms = draw_cheese(cheese_coordinates, cheese_img)
    player = draw_player(player_x, player_y, jerry, direction)  # Gets back the player_rect
    enemy_boxes = draw_enemies(enemies_coordinates, tom)
    enemies = move_enemies(enemies_coordinates, score)
    player_y, clouds, enemies, cheeses = update_objects(clouds_coordinates, player_y, enemies_coordinates, cheese_coordinates)

    if game_over:  # Enemy should disappear when tom and jerry touch...i.e. catch
        game_over_img = pygame.transform.scale(pygame.image.load('assets/gameover.png'), (500, 130))
        end_text = huge_font.render('Jerry\'s Free Fall Frenzy!!!', True, 'black')
        end_text2 = font.render('Press "Enter" to Restart...', True, 'black')
        screen.blit(game_over_img, (0, 130))
        screen.blit(end_text2, (100, 250))
        player_y = -300
        if Cheese // 10 >= 1:   # If cheese > 10 then...jerry gets a life
            life_img = pygame.transform.scale(pygame.image.load('assets/life.png'), (400, 100))
            end_text3 = font.render('Jerry! Escape from Tom!!!,You have a life!!', True, 'black')
            end_text4 = font.render('Press "Tab" to Continue...', True, 'black')
            screen.blit(life_img, (40, 500))
            screen.blit(end_text4, (100, 600))

    # Checking whether the jerry rectangle is colliding with any platform rectangle
    for i in range(len(cloud_platforms)):
        if direction == -1 and player.colliderect(cloud_platforms[i]):  # If it is in Free-Fall then change the direction of motion to upwards
            y_speed *= -1
            if y_speed > -2:  # It will keep on collide until we move jerry using left and right arrows
                y_speed = -2  # If this condition is not there then after sometime it will come down from platform without pressing any key
            bounce.play()  # Plays the bounce sound when jerry bounces

    remove_cheeses = []
    for i in range(len(cheese_platforms)):
        if direction == -1 and player.colliderect(cheese_platforms[i]):
            Cheese += 1
            remove_cheeses.append(i)

    updated_cheese_coordinates = []
    for i in range(len(cheese_coordinates)):
        if i in remove_cheeses:
            continue
        updated_cheese_coordinates.append(cheese_coordinates[i])

    cheese_coordinates = updated_cheese_coordinates
    if y_speed < 10:
        y_speed += gravity

    # Since it is a free fall game....gravity will pull down
    player_y += y_speed

    if y_speed < 0:
        direction = 1
    else:
        direction = -1

    # Based on key-press it will change
    player_x += x_speed * x_direction

    if player_x > WIDTH:
        player_x = -30

    elif player_x < -50:
        player_x = WIDTH - 20

    for i in range(len(enemy_boxes)):
        if player.colliderect(enemy_boxes[i]) and not game_over:
            game_over = True  # If jerry collides then the game is over
            old_pos_y = player_y
            if score > first_high_score:
                file = open('High_Score.txt', 'w')
                write_score = str(score)
                file.write(write_score)
                file.close()
                first_high_score = score
            end_sound.play()
+
    # Calculating the scores
    if not game_over:
        total_distance += y_speed
        score = round(total_distance / 100)
    score_text = font.render(f'Score : {score}', True, 'black')
    screen.blit(score_text, (10, HEIGHT - 90))

    Cheese_text = font.render(f'Cheese : {Cheese}', True, 'black')
    screen.blit(Cheese_text, (WIDTH - 150, HEIGHT - 60))

    if score > high_score:
        high_score = score
    score_text2 = font.render(f'High Score : {high_score}', True, 'black')
    screen.blit(score_text2, (10, HEIGHT - 60))

    # Exit Handler
    for event in pygame.event.get():    # When Exit is pressed(Red color Cross)...While
        if event.type == pygame.QUIT:   # loop terminates
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_direction = -1

            elif event.key == pygame.K_RIGHT:
                x_direction = 1

            if event.key == pygame.K_RETURN and game_over:  # Pressing Enter key
                game_over = False
                player_x = 240
                player_y = 40
                direction = -1
                y_speed = 0
                x_direction = 0
                score = 0
                Cheese = 0
                total_distance = 0
                enemies_coordinates = [[-234, random.randint(400, HEIGHT - 100), 1]]
                clouds_coordinates = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
                pygame.mixer.music.play()

            if event.key == pygame.K_TAB and Cheese // 10 >= 1 and game_over:  # when game over..if cheese > 10, jerry gets a life by pressing "TAB" key
                player_y = old_pos_y - 200
                game_over = False
                Cheese = Cheese - 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('assets/tom-e-jerry-1.mp3')
            pygame.mixer.music.play()

    pygame.display.flip()

pygame.quit()
