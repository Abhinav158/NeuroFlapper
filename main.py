# Import all necessary packages
import neat.population
import pygame 
import neat 
import time 
import os 
import random 

pygame.font.init()

# Declare constants 
WIN_WIDTH = 550
WIN_HEIGHT = 800

GEN = -1

# Grab the images and scale it up to 2x the original size
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png"))),
]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))

BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))

BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))

SCORE_FONT = pygame.font.Font('LuckiestGuy-Regular.ttf', 48)


class Bird:
    IMAGES = BIRD_IMAGES

    # How much the bird will tilt when we move the bird up and down
    MAX_ROTATION = 25

    # How much will we rotate on each frame or everytime we move the bird
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    # Represent the starting position of the bird
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Bird is flat (Facing horizontally) at the start of every game
        self.tilt = 0

        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]
    
    def jump(self):

        # Give a negative velocity since (0, 0) is on the top left of the screen and we are moving upwards
        self.velocity = -10.5

        # Keep track of when the last jump was performed
        self.tick_count = 0

        # Keep track of where the bird is jumping from
        self.height = self.y
    
    def move(self):

        # Indicate that a movement has happened
        self.tick_count += 1

        # Results in an arc motion for the bird
        displacement = self.velocity*self.tick_count + 1.5*self.tick_count**2

        # We do not want to go very fast - Setup the Terminal Velocity
        if displacement >= 16: 
            displacement = 16
        
        # If you want a higher or lower jump, play with the displacement decrement
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        # If we are moving upwards or above the point from where we jumped from
        if displacement < 0 or self.y < self.height + 50: 
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        # Nose-dive the bird to the ground while it is going down
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, win):
        self.image_count += 1

        # Decide what image we should show based on the current image count 
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]
        elif self.image_count == self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0
        
        if self.tilt <= -80:
            self.image = self.IMAGES[1]
            # Should not feel like a frame is being skipped
            self.image_count = self.ANIMATION_TIME*2
        
        # Rotate the image about the center (Reference: https://stackoverflow.com/questions/67362677/how-do-i-make-an-image-which-rotates-without-distorting-in-pygame)
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center) 
        win.blit(rotated_image, new_rectangle.topleft)  

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe: 

    # Space in between the pipes 
    GAP = 200
    # Move the pipe backwards to make it seem like the bird is moving forward while playing
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        # Grab the images for the top and bottom pipes so flip one upside down
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        # Collision purposes - Has the bird passed this pipe yet?
        self.passed = False

        # Function to define how tall the top and bottom pipes are  
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        # Change the x position to the left according to the velocity 
        self.x -= self.VELOCITY
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()

        # Create a mask from the top and bottom pipe 
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Check if there is a collision in these masks 
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)
        if top_point or bottom_point: 
            return True
    
        # If None in both, then no collision 
        return False

class Base: 
    # This should be the same as the pipe so everything moves uniformly 
    VELOCITY = 5

    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))

def draw_window(win, birds, pipes, base, score, gen): 
    
    # Draw everything on top of the background image 
    win.blit(BACKGROUND_IMAGE, (0,0))

    for pipe in pipes: 
        pipe.draw(win)
    
    text = SCORE_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = SCORE_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds: 
        bird.draw(win)
    pygame.display.update()

# Run the main loop of the game  
def eval_genomes(genomes, config):

    global GEN 
    GEN += 1

    # Define the window 
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Put the base at the Bottom of the screen
    base = Base(730)

    # Throw the pipes on the screen
    pipes = [Pipe(600)]

    # Define the birds along with their starting position
    birds = []

    nets = []

    ge = [] 

    for _, g in genomes: 
        # Setup a bird object and its neural network 
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        # Set the initial fitness to 0
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()

    score = 0 

    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        # Which pipe do we look at to determine how the bird moves?
        pipe_index = 0
        
        if len(birds) > 0:
            # If we have passed the pipes, then look at the second pipe on the screen
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        
        # No birds left 
        else:
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()

        # List of removed pipes as they cross off the screen
        add_pipe = False
        rem = []

        for pipe in pipes:

            for x, bird in enumerate(birds): 
                # Check if any bird has had a collision with a pipe 
                if pipe.collide(bird):
                    # If a bird hits a pipe, reduce its fitness score 
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                
                # Check if the bird has crossed the pipe 
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            # Remove the pipe when it moves off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe: 

            # Increase the score once you cross a pipe 
            score += 1
            # Give the birds 5 fitness for every pipe passed 
            for g in ge: 
                g.fitness += 5
            # Add a new pipe for the bird to encounter 
            pipes.append(Pipe(600))
        
        # Remove the pipes that go off the screen
        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(birds): 

            # If the bird hits the ground, then you lose 
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        draw_window(win, birds, pipes, base, score, GEN)        



def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction, 
        neat.DefaultSpeciesSet, 
        neat.DefaultStagnation, 
        config_path
    )

    # Create a population
    population = neat.Population(config)

    # Grab detailed section about each population's performance
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Set the fitness function
    winner = population.run(eval_genomes, 50)



if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "neat-config.txt")
    run(config_path)
    