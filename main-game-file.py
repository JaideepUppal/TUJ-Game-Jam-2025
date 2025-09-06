import pygame
import sys
import os
from game.player import Player
from game.boss import Boss
from game.projectile import Projectile
from game.constants import *
from game.game_state import GameState
import random
import math
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for the music

# Get the screen info to determine the full screen size
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
print(screen_info)

# Game display dimensions (fixed at 800x600)
game_width, game_height = 800, 600

# Create a full screen display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Centered Game Display")
pygame.mixer.music.load("intro_music.mp3")
pygame.mixer.music.play(loops=0, start=18.0)  # Start at 10 seconds

# Create a surface for the game content (720x720)
game_surface = pygame.Surface((game_width, game_height))

# Calculate the position to center the game display
game_x = (screen_width - game_width) // 2
game_y = (screen_height - game_height) // 2

# Create a clock for controlling frame rate
clock = pygame.time.Clock()
    

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Function to fade text
def fade_text(text, hold_time=1.5, fade_speed=5):
    #import the font 
    font = pygame.font.Font("PokemonGb-RAeo.ttf", 20)

    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill(BLACK)

    # Ensure text is a list (if it's a single string, convert it to a list with one element)
    if isinstance(text, str):
        text = [text] 

    # Render each line manually
    text_surfaces = []
    for i, line in enumerate(text):
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(15, 20 + i * (font.get_height() + 20)))
        text_surfaces.append((text_surface, text_rect))

    # Fade in
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(255 - alpha)
        screen.fill(BLACK)
        for surface, rect in text_surfaces:
            screen.blit(surface, rect)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)
        
    # Hold text
    time.sleep(hold_time)

    # Fade out
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.fill(BLACK)
        for surface, rect in text_surfaces:
            screen.blit(surface, rect)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

# Left border text lines
left_text_lines = [
    "WASD to Move", 
    "K to Shoot",
    "ESC to Escape"
]

# Right border text lines (similar format)
right_text_lines = [
    "Wassup",
    "Fam",
    "Bomboclaat"
]

# Render all text surfaces
font = pygame.font.Font("PokemonGb-RAeo.ttf", 15)
left_text_surfaces = [font.render(line, True, "white") for line in left_text_lines]
right_text_surfaces = [font.render(line, True, "white") for line in right_text_lines]

# Calculate starting position (centered vertically)
total_text_height = max(
    sum(text.get_height() for text in left_text_surfaces) + 20 * (len(left_text_lines) - 1),
    sum(text.get_height() for text in right_text_surfaces) + 20 * (len(right_text_lines) - 1)
)

start_y = screen_height // 2 - total_text_height // 2



# Main Game starts here

#Game display dimensions (fixed at 720x720)
game_width, game_height = 800, 600

#Create a surface for the game content (720x720)
game_surface = pygame.Surface((game_width, game_height))

#Calculate the position to center the game display
game_x = (1920 - game_width) // 2
game_y = (1080 - game_height) // 2


#start running the intro screen
running = True

#Intro Loop
while running:
    
    screen.fill(BLACK)
    
    fade_text(["","","","","","","   This is our amazing Game!"], hold_time=2) # 51 Characters is the max length for one line we can go for 


    fade_text(["Welcome, brave adventurer!",
    "You came to fight the mighty boss, ",
    "a creature so terrifying and powerful ",
    "that you are certain you will never ",
    "beat it. But do not worry, you are ",
    "going to try anyway! It's going to ",
    "be easy! Just keep battling ",
    "and fighting; victory will be yours, ","",
    "eventually... maybe... The boss is ",
    "unstoppable, or is he?? Get ready ",
    "to enter a world where victory ",
    "is impossible... but you will ",
    "have fun failing!"], hold_time=15)

    fade_text(["Instructions:", "",
    "1. Move: Use W A S D ",
    "   to move around",
    "   SHIFT to dash", "",
    "2. Shoot: Press K to fire your bow ","",
    "3. Not matter how it may seem. ",
    "   Do NOT give up and show love.",
    "   We worked hard on this","",
    "4. Pay VERY close attention ",
    "   to those instructions"], hold_time=10)

    pygame.mixer.music.stop()  # Stop the music
    running = False  # Exit after intro


running = True
# Actual game starts here 

#add music here
pygame.mixer.music.load("main_music.mp3")
pygame.mixer.music.play(loops=-1, start=3.0)  # Start at 3 seconds

def load_image(path, scale=None):
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

