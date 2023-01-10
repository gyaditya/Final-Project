import pygame

class Player:
    def __init__(self, x, y, vx, vy, color, controls):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.controls = controls
        self.width = 50
        self.height = 50
        self.lives = 3
        self.bullets = []
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
    
    def shoot(self):
        self.bullets.append(pygame.Rect(self.x, self.y, 5, 5))
    
    def check_bounds(self, screen_height):
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > screen_height / 2:
            self.y = screen_height / 2 - self.height
    
    def update_bullets(self):
        for bullet in self.bullets:
            bullet.y += 10 if self.controls == "arrows" else -10
        self.bullets = [b for b in self.bullets if b.y > 0 and b.y < 600]
    
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

# Set the font for displaying the player's lives
font = pygame.font.Font(None, 36)

# Set the width of the line separating the two halves of the screen
line_width = 5

# Set the colors for the players and the line
player1_color = (0, 0, 255)
player2_color = (255, 0, 0)
line_color = (0, 0, 0)

# Set the game clock
clock = pygame.time.Clock()

# Create the players
player1 = Player(50, 50, 0, 0, player1_color, "wasd")
player2 = Player(750, 50, 0, 0, player2_color, "arrows")

# Set the game loop flag
running = True

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        # Quit the game when the close button is clicked
        if event.type == pygame.QUIT:
            running = False
        
        # Handle player 1 movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.vy = -5
            elif event.key == pygame.K_s:
                player1.vy = 5
            elif event.key == pygame.K_a:
                player1.vx = -5
            elif event.key == pygame.K_d:
                player1.vx = 5
            elif event.key == pygame.K_SPACE:
                player1.shoot()
        
        # Handle player 2 movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2.vy = -5
            elif event.key == pygame.K_DOWN:
                player2.vy = 5
            elif event.key == pygame.K_LEFT:
                player2.vx = -5
            elif event.key == pygame.K_RIGHT:
                player2.vx = 5
            elif event.key == pygame.K_k:
                player2.shoot()
        
        # Stop player 1's movement when the keys are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1.vy = 0
            elif event.key == pygame.K_s:
                player1.vy = 0
            elif event.key == pygame.K_a:
                player1.vx = 0
            elif event.key == pygame.K_d:
                player1.vx = 0
        
        # Stop player 2's movement when the keys are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2.vy = 0
            elif event.key == pygame.K_DOWN:
                player2.vy = 0
            elif event.key == pygame.K_LEFT:
                player2.vx = 0
            elif event.key == pygame.K_RIGHT:
                player2.vx = 0
    
    # Update the positions of the players
    player1.move()
    player2.move()

    # Keep the players within their half of the screen
    player1.check_bounds(window_size[1])
    player2.check_bounds(window_size[1])

    # Update the positions of the bullets
    player1.update_bullets()
    player2.update_bullets()

    # Check for collisions between bullets and players
    player1.check_collisions(player2)
    player2.check_collisions(player1)

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
