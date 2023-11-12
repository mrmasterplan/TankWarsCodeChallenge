# -*- coding: utf-8 -*-

import pygame
import random
import time
import math
from src.vec import Vec
from TankOperator import OperatorActions
from TankOperator import GameState
from TankOperator import TankOperator

## Put on github
## Make server_settings.py and have the operators with settings loaded in there. Also color.
## Make game_client.py and settings for it - it should load a specific operator
## Create operator instructions.
##  Create install and run instructions
## Send to Nico :-)
## Make game time out or similar..
## Better tank pngs (make one with a colored letter on it!?) or make interface so they can provide it?

## OptionaL_
## Make obstacles (mountains?)
## Remove or fade broken tanks

pygame.init()

display_size = Vec(1200, 800)

intro_display_seconds = 1 #5 #TODO:Prod
game_fps = 30
tank_image_size = (50, 50)

##Movement:
tank_turn_speed = tank_turn_speed = math.radians(7.5)
tank_maxspeed = 3.5

shot_speed = 15.0
tank_shots_cooldown = 1.2  #seconds

game_layout_display = pygame.display.set_mode(display_size.as_tuple())
pygame.display.set_caption('Tanks Game 2')

Resources = pygame.image.load("res/grass.png")

tankRedImage = pygame.transform.scale(pygame.image.load('res/tankred.png'), tank_image_size)
tankBlueImage = pygame.transform.scale(pygame.image.load('res/tankblue.png'), tank_image_size)

shotImage = pygame.transform.scale(pygame.image.load('res/shot.png'), (15,20))

pygame.display.set_icon(Resources)

# colors
wheat = (245, 222, 179)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

