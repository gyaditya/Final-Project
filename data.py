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
        self.bullets = []
        self.controls = controls
        self.health = 10
        self.shooting = False

    def move(self, screen_width, screen_height, line_width):
        self.x += self.vx
        self.y += self.vy
        half_screen = screen_width/2
        if self.color == player1_color:
            if self.x < 0:
                self.x = 0
            elif self.x + self.width > half_screen:
                self.x = half_screen - self.width
        else:
            if self.x < half_screen:
                self.x = half_screen
            elif self.x + self.width > half_screen + line_width:
                self.x = half_screen + line_width - self.width
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > screen_height:
            self.y = screen_height - self.height


    def shoot(self):
        if self.color == player1_color:
            self.bullets.append(pygame.Rect(self.x + self.width, self.y + self.height/2, 5, 5))
        else:
            self.bullets.append(pygame.Rect(self.x, self.y + self.height/2, 5, 5))


    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x += 10 if self.color == player1_color else -10
        self.bullets = [b for b in self.bullets if b.x >= 0 and b.x <= screen_width ]

    def check_collisions(self, other_player):
        for bullet in self.bullets:
            if bullet.colliderect(other_player.x, other_player.y, other_player.width, other_player.height):
                other_player.health -= 1
                self.bullets.remove(bullet)
                if other_player.health <= 0:
                    font = pygame.font.Font(None, 30)
                    if self.color == (255, 0, 0):
                        winner = "Player 1"
                        color = self.color
                    elif self.color == (0, 0, 255):
                        winner = "Player 2"
                        color = self.color

                    winner_text = font.render(winner + " won!", True, (color))
                    screen.blit(winner_text, (350, 300))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    pygame.quit()
                    quit()

# Initialize pygame
pygame.init()

# Set the window size
window_size = (800, 600)

# Create the window
screen = pygame.display.set_mode(window_size)
screen_width, screen_height = screen.get_size()
# Set the title of the window
pygame.display.set_caption("Two Player Game")

# Define the colors
player1_color = (255, 0, 0)
player2_color = (0, 0, 255)
line_color = (255, 255, 255)

# Define the line width
line_width = 5

#Create the clock
clock = pygame.time.Clock()

# Create the players
player1 = Player(50, 250, player1_color, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_SPACE})
player2 = Player(750, 250, player2_color, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_k})

# Create the font
font = pygame.font.Font(None, 30)

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == player1.controls["up"]:
                player1.vy = -5
            elif event.key == player1.controls["down"]:
                player1.vy = 5
            elif event.key == player1.controls["left"]:
                player1.vx = -5
            elif event.key == player1.controls["right"]:
                player1.vx = 5
            elif event.key == player1.controls["shoot"] and not player1.shooting:
                player1.shoot()
                player1.shooting = True
            elif event.key == player2.controls["up"]:
                player2.vy = -5
            elif event.key == player2.controls["down"]:
                player2.vy = 5
            elif event.key == player2.controls["left"]:
                player2.vx = -5
            elif event.key == player2.controls["right"]:
                player2.vx = 5
            elif event.key == player2.controls["shoot"] and not player2.shooting:
                player2.shoot()
                player2.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key in (player1.controls["up"], player1.controls["down"]):
                player1.vy = 0
            elif event.key in (player1.controls["left"], player1.controls["right"]):
                player1.vx = 0
            elif event.key == player1.controls["shoot"]:
                player1.shooting = False
            elif event.key in (player2.controls["up"], player2.controls["down"]):
                player2.vy = 0
            elif event.key in (player2.controls["left"], player2.controls["right"]):
                player2.vx = 0
            elif event.key == player2.controls["shoot"]:
                player2.shooting = False

    player1.move(screen_width, window_size[1], screen_width / 2)
    player2.move(screen_width, window_size[1], screen_width / 2)
    player1.update_bullets()
    player2.update_bullets()
    player1.check_collisions(player2)
    player2.check_collisions(player1)
    
    # Draw the game elements
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, line_color, (window_size[0] / 2, 0), (window_size[0] / 2, window_size[1]), line_width)
    pygame.draw.rect(screen, player1.color, (player1.x, player1.y, player1.width, player1.height))
    pygame.draw.rect(screen, player2.color, (player2.x, player2.y, player2.width, player2.height))
    for bullet in player1.bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)
    for bullet in player2.bullets:
        pygame.draw.rect(screen, (0, 0, 255), bullet)
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()




