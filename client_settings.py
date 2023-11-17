import pygame

from my_tank_operator import MyTankOperator
from keyboard_operator import KeyboardOperator
from dummy_operator import DummyOperator

# Change these to reflect the server you want to connect to!
serverIp = "10.4.13.96"
serverPort = 63587

""" When your MyTankOperator is ready - use it like this: """
tankoperator = MyTankOperator()

""" To just have a stupid dummy operator that shoots in circles around it: """
#tankoperator = DummyOperator()

""" To run with a human controlled operator (key bindings can be specified in constructor arguments) do this:"""
# tankoperator = KeyboardOperator("Hooman Player", shootKey = pygame.K_SPACE) #Default arrow keys, keypad zero=shoot