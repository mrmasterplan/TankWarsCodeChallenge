# -*- coding: utf-8 -*-

from src.vec import Vec
# Vec is a 2D vector with member attributes x and y.

class GameObject:
    def __init__(self, position, direction):
        """
        Represents a general object in the game.

        :param position: Vec instance representing the object's position on the game field.
        :param direction: Vec instance representing the object's facing direction.
        """
        self.position = position
        self.direction = direction

class GameState:
    def __init__(self, tank, other_tanks, shots):
        """
        Holds the current state of the game, providing necessary information for decision-making.

        :param tank: GameObject representing the player's tank.
        :param other_tanks: List of GameObjects representing other tanks in the game.
        :param shots: List of GameObjects representing shots currently active in the game. Beware of incoming grenades!
        """
        self.tank = tank
        self.other_tanks = other_tanks
        self.shots = shots

class OperatorActions:
    def __init__(self, turn = 0.0, engine = 0.0, shoot = False):
        """
        Encapsulates the actions that a tank operator can take in a given frame.
        """
        self.turn = turn    # [-1.0 to 1.0] left to right respectively.
        self.engine = engine  # [-1.0 to 1.0] reverse to full ahead.
        self.shoot = shoot  # Set to True to fire cannon! Beware that cannon has to reload between shots.

class TankOperator:
    def get_tank_action(self,game_state):
        """
        This method should be implemented by the user to define the tank's actions based on the game state.

        :param game_state: GameState instance containing information about the current state of the game.
        :return: OperatorActions instance representing the tank's actions for the current frame.
        """
        raise NotImplementedError("This method should be overridden in a subclass")

    def get_operator_name(self):
        """
        Returns the name of the operator.

        :return: String representing the operator's name.
        """
        raise NotImplementedError("This method should be overridden in a subclass")

