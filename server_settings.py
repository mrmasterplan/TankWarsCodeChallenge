from keyboard_operator import KeyboardOperator
from dummy_operator import DummyOperator
from my_tank_operator import MyTankOperator
from operator_tcp_adapter import OperatorTCPadaptor_Server
from src.vec import Vec
import pygame

starting_positions = [
    "red",  #red is upper left corner
    "blue", #blue is upper right corner
    "yellow", #Yellow is lower left corner
    "green" #Green is lower right corner
]

server_ip = 'localhost' #TODO change on LAN!

def get_tank_operators_and_starting_positions():
    """ Edit to specify types of operators in game MIN two and MAX four players. """
    return {
        "red"   : DummyOperator(),
        "blue"  : KeyboardOperator("BlueBob"), #Default arrow keys
        "yellow": OperatorTCPadaptor_Server(server_ip),
        "green" : MyTankOperator(),
    }

server_fullscreen = False
