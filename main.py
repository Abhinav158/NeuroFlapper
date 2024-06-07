# Import all necessary packages
import pygame 
import neat 
import time 
import os 
import random 

# Declare constants 
WIN_WIDTH = 600
WIN_HEIGHT = 800

# Grab the images and scale it up to 2x the original size
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png"))),
]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))

BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))

BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))

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
        
def draw_window(win, bird): 
    # Draw the bird on top of the background image 
    win.blit(BACKGROUND_IMAGE, (0,0))
    
    bird.draw(win)
    pygame.display.update()

# Run the main loop of the game  
def main():
    # Define the window 
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Define the bird along with its starting position
    bird = Bird(200, 200)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)        
    pygame.quit()
    quit()

main()
    