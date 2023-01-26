import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((800, 600))

# Set the title of the window
pygame.display.set_caption("Space Invaders")

# Load the player image
player_image = pygame.image.load("player.png")
# Scale the player image
scaled_player_image = pygame.transform.scale(player_image, (30, 30))

# Set the player's starting position
player_x = 400
player_y = 550

# Load the enemy image
enemy_image = pygame.image.load("enemy.png")
# Scale the enemy image
scaled_enemy_image = pygame.transform.scale(enemy_image, (30, 30))

# Set the enemy's starting position
enemy_x = 50
enemy_y = 50

# Set the speed at which the enemy moves
enemy_speed_x = 0.5
enemy_speed_y = 0.5

# Set the speed at which the player moves
player_speed = 2

# Load the bullet image
bullet_image = pygame.image.load("bullet.png")
# Scale the bullet image
scaled_bullet_image = pygame.transform.scale(bullet_image, (30, 20))

# Create a variable to control the game loop
running = True

# Create a variable to keep track of the score
score = 0

# Create a variable to keep track of the player's lives
lives = 3

# Create a variable to keep track of the player's bullets
bullets = []

# Create a variable to keep track of the game over condition
game_over = False

# Create a variable to keep track of the bullet firing rate
bullet_firing_rate = 0

# Create a variable to keep track of the level
level = 1

# Create a variable to keep track of the number of enemies
num_enemies = 1

# Create a list to store the enemies
enemies = []
enemies.append([scaled_enemy_image, enemy_x, enemy_y])

pre_level_score=0

# Start the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Move the player based on user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_x > 30:
            player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        if player_x < 770:
            player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_firing_rate == 0:
        bullet = scaled_bullet_image.copy()
        bullet_rect = bullet.get_rect(center=(player_x, player_y))
        bullets.append((bullet, bullet_rect))
        bullet_firing_rate = 10
    if bullet_firing_rate > 0:
        bullet_firing_rate -= 1

    # Move the enemies
    for enemy in enemies:
        enemy[1] += enemy_speed_x
        enemy[2] += enemy_speed_y
        # Check if the enemy has hit the edge of the screen
        if enemy[1] > 750 or enemy[1] < 0:
            enemy_speed_x = -enemy_speed_x
        if enemy[2] > 550:
            lives -= 1
            enemies.remove(enemy)
            if len(enemies) == 0:
                for i in range(num_enemies):
                    enemy_x = random.randint(0, 750)
                    enemy_y = 50
                    enemies.append([scaled_enemy_image, enemy_x, enemy_y])

    # Move the player's bullets
    for bullet in bullets:
        bullet[1].y -= 5
        if bullet[1].y < 0:
            bullets.remove(bullet)

    # Check for collisions between the player's bullets and the enemies
    for bullet in bullets:
        for enemy in enemies:
            if bullet[1].colliderect(pygame.Rect(enemy[1], enemy[2], 30, 30)):
                #bullets.remove(bullet)
                score += 1
                enemies.remove(enemy)
                if len(enemies) == 0:
                    for i in range(num_enemies):
                        enemy_x = random.randint(0, 750)
                        enemy_y = 50
                        enemies.append([scaled_enemy_image, enemy_x, enemy_y])

    screen.fill((0, 0, 0))
    # check for level up condition
    
    if  score % 100 == 0 and score != 0 and score != pre_level_score :
        pre_level_score = score
        level += 1
        num_enemies += 1
        for i in range(num_enemies):
            enemy_x = random.randint(0, 750)
            enemy_y = 50
            enemies.append([scaled_enemy_image, enemy_x, enemy_y])

    # Clear the screen
    screen.fill((0, 0, 0))        
    # Draw the player
    screen.blit(scaled_player_image, (player_x, player_y))

    # Draw the enemies
    for enemy in enemies:
        screen.blit(enemy[0], (enemy[1], enemy[2]))

    # Draw the player's bullets
    for bullet in bullets:
        screen.blit(bullet[0], bullet[1])

    # Draw the score
    score_text = "Score: {}".format(score)
    score_label = pygame.font.Font(None, 20).render(score_text,1, (255, 255, 255))
    screen.blit(score_label, (650, 10))

    # Draw the lives
    lives_text = "Lives: {}".format(lives)
    lives_label = pygame.font.Font(None, 20).render(lives_text, 1, (255, 255, 255))
    screen.blit(lives_label, (10, 10))

    # Draw the level
    level_text = "Level: {}".format(level)
    level_label = pygame.font.Font(None, 20).render(level_text, 1, (255, 255, 255))
    screen.blit(level_label, (350, 10))

    # Check for collisions between the enemies and the player
    for enemy in enemies:
        if pygame.Rect(enemy[1], enemy[2], 30, 30).colliderect(pygame.Rect(player_x, player_y, 30, 30)):
            lives -= 1
            enemies.remove(enemy)
            if len(enemies) == 0:
                for i in range(num_enemies):
                    enemy_x = random.randint(0, 750)
                    enemy_y = 50
                    enemies.append([scaled_enemy_image, enemy_x, enemy_y])
            if lives <= 0:
                game_over = True
                running = False

    # Check if the player has no lives left
    if lives <= 0:
        game_over = True
        running = False

    

    # Update the display
    pygame.display.update()

    #If the game is over, display the game over screen
    if game_over:
        game_over_text = "Game Over"
        game_over_label = pygame.font.Font(None, 50).render(game_over_text, 1, (255, 255, 255))
        screen.blit(game_over_label, (350, 300))
        pygame.display.update()
        pygame.time.wait(3000)

        #Clean up before exiting
        pygame.quit()

