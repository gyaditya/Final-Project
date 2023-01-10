import pygame

class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.width = 50
        self.height = 50
        self.lives = 3
        self.bullets = []

    def move(self, screen_width, screen_height):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen_width/2:
            self.x = screen_width/2 - self.width
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > screen_height:
            self.y = screen_height - self.height

    def shoot(self):
        self.bullets.append(pygame.Rect(self.x + self.width/2, self.y + self.height/2, 5, 5))

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x += 10
        self.bullets = [b for b in self.bullets if b.x > 0 and b.x < 800]

    def check_collisions(self, other_player):
        for bullet in self.bullets:
            if bullet.colliderect(other_player.x, other_player.y, other_player.width, other_player.height):
                other_player.lives -= 1
                self.bullets.remove(bullet)

# Initialize pygame
pygame.init()

# Set the window size
window_size = (800, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Two Player Game")

# Define the colors
player1_color = (255, 0, 0)
player2_color = (0, 0, 255)
line_color = (0, 0, 0)

# Define the line width
line_width = 5

#Create the clock
clock = pygame.time.Clock()

# Create the players
player1 = Player(50, 250, player1_color, "wasd")
player2 = Player(750, 250, player2_color, "arrows")

# Create the font
font = pygame.font.Font(None, 30)

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            #player 1 event handling
            if event.key == pygame.K_w:
                player1.vy = -5
            if event.key == pygame.K_s:
                player1.vy = 5
            if event.key == pygame.K_a:
                player1.vx = -5
            if event.key == pygame.K_d:
                player1.vx = 5
            if event.key == pygame.K_SPACE:
                if not player1.shooting:
                    player1.shoot()
                    player1.shooting = True
            #player 2 event handling
            if event.key == pygame.K_UP:
                player2.vy = -5
            if event.key == pygame.K_DOWN:
                player2.vy = 5
            if event.key == pygame.K_LEFT:
                player2.vx = -5
            if event.key == pygame.K_RIGHT:
                player2.vx = 5
            if event.key == pygame.K_k:
                if not player2.shooting:
                    player2.shoot()
                    player2.shooting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1.vy = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player1.vx = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2.vy = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player2.vx = 0
            if event.key == pygame.K_k:
                player2.shooting = False    

    # Update the positions of the players
    player1.move(window_size[0], window_size[1])
    player2.move(window_size[0], window_size[1])

    # Update the positions of the bullets
    player1.update_bullets()
    player2.update_bullets()

    # Check for collisions
    player1.check_collisions(player2)
    player2.check_collisions(player1)

    if player1.lives == 0 or player2.lives == 0:
        running = False
        if player1.lives == 0:
            end_message = "Player 2 wins!"
        else:
            end_message = "Player 1 wins!"
        end_text = font.render(end_message, True, (0, 0, 0))
        screen.blit(end_text, (window_size[0]/2 - end_text.get_width()/2, window_size[1]/2 - end_text.get_height()/2))
        pygame.display.flip()
        pygame.time.wait(3000)
    else:
        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the line separating the two halves of the screen
        pygame.draw.line(screen, line_color, (window_size[0] / 2, 0), (window_size[0] / 2, window_size[1]), line_width)

        # Draw the players
        pygame.draw.rect(screen, player1.color, (player1.x, player1.y, player1.width, player1.height))
        pygame.draw.rect(screen, player2.color, (player2.x, player2.y, player2.width, player2.height))

        # Draw the bullets
        for bullet in player1.bullets:
            pygame.draw.rect(screen, player1.color, bullet)
        for bullet in player2.bullets:
            pygame.draw.rect(screen, player2.color, bullet)

        # Display the player's lives
        player1_lives_text = font.render(str(player1.lives), True, player1.color)
        player2_lives_text = font.render(str(player2.lives), True, player2.color)
        screen.blit(player1_lives_text, (10, 10))
        screen.blit(player2_lives_text, (window_size[0] - 10 - player2_lives_text.get_width(), 10))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

# Quit pygame
pygame.quit()


