import pygame
from .constants import *

class Player:
    def __init__(self, image=None):
        self.x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        self.y = SCREEN_HEIGHT - 150
        self.width = PLAYER_SIZE - 20
        self.height = PLAYER_SIZE - 20
        self.vel_x = 0
        self.vel_y = 0
        self.speed = PLAYER_SPEED
        self.image = image
        self.dash_cooldown = 0
        self.dash_duration = 0
        self.is_dashing = False
        self.dash_direction = (0, 0)
        self.stunned = False
        self.stun_timer = 0
        self.gotRose = False

    def update(self, dt, keys, current_phase, arrRoses):
        if current_phase == 2:
            self.gotRose = False
        
        if keys[pygame.K_e] and current_phase == 3:
            if (abs(self.x - arrRoses[0]) <= 30) and (abs(self.y - arrRoses[1]) <= 30):
                self.stun()
            if (abs(self.x - arrRoses[2]) <= 30) and (abs(self.y - arrRoses[3]) <= 30):
                self.stun()
            if (abs(self.x - arrRoses[4]) <= 30) and (abs(self.y - arrRoses[5]) <= 30):
                self.gotRose = True
        
        # Handle stun
        if self.stunned:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.stunned = False
            return
        
        # Reset velocity
        self.vel_x = 0
        self.vel_y = 0
        
        # Handle dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        
        # Handle dash duration
        if self.is_dashing:
            self.dash_duration -= dt
            if self.dash_duration <= 0:
                self.is_dashing = False
            else:
                # Continue dash movement
                self.vel_x = self.dash_direction[0] * DASH_SPEED
                self.vel_y = self.dash_direction[1] * DASH_SPEED
        else:
            # Normal movement
            if self.gotRose:
                if keys[pygame.K_s]:
                    self.vel_y = -self.speed
                if keys[pygame.K_w]:
                    self.vel_y = self.speed
                if keys[pygame.K_d]:
                    self.vel_x = -self.speed
                if keys[pygame.K_a]:
                    self.vel_x = self.speed
            else:
                if keys[pygame.K_w]:
                    self.vel_y = -self.speed
                if keys[pygame.K_s]:
                    self.vel_y = self.speed
                if keys[pygame.K_a]:
                    self.vel_x = -self.speed
                if keys[pygame.K_d]:
                    self.vel_x = self.speed
                
            
            # Dash
            if keys[pygame.K_LSHIFT] and self.dash_cooldown <= 0:
                dash_x, dash_y = 0, 0
                
                if keys[pygame.K_w]:
                    dash_y = -1
                if keys[pygame.K_s]:
                    dash_y = 1
                if keys[pygame.K_a]:
                    dash_x = -1
                if keys[pygame.K_d]:
                    dash_x = 1
                
                # Normalize direction
                if dash_x != 0 or dash_y != 0:
                    magnitude = (dash_x ** 2 + dash_y ** 2) ** 0.5
                    dash_x /= magnitude
                    dash_y /= magnitude
                    
                    self.dash_direction = (dash_x, dash_y)
                    self.is_dashing = True
                    self.dash_duration = DASH_DURATION
                    self.dash_cooldown = DASH_COOLDOWN
                    
                    # Apply dash velocity
                    self.vel_x = dash_x * DASH_SPEED
                    self.vel_y = dash_y * DASH_SPEED
        
        # Update position
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Keep player in bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Draw a basic shape if no image is provided
            if self.is_dashing:
                color = (0, 255, 255)  # Cyan for dashing
            elif self.stunned:
                color = (255, 255, 0)  # Yellow for stunned
            else:
                color = (0, 200, 255)  # Blue for normal
            
            pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.width, self.height))
    
    def stun(self):
        self.stunned = True
        self.stun_timer = STUN_DURATION
        self.is_dashing = False
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
        self.y = SCREEN_HEIGHT - 150
        self.vel_x = 0
        self.vel_y = 0
        self.dash_cooldown = 0
        self.dash_duration = 0
        self.is_dashing = False
        self.stunned = False
        self.stun_timer = 0
        self.gotRose = False
