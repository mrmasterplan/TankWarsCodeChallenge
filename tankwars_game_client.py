import client_settings
from operator_tcp_adapter import OperatorTCPadaptor_Client
import pygame


#client_settings.tankoperator

#OperatorTCPadaptor_Client

def establish_connection_to_server(serverIp = client_settings.serverIp, serverPort = client_settings.serverPort):
    pass




if __name__ == "__main__":
    print("Running Tank wars Operator client. Connecting to " + client_settings.serverIp + ":" + str(client_settings.serverPort))
    print("Using Tank operator: " + str(type(client_settings.tankoperator)) + " (Change this in client_setting.py if needed)")


