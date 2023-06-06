import pygame
import random

COLORS = [
    (255, 17, 0), #red
    (255, 140, 0), #orange
    (240, 233, 43), #yellow
    (58, 189, 98), #green
    (61, 161, 219), #blue
    (165, 113, 235), #purple
    (219, 70, 137) #pink
]

class Figure:
    x = 0
    y = 0

    # List of shapes - numbers represetn the positions in a 4x4 matrix
    FIGURES = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
        ]


    def __init__(self,x,y):
        self.x = x
        self.y = y
        # Generates random figure
        self.type = random.randint(0, len(self.FIGURES) - 1)
        # Generates a random color
        self.color = random.randint(1, len(COLORS)-1)
        self.rotation = 0

    
    def image(self):
        return self.FIGURES[self.type][self.rotation]
    
    # Rotates the figure
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.FIGURES[self.type])


class Tetris:
    
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    # Creates a new figure
    def new_figure(self):
        self.figure = Figure(3,0)


    # Check if current figure is intersecting with something on the field
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                # Check each cell in the matrix of current figure to see if it is
                # out of bounds or touching game field
                if i*4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width-1 or \
                            j+ self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        # Check if field is not empty
                        intersection = True
        return intersection
    
    # Break lines when color matches all the way through
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2


    # Goes down until it reaches bottom or fixed figure
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # Move down
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()


    # If figure reaches the bottom, "lock in place" or freeze
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

   

    # Move sideways: remember previous position, change coordinates, check if intersection                        
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    # Rotate
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation



# Pygame stuff
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up screen
size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")


done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False


# Loop until user exits
while not done:
    # Create new figure
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0


    # Start game
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    # Handle different events in game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # If a key is pressed
        if event.type == pygame.KEYDOWN:
            # Up key - rotate
            if event.key == pygame.K_UP:
                game.rotate()
            # Down key
            if event.key == pygame.K_DOWN:
                pressing_down = True
            # Left key
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            # Right key
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            # Space
            if event.key == pygame.K_SPACE:
                game.go_space()
            # Escape 
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    # Check if key is no longer being pressed
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False
    
    # Set background color to white
    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, COLORS[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, COLORS[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])


    # Set fonts
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)

    # Display game score
    text = font.render("Score: " + str(game.score), True, BLACK)

    # Display "Game Over"
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))
    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()

    # Run the clock
    clock.tick(fps)

# Exit game
pygame.quit()
