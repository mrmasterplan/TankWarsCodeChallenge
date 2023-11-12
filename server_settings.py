from keyboard_operator import KeyboardOperator
from dummy_operator import DummyOperator
from src.vec import Vec
import pygame

starting_positions = [
    "red",  #red is upper left corner
    "blue", #blue is upper right corner
    "yellow", #Yellow is lower left corner
    "green" #Green is lower right corner
]

def get_tank_operators_and_starting_positions():
    """ Edit to specify types of operators in game MIN two and MAX four players. """
    return {
        "red"   : KeyboardOperator("WASD-tank", pygame.K_w,pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
        "blue"  : KeyboardOperator("Bob"), #Default keys
        "yellow": DummyOperator(),
        "Green" : None,
    }
