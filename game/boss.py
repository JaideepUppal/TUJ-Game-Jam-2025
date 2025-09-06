import pygame
import random
from .constants import *

class Boss:
    def __init__(self, image=None, stomp_image=None, rock_image=None, projectile_image=None, worm_image=None):
        self.x = SCREEN_WIDTH // 2 - BOSS_WIDTH // 2
        self.y = 50
        self.width = BOSS_WIDTH - 20
        self.height = BOSS_HEIGHT - 20
        self.image = image
        self.stomp_image = stomp_image
        self.rock_image = rock_image
        self.projectile_image = projectile_image
        self.worm_image = worm_image
        
        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.is_transitioning = False
        self.transition_timer = 0
        
        self.attack_timer = 0
        self.stomp_cooldown = 0
        self.worm_cooldown = 0
        self.rock_cooldown = 0
        self.stomp_active = False
        self.stomp_duration = 0
    
    def update(self, dt, current_phase, loop_count):
        result = None
        
        # Handle phase transition
        if self.is_transitioning:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.is_transitioning = False
                self.max_health = BOSS_HEALTH * (1 + (current_phase - 1) * 0.5) * (1 + loop_count * 0.25)
                self.health = self.max_health
            return None
        
        # Update attack timers
        self.attack_timer -= dt
        self.stomp_cooldown -= dt
        self.worm_cooldown -= dt
        self.rock_cooldown -= dt
        
        # Handle stomp effect
        if self.stomp_active:
            self.stomp_duration -= dt
            if self.stomp_duration <= 0:
                self.stomp_active = False
        
        # Check if it's time for an attack
        if self.attack_timer <= 0:
            # Reset attack timer
            self.attack_timer = random.uniform(0.5, 1.5) / (1 + current_phase * 0.1 + loop_count * 0.05)
            
            # Choose an attack based on the current phase
            attack_choice = random.random()
            
            if current_phase >= 4 and self.rock_cooldown <= 0 and attack_choice < 0.15:
                # Rock attack in phase 4+
                result = "rock"
                self.rock_cooldown = ROCK_COOLDOWN
            elif current_phase >= 3 and self.worm_cooldown <= 0 and attack_choice < 0.3:
                # Worm attack in phase 3+
                result = "worm"
                self.worm_cooldown = WORM_COOLDOWN
            elif current_phase >= 2 and self.stomp_cooldown <= 0 and attack_choice < 0.5:
                # Stomp attack in phase 2+
                result = "stomp"
                self.stomp_active = True
                self.stomp_duration = STOMP_DURATION
                self.stomp_cooldown = STOMP_COOLDOWN
            else:
                # Basic projectile attack
                result = "projectile"
        
        return result
    
    def take_damage(self):
        if not self.is_transitioning:
            self.health -= 1
    
    def start_transition(self):
        self.is_transitioning = True
        self.transition_timer = TRANSITION_DURATION
    
    def draw(self, screen):
        # Draw boss
        if self.image:
            if self.is_transitioning:
                # Flicker during transition
                if pygame.time.get_ticks() % 200 < 100:
                    screen.blit(self.image, (self.x, self.y))
            else:
                screen.blit(self.image, (self.x, self.y))
        else:
            # Draw a basic shape if no image is provided
            if self.is_transitioning:
                # Flicker during transition
                if pygame.time.get_ticks() % 200 < 100:
                    pygame.draw.rect(screen, (255, 0, 0), 
                                    pygame.Rect(self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, (255, 0, 0), 
                                pygame.Rect(self.x, self.y, self.width, self.height))
        
        # Draw stomp effect
        if self.stomp_active:
            if self.stomp_image:
                screen.blit(self.stomp_image, 
                           (self.x + self.width // 2 - STOMP_RADIUS, 
                            self.y + self.height // 2 - STOMP_RADIUS))
            else:
                # Draw circle for stomp area
                pygame.draw.circle(screen, (255, 100, 100, 128), 
                                  (int(self.x + self.width // 2), int(self.y + self.height // 2)), 
                                  STOMP_RADIUS, 2)
    
    def draw_health_bar(self, screen, current_phase, loop_count):
        # Draw health bar background
        pygame.draw.rect(screen, (100, 100, 100), 
                        pygame.Rect(50, 20, SCREEN_WIDTH - 100, 20))
        
        # Draw current health
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, (255, 50, 50), 
                        pygame.Rect(50, 20, (SCREEN_WIDTH - 100) * health_percent, 20))
        
        # Draw phase indicators
        total_phases = 4 + loop_count
        for i in range(total_phases):
            phase_pos = 50 + (SCREEN_WIDTH - 100) * ((i + 1) / total_phases) - 10
            if i < current_phase - 1 or (self.health <= 0 and i == current_phase - 1):
                # Completed phase
                pygame.draw.circle(screen, (50, 255, 50), (int(phase_pos), 30), 5)
            else:
                # Upcoming phase
                pygame.draw.circle(screen, (255, 255, 255), (int(phase_pos), 30), 5)
    
    def reset(self):
        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.is_transitioning = False
        self.transition_timer = 0
        self.attack_timer = 1.0
        self.stomp_cooldown = 0
        self.worm_cooldown = 0
        self.rock_cooldown = 0
        self.stomp_active = False
        self.stomp_duration = 0
