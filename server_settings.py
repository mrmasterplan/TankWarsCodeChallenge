from keyboard_operator import KeyboardOperator
from dummy_operator import DummyOperator
from my_tank_operator import MyTankOperator
from operator_tcp_adapter import OperatorTCPadaptor_Server
from ahj_tank_operator import AhjTankOperator
from src.vec import Vec
import pygame

starting_positions = [
    "red",  #red is upper left corner
    "blue", #blue is upper right corner
    "yellow", #Yellow is lower left corner
    "green" #Green is lower right corner
]

server_ip = '192.168.1.195' #TODO change on LAN!

def get_tank_operators_and_starting_positions():
    """ Edit to specify types of operators in game MIN two and MAX four players. """
    return {
        "red"   : OperatorTCPadaptor_Server(server_ip),
        "blue"  : OperatorTCPadaptor_Server(server_ip), #Default arrow keys
        "yellow": OperatorTCPadaptor_Server(server_ip),
        "green" : OperatorTCPadaptor_Server(server_ip),
    }

server_fullscreen = False
