from tank_operator import OperatorActions
from tank_operator import GameState
from tank_operator import TankOperator
from src.vec import Vec

class MyTankOperator(TankOperator):
    def __init__(self):
        self.name = "Insert Name here"
    
    def get_operator_name(self):
        return self.name
    
    def get_tank_action(self, gamestate):
        actions = OperatorActions()
        
        # A little help:
        # actions.turn    # [-1.0 to 1.0] left to right respectively.
        # actions.engine  # [-1.0 to 1.0] reverse to full ahead.
        # actions.shoot   # Set to True to fire cannon! Beware that cannon has to reload between shots.
        # The gamestate object tells you the position and direction of: you, the other tanks, and all shots fired.. 
        # (Check out the tank_operator.py file to see how the gamestate class is defined)
        
        ## Figure out what to do!

        return actions