red = (200, 0, 0)
light_red = (255, 0, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

# for picking current time for the frames per second
clock = pygame.time.Clock()
# geometry of tank and its turret
tnk_width = 40
tnk_height = 20

s_font = pygame.font.SysFont("Arial", 25)
m_font = pygame.font.SysFont("Arial", 50)
l_font = pygame.font.SysFont("Arial", 85)
vs_font = pygame.font.SysFont("Arial", 25)

# defining function to get the fonts and sizes assigned with them by size names by default size="small"
def txt_object(txt, color, size="small"):
    if size == "small":
        txtSrfc = s_font.render(txt, True, color)
    if size == "medium":
        txtSrfc = m_font.render(txt, True, color)
    if size == "large":
        txtSrfc = l_font.render(txt, True, color)
    if size == "vsmall":
        txtSrfc = vs_font.render(txt, True, color)

    return txtSrfc, txtSrfc.get_rect()

# function for texts that has to appear over screen
def msg_screen(message, color, y_displace=0, size="small"):
    txtSrf, textRect = txt_object(message, color, size)
    textRect.center = (int(display_size.x / 2), int(display_size.y / 2) + y_displace)
    game_layout_display.blit(txtSrf, textRect)
    
def game_intro():
    intro_time = time.time()

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        msg_screen("Trophy Wall Tank Wars!", white, -100, size="medium")
        msg_screen("Battle commencing...", wheat, 15)
        
        pygame.display.update()

        clock.tick(15)
        if time.time() - intro_time > intro_display_seconds:
            print("5 seconds have passed.")
            break

# function for game Over screen
def game_over(winner):
    game_over = True

    while game_over:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_layout_display.fill(black)
        msg_screen("Game Over - Winner is:", white, -100, size="medium")
        msg_screen(winner, wheat, 0, size="large")

        pygame.display.update()

        clock.tick(15)
        

        
        
class GameEntity:
    def get_orientation_angle(self):
        return self.direction.get_orientation_angle()
        
    def apply_turn(self, operator_actions):
        # Calculate the current orientation angle
        current_angle = math.atan2(self.direction.y, self.direction.x)
        
        # Cap turning:
        turn_value = max(-1.0, min(1.0, operator_actions.turn))
        
        # Calculate the change in angle based on the turn value and turn speed
        # The turn value is between -1 and 1, so multiplying by the turn speed gives the angle change
        angle_change = turn_value * tank_turn_speed
        
        # Update the current angle based on the angle change
        new_angle = current_angle + angle_change
        
        # Calculate the new orientation vector from the new angle
        self.direction.x = math.cos(new_angle)
        self.direction.y = math.sin(new_angle)
    
    def move_player(self, operator_actions, maxspeed = tank_maxspeed):
        # Normalize the orientation vector
        self.direction.normalize()
        
        # Cap Speed
        operator_speed_value = max(-1.0, min(1.0, operator_actions.engine))
        
        # Update the player's position based on the normalized orientation and speed
        self.position.x += self.direction.x * maxspeed * operator_speed_value
        self.position.y += self.direction.y * maxspeed * operator_speed_value
        
        def cap_value_zero_max(cap, max_val):
            if cap > max_val or cap < 0:
                return True, max(0.0, min(max_val, cap))
            else:
                return False, cap
    
        cappedX, self.position.x = cap_value_zero_max(self.position.x, display_size.x)
        cappedY, self.position.y = cap_value_zero_max(self.position.y, display_size.y)
        
        return cappedX or cappedY

class PlayerContext(GameEntity):   
    def __init__(self, startX, startY, startDirectionX, startDirectionY, name, operator, image):
        self.position = Vec(startX, startY)
        self.direction = Vec(startDirectionX, startDirectionY)
        self.alive = True
        self.name = name
        self.operator = operator
        self.image = image

class Shot(GameEntity):
    def __init__(self, player_context):
        self.position = Vec(player_context.position)
        self.direction = Vec(player_context.direction)
        self.playerContext = player_context
    
    
class KeyboardOperator(TankOperator):
    def __init__(self, fwdKey = pygame.K_UP, backKey = pygame.K_DOWN, leftKey = pygame.K_LEFT, rightKey = pygame.K_RIGHT, shootKey = pygame.K_KP0):
        self.forwardKey = fwdKey #pygame.K_w
        self.backKey = backKey #pygame.K_s
        self.leftKey = leftKey #pygame.K_a
        self.rightKey = rightKey #pygame.K_d
        self.shootKey = shootKey #pygame.K_SPACE
    
    def get_actions(self):
        actions = OperatorActions()

        # Get the current state of all keyboard buttons
        keys = pygame.key.get_pressed()

        actions.engine = 0.0
        # Check for 'w' and 's' for engine control
        if keys[self.forwardKey]:
            actions.engine = 1.0
        if keys[self.backKey]:
            actions.engine += -1.0

        actions.turn = 0.0
        # Check for 'a' and 'd' for turning
        if keys[self.leftKey]:
            actions.turn = -1.0
        if keys[self.rightKey]:
            actions.turn += 1.0

        # Check if spacebar is pressed for shooting
        actions.shoot = keys[self.shootKey]

        return actions

class DummyOperator(TankOperator):
    def get_actions(self):
        actions = OperatorActions()
        actions.turn = -1.0
        actions.shoot = True
        return actions
    

shots_cooldown_expiry = {}    
def check_shots_fired(player_context, operator_actions):
    shot = None
    
    if operator_actions.shoot:
        cooldown = False
        try:
            if shots_cooldown_expiry[player_context] > time.time():
                #cooldown in effect
                cooldown = True
        except Exception:
            pass    
        
        if not cooldown:        
            shot = Shot(player_context)
            shots_cooldown_expiry[player_context] = time.time() + tank_shots_cooldown
    return shot
        
def render_entity(ent, image):
    ent_image = pygame.transform.rotate(image, -1.0 * ent.get_orientation_angle())
    ent_image_rect = ent_image.get_rect(center=ent.position.as_tuple())

    # Draw rotated images
    game_layout_display.blit(ent_image, ent_image_rect.topleft)

class Explosion:
    def __init__(self, center, duration):
        self.center = center
        self.start_time = pygame.time.get_ticks()
        self.duration = duration * 1000  # convert seconds to milliseconds
        self.alive = True
        
# Function to draw the explosion
def draw_explosion(screen, explosion):
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - explosion.start_time

    if elapsed_time > explosion.duration:
        explosion.alive = False
        return

    # Calculate the radius of the explosion based on elapsed time
    max_radius = 50  # maximum radius of the largest circle
    num_circles = 5  # number of circles in the explosion
    for i in range(num_circles):
        # Randomize the color slightly to vary between red and orange
        color = (255, random.randint(100, 160), 0)
        # Each circle starts small and expands over time
        radius = max_radius * (i + 1) / num_circles * (elapsed_time / explosion.duration)
        pygame.draw.circle(screen, color, explosion.center, int(radius))
        
def game_loop(tanks):
    winner = None
        
    shots = []
    explosions = []
    
    while winner is None:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                return "NONE - quitting early?"
        #main game loop - render, act, repeat
        
        ## Render
        # Clear the screen
        game_layout_display.fill((0, 0, 0))

        ## Update tank movement
        for tank in tanks:
            if tank.alive:
                tankActions = tank.operator.get_actions()
                tank.apply_turn(tankActions)
                tank.move_player(tankActions)
                shot = check_shots_fired(tank, tankActions)
                if not shot is None:
                    shots.append(shot)
            
            render_entity(tank, tank.image)
                        
        for ss in shots:
            shotOp = OperatorActions()
            shotOp.engine = 1.0
            if ss.move_player(shotOp, shot_speed):
                #shot reached border
                shots.remove(ss)
                explosions.append(Explosion(ss.position.as_tuple(),1))
                
            render_entity(ss, shotImage)
        
        for ee in explosions:
            draw_explosion(game_layout_display, ee)
            if not ee.alive:
                explosions.remove(ee)
        
        ## Check for win conditions!
        for shot in shots:
            shot_rect = pygame.Rect(shot.position.x, shot.position.y, shotImage.get_width(), shotImage.get_height())
            for tank in tanks:
                if tank != shot.playerContext:
                    tank_rect = pygame.Rect(tank.position.x, tank.position.y, tank_image_size[0], tank_image_size[1])
                    if shot_rect.colliderect(tank_rect):
                        shots.remove(shot)
                        explosions.append(Explosion(shot.position.as_tuple(),3))
                        tank.alive = False
        
        tanksalive = [tt for tt in tanks if tt.alive]
        
        if len(tanksalive) == 1:
            winner = tanksalive[0].name
        if len(tanksalive) == 0:
            #Hmm?
            winner = "Draw - no one survived"
        
        pygame.display.update()
        clock.tick(game_fps)
    
    # before ending, let the winner explosion render to completion
    while explosions:
        for ee in explosions:
            draw_explosion(game_layout_display, ee)
            if not ee.alive:
                explosions.remove(ee)
        pygame.display.update()
        clock.tick(game_fps)
    
    return winner
        
########################################### ACTION!
        
game_intro() #TODO:Prod
#tanks = init_players()

tankRedOperator = KeyboardOperator(pygame.K_w,pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE) #WASD player
tankBlueOperator = KeyboardOperator()    #arrow-key operator

tanks  = [PlayerContext(50, 50, -1, -1, "Red", tankRedOperator, tankRedImage),
          PlayerContext(display_size.x-50, display_size.y-50, 1, 1, "Blue", tankBlueOperator, tankBlueImage) ]#,
          #PlayerContext(display_size.x-50, 50, 1, -1, "Green", DummyOperator(), tankBlueImage)]


winner = game_loop(tanks)
game_over(winner) #TODO:Prod
pygame.quit()
