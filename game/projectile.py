import pygame
from .constants import *

class Projectile:
    def __init__(self, x, y, vel_x, vel_y, image=None, is_worm=False, is_rock=False):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.width = PROJECTILE_SIZE
        self.height = PROJECTILE_SIZE
        
        if is_worm:
            self.height = PROJECTILE_SIZE * 2
            self.color = (255, 100, 0)
        elif is_rock:
            self.width = ROCK_SIZE
            self.height = ROCK_SIZE
            self.color = (150, 150, 150)
        else:
            self.color = (255, 255, 0) if vel_y > 0 else (0, 255, 0)
        
        self.image = image
        self.is_worm = is_worm
        self.is_rock = is_rock
    
    def update(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, 
                            pygame.Rect(self.x, self.y, self.width, self.height))
    
    def collides_with(self, entity):
        # Simple rectangle collision detection
        return (self.x < entity.x + entity.width and
                self.x + self.width > entity.x and
                self.y < entity.y + entity.height and
                self.y + self.height > entity.y)