def main():
    # Initialize game state
    game_state = GameState()
    
    # Load assets
    try:
        background_img = load_image("assets/images/background.webp", (SCREEN_WIDTH, SCREEN_HEIGHT))
        rose_img = load_image("assets/images/rose.webp", (30, 40))
        roseBW_img = load_image("assets/images/roseBW.png", (30, 40))
        lava_img = load_image("assets/images/lava.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT))
        player_img = load_image("assets/images/player.png", (PLAYER_SIZE, PLAYER_SIZE))
        boss_img = load_image("assets/images/boss.png", (BOSS_WIDTH, BOSS_HEIGHT))
        projectile_img = load_image("assets/images/projectile.png", (PROJECTILE_SIZE, PROJECTILE_SIZE))
        boss_projectile_img = load_image("assets/images/boss_projectile.png", (PROJECTILE_SIZE, PROJECTILE_SIZE))
        stomp_img = load_image("assets/images/stomp.png", (STOMP_RADIUS * 2, STOMP_RADIUS * 2))
        rock_img = load_image("assets/images/rock.png", (ROCK_SIZE, ROCK_SIZE))
        worm_img = load_image("assets/images/worm.png", (PROJECTILE_SIZE * 1.5, PROJECTILE_SIZE * 3.76))
    except pygame.error:
        print("Warning: Could not load some images. Using default shapes instead.")
        background_img = None
        lava_img = None
        rose_img = None
        player_img = None
        boss_img = None
        projectile_img = None
        boss_projectile_img = None
        stomp_img = None
        rock_img = None
        worm_img = None
    
    # Load fonts
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 72)
    
    # Game objects
    player = Player(player_img)
    boss = Boss(boss_img, stomp_img, rock_img, boss_projectile_img, worm_img)
    
    player_projectiles = []
    boss_projectiles = []
    lava_worms = []
    rocks = []
    
    lava_height = 0
    screen_overlay = None
    overlay_alpha = 0

    arrRoses = [random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500)]
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state.current_state == "playing":
                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_e:
                    #     if (abs(player.x - arrRoses[0]) <= 10) and (abs(player.y - arrRoses[1]) <= 10):
                    #         player.stun()
                    #     if (abs(player.x - arrRoses[2]) <= 10) and (abs(player.y - arrRoses[3]) <= 10):
                    #         player.stun()
                    #     if (abs(player.x - arrRoses[4]) <= 10) and (abs(player.y - arrRoses[5]) <= 10):
                    #         player.stun()
                    
                    if event.key == pygame.K_k and not player.stunned:
                        # Create player projectile
                        if projectile_img:
                            proj = Projectile(player.x + player.width // 2 - PROJECTILE_SIZE // 2, 
                                              player.y, 0, -PROJECTILE_SPEED, projectile_img)
                        else:
                            proj = Projectile(player.x + player.width // 2 - PROJECTILE_SIZE // 2, 
                                              player.y, 0, -PROJECTILE_SPEED)
                        player_projectiles.append(proj)
            
            elif game_state.current_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state.start_game()
                        player.reset()
                        boss.reset()
                        player_projectiles.clear()
                        boss_projectiles.clear()
                        lava_worms.clear()
                        rocks.clear()
                        lava_height = 0
            
            elif game_state.current_state in ["win", "lose"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state.change_state("menu")
        
        # Update game state
        if game_state.current_state == "playing":
            # Update player
            keys = pygame.key.get_pressed()
            player.update(dt, keys, game_state.current_phase, arrRoses)
            
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_e:
            #         print("hello")
            #         if (abs(player.x - arrRoses[0]) <= 10) and (abs(player.y - arrRoses[1]) <= 10):
            #             player.stun()
            #         if (abs(player.x - arrRoses[2]) <= 10) and (abs(player.y - arrRoses[3]) <= 10):
            #             player.stun()
            #         if (abs(player.x - arrRoses[4]) <= 10) and (abs(player.y - arrRoses[5]) <= 10):
            #             player.stun()

            # Boss actions
            boss_action = boss.update(dt, game_state.current_phase, game_state.loop_count)
            
            if boss_action == "projectile" and not boss.is_transitioning:
                # Create boss projectile
                if boss_projectile_img:
                    proj = Projectile(boss.x + boss.width // 2, boss.y + boss.height, 
                                     (player.x - boss.x) / 1, PROJECTILE_SPEED, boss_projectile_img)
                else:
                    proj = Projectile(boss.x + boss.width // 2, boss.y + boss.height, 
                                     (player.x - boss.x) / 1, PROJECTILE_SPEED)
                boss_projectiles.append(proj)
            
            elif boss_action == "stomp" and game_state.current_phase >= 2:
                # Check if player is in stomp radius
                dx = (player.x + player.width / 2) - (boss.x + boss.width / 2)
                dy = (player.y + player.height / 2) - (boss.y + boss.height / 2)
                distance = (dx ** 2 + dy ** 2) ** 0.5
                
                if distance < STOMP_RADIUS:
                    player.stun()
            
            elif boss_action == "worm" and game_state.current_phase >= 3:
                # Create lava worm
                worm_x = pygame.time.get_ticks() % SCREEN_WIDTH
                if worm_img:
                    worm = Projectile(worm_x, SCREEN_HEIGHT - lava_height, 0, -PROJECTILE_SPEED * 1.5, worm_img, is_worm=True)
                else:
                    worm = Projectile(worm_x, SCREEN_HEIGHT - lava_height, 0, -PROJECTILE_SPEED * 1.5, is_worm=True)
                lava_worms.append(worm)
            
            elif boss_action == "rock" and game_state.current_phase >= 4:
                # Create blinding rock
                if rock_img:
                    rock = Projectile(boss.x + boss.width // 2, boss.y + boss.height, 
                                     (player.x - boss.x) / 1, PROJECTILE_SPEED * 0.5, rock_img, is_rock=True)
                else:
                    rock = Projectile(boss.x + boss.width // 2, boss.y + boss.height, 
                                     (player.x - boss.x) / 1, PROJECTILE_SPEED * 0.5, is_rock=True)
                rocks.append(rock)
            
            # Update projectiles
            for proj in player_projectiles[:]:
                proj.update(dt)
                if proj.y < 0:
                    player_projectiles.remove(proj)
                elif proj.collides_with(boss) and not boss.is_transitioning:
                    player_projectiles.remove(proj)
                    boss.take_damage()
                    
                    # Check if boss phase should change
                    if boss.health <= 0:
                        boss.start_transition()
                        game_state.advance_phase()
                        
                        # Reset lava if moving to phase 4
                        if game_state.current_phase == 4:
                            lava_height = 600
                            arrRoses = [random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500), random.randrange(100, 500)]
                        if game_state.current_phase == 3:
                            lava_height = 0
            
            for proj in boss_projectiles[:]:
                proj.update(dt)
                if proj.y > SCREEN_HEIGHT or proj.x < 0 or proj.x > SCREEN_WIDTH:
                    boss_projectiles.remove(proj)
                elif proj.collides_with(player):
                    if game_state.current_phase == 4 and lava_height > 0 and proj.y > SCREEN_HEIGHT - lava_height:
                        # In phase 4, projectiles in lava don't hurt player
                        pass
                    else:
                        game_state.change_state("lose")
            
            for worm in lava_worms[:]:
                worm.update(dt)
                if worm.y < 0:
                    lava_worms.remove(worm)
                elif worm.collides_with(player):
                    if game_state.current_phase == 4:
                        # In phase 4, worms don't hurt player
                        pass
                    else:
                        game_state.change_state("lose")
            
            for rock in rocks[:]:
                rock.update(dt)
                if rock.y > SCREEN_HEIGHT or rock.x < 0 or rock.x > SCREEN_WIDTH:
                    rocks.remove(rock)
                elif rock.collides_with(player):
                    rocks.remove(rock)
                    # Apply screen overlay effect
                    screen_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    screen_overlay.fill((0, 0, 0))
                    overlay_alpha = 500  # Start at ~80% opacity
            
            if ((player.gotRose) and (abs(player.x - boss.x) <= 50) and (abs(player.y - boss.y) <= 50)):
                game_state.change_state("win")

            # Update lava height
            if game_state.current_phase >= 3:
                if game_state.current_phase == 3:
                    lava_height += LAVA_RISE_SPEED * dt
            
                
                # Check if player is touching lava
                if game_state.current_phase == 4:
                    lava_height -= LAVA_RISE_SPEED * dt
                    # In phase 4, lava is safe, everything else kills
                    player_in_lava = player.y + player.height > SCREEN_HEIGHT - lava_height
                    if not player_in_lava and lava_height > 0:
                        game_state.change_state("lose")
                    
                    # Check secret win condition
                    if (player.x + player.width > SCREEN_WIDTH - 50 and 
                        player.y + player.height > SCREEN_HEIGHT - 50 and 
                        game_state.current_phase == 4):
                        game_state.change_state("win")
                    
                else:
                    # Normal phases - lava kills
                    if player.y + player.height > SCREEN_HEIGHT - lava_height:
                        game_state.change_state("lose")
            
            # Update screen overlay effect
            if overlay_alpha > 0:
                overlay_alpha -= 150 * dt  # Fade out over approximately 1 second
                if overlay_alpha < 0:
                    overlay_alpha = 0
                    screen_overlay = None
        
        # Draw everything
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill((30, 30, 30))
        
        if game_state.current_state == "playing":
            # Draw boss
            boss.draw(screen)
            
            # Draw projectiles
            for proj in player_projectiles:
                proj.draw(screen)
            
            for proj in boss_projectiles:
                proj.draw(screen)
            
            for worm in lava_worms:
                worm.draw(screen)
            
            for rock in rocks:
                rock.draw(screen)
            
            # Draw player
            player.draw(screen)
            
            if game_state.current_phase != 2:
                screen.blit(rose_img, (arrRoses[0], arrRoses[1]))
                screen.blit(rose_img, (arrRoses[2], arrRoses[3]))
                screen.blit(rose_img, (arrRoses[4], arrRoses[5]))
            
            if player.gotRose:
                screen.blit(roseBW_img, (arrRoses[4], arrRoses[5]))

            # Draw lava
            if game_state.current_phase >= 3 and lava_height > 0:
                if lava_img:
                    lava_rect = pygame.Rect(0, SCREEN_HEIGHT - lava_height, SCREEN_WIDTH, lava_height)
                    # Only draw the visible portion of the lava
                    sub_rect = pygame.Rect(0, 600 - lava_height, SCREEN_WIDTH, lava_height)
                    screen.blit(lava_img, lava_rect, sub_rect)
                else:
                    pygame.draw.rect(screen, (600, 60, 30), 
                                    pygame.Rect(0, SCREEN_HEIGHT - lava_height, SCREEN_WIDTH, lava_height))
            
            # Draw health bar
            boss.draw_health_bar(screen, game_state.current_phase, game_state.loop_count)
            
            # Apply screen overlay if active
            if screen_overlay and overlay_alpha > 0:
                screen_overlay.set_alpha(int(overlay_alpha))
                screen.blit(screen_overlay, (0, 0))
        
        elif game_state.current_state == "menu":
            # Draw menu
            title_text = large_font.render("IMPOSSIBLE BOSS", True, (255, 0, 0))
            instructions_text = font.render("Press ENTER to start", True, (255, 255, 255))
            
            screen.blit(title_text, 
                       (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 
                        SCREEN_HEIGHT // 3 - title_text.get_height() // 2))
            
            screen.blit(instructions_text, 
                       (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - instructions_text.get_height() // 2))
            
            controls_text1 = font.render("Move: WASD | Shoot: K | Dash: SHIFT+Direction", True, (200, 200, 200))
            
            screen.blit(controls_text1, 
                       (SCREEN_WIDTH // 2 - controls_text1.get_width() // 2, 
                        SCREEN_HEIGHT * 2 // 3))
        
        elif game_state.current_state == "win":
            # Draw win screen
            win_text = large_font.render("YOU WIN!", True, (0, 255, 0))
            restart_text = font.render("Press ENTER to return to menu", True, (255, 255, 255))
            
            screen.blit(win_text, 
                       (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                        SCREEN_HEIGHT // 3 - win_text.get_height() // 2))
            
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - restart_text.get_height() // 2))
            
            found_text = font.render("You found the secret ending!", True, (255, 255, 0))
            screen.blit(found_text, 
                       (SCREEN_WIDTH // 2 - found_text.get_width() // 2, 
                        SCREEN_HEIGHT * 2 // 3 - found_text.get_height() // 2))
        
        elif game_state.current_state == "lose":
            # Draw lose screen
            lose_text = large_font.render("YOU DIED", True, (255, 0, 0))
            restart_text = font.render("Press ENTER to return to menu", True, (255, 255, 255))
            
            screen.blit(lose_text, 
                       (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, 
                        SCREEN_HEIGHT // 3 - lose_text.get_height() // 2))
            
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - restart_text.get_height() // 2))
            
            if game_state.current_phase >= 4:
                hint_text = font.render("Hint: In phase 4, lava is safe...", True, (200, 200, 200))
                screen.blit(hint_text, 
                           (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 
                            SCREEN_HEIGHT * 2 // 3 - hint_text.get_height() // 2))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
