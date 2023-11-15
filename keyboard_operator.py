import pygame
from tank_operator import OperatorActions
from tank_operator import TankOperator

class KeyboardOperator(TankOperator):
    def __init__(self, name, 
                 fwdKey = pygame.K_UP, 
                 backKey = pygame.K_DOWN, 
                 leftKey = pygame.K_LEFT, 
                 rightKey = pygame.K_RIGHT, 
                 shootKey = pygame.K_KP0, 
                 turretLeftKey = pygame.K_KP1,
                 turretRightKey = pygame.K_KP2):
        self.forwardKey = fwdKey #pygame.K_w
        self.backKey = backKey #pygame.K_s
        self.leftKey = leftKey #pygame.K_a
        self.rightKey = rightKey #pygame.K_d
        self.shootKey = shootKey #pygame.K_SPACE
        self.turretLeftKey = turretLeftKey
        self.turretRightKey = turretRightKey
        self.name = name
    
    def get_operator_name(self):
        return self.name
    
    def get_tank_action(self, _):
        actions = OperatorActions(0,0,False)

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

        if keys[self.turretLeftKey]:
            actions.turn_turret = -1.0
        if keys[self.turretRightKey]:
            actions.turn_turret += 1.0
            
        # Check if spacebar is pressed for shooting
        actions.shoot = keys[self.shootKey]

        return actions