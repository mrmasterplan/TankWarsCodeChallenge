import traceback
import socket
import time
import json
from src.json_protocol import JSONProtocol
from src.vec import Vec
from tank_operator import TankOperator
from tank_operator import OperatorActions
from tank_operator import GameState
from tank_operator import TankObject
from tank_operator import ShotObject

from src.tcp_server import TcpServer
from src.tcp_client import TcpClient

class NameResponse:
    def __init__(self, name):
        self.name = name

class GameOverMessage:
    def __init__(self, game_over_message):
        self.game_over_message = game_over_message

class OperatorTCPadaptor_Server(TankOperator):
    def __init__(self, serverIp):
        self.tcp_server = TcpServer(serverIp)
        self.name = None
        self.json_protocol = JSONProtocol()
        self.latestOperatorAction = OperatorActions()

    def is_client_connected(self):
        return self.tcp_server.connected
    
    def get_connection_info_string(self):
        return self.tcp_server.serverIp + ":" + str(self.tcp_server.serverPort)

    def _run_server(self, object_to_send = None):
        try:
            bytes_to_send = None
            if object_to_send:
                bytes_to_send = self.json_protocol.encode(object_to_send)
            received_bytes = self.tcp_server.run_server(bytes_to_send)
            if received_bytes:
                jsonresponses = self.json_protocol.decode(received_bytes)
                for jsonresponse in jsonresponses:
                    if "name" in jsonresponse:
                        nr = NameResponse(**jsonresponse)
                        self.name = nr.name
                    elif "turn" in jsonresponse:
                        # Just overwrite older action response
                        self.latestOperatorAction =  OperatorActions(**jsonresponse)
        except:
            self.json_protocol = JSONProtocol()
  
            
    def get_tank_action(self, game_state):
        self._run_server(game_state)
        return self.latestOperatorAction #always repeat latest action if nothing new

    def get_operator_name(self):       
        # designed for polling
        self._run_server()
        return self.name
    
    def send_game_over_message(self, message):
        self._run_server(GameOverMessage(message))             

class OperatorTCPadaptor_Client:
    def __init__(self, serverIp, serverPort, tankoperator):
        self.tankoperator = tankoperator
        self.json_protocol = JSONProtocol()
        self.tcp_client = TcpClient(serverIp, serverPort)
        self.bytes_to_send = None
        self.name_sent = False

        self._messages_received = 0
        self._actions_sent = 0
        self.game_over_message = None
    
    def deserialize_game_state(self,data):
        def dict_to_vec(d):
            return Vec(d['x'], d['y'])

        def dict_to_tank(d):
            return TankObject(dict_to_vec(d['position']), dict_to_vec(d['direction']), dict_to_vec(d['turret_direction']))

        def dict_to_shot(d):
            return ShotObject(dict_to_vec(d['position']), dict_to_vec(d['direction']))

        tank = dict_to_tank(data['tank'])
        other_tanks = [dict_to_tank(t) for t in data['other_tanks']]
        shots = [dict_to_shot(s) for s in data['shots']]

        return GameState(tank, other_tanks, shots)
    
    def run_client(self):
        try:
            received_bytes = self.tcp_client.run_client(self.bytes_to_send)
            self.bytes_to_send = None
            if received_bytes:
                jsonresponses = self.json_protocol.decode(received_bytes)
                if jsonresponses:
                    self._messages_received += len(jsonresponses)
                    lastmessage_json = jsonresponses[-1] # JUST USE LAST GAMESTATE others are stale..
                    try:
                        gamestate = self.deserialize_game_state(lastmessage_json)
                        try:
                            action = self.tankoperator.get_tank_action(gamestate)
                            self.bytes_to_send = self.json_protocol.encode(action)
                            self._actions_sent += 1
                        except Exception:
                            print(traceback.format_exc())
                    except:
                        try:
                            self.game_over_message = GameOverMessage(**lastmessage_json).game_over_message
                        except:
                            print("Message from server not understood: " + str(lastmessage_json))

        except:
            self.json_protocol = JSONProtocol()
            self.bytes_to_send = None
        
        if self.bytes_to_send == None and self.tcp_client.connected and not self.name_sent:
            self.bytes_to_send = self.json_protocol.encode(NameResponse(self.tankoperator.get_operator_name()))
            self.name_sent = True
        return None != self.bytes_to_send #True if more work, call again asap.


# class MockTankOperator(TankOperator):
#     def tank_action(self, game_state):
#         return OperatorActions(0.5,0.1,True)

#     def get_operator_name(self):
#         return "MockOperator"

# ss = OperatorTCPadaptor_Server('localhost')
# cc = OperatorTCPadaptor_Client('localhost', ss.tcp_server.serverPort, MockTankOperator())
# nn = None
# while not nn:
#     nn = ss.get_operator_name()
#     cc.run_client()
    
# print(nn)

# from src.vec import Vec
# from tank_operator import GameObject
# vv = Vec(1,1)
# gg = GameObject(vv, vv)


# while True:
#     aa = ss.tank_action(GameState(gg, [gg,gg,gg], [gg,gg,gg,gg,gg]))
#     if aa:
#         print(aa.turn, aa.engine, aa.shoot)
#     cc.run_client()
#     time.sleep(1/30)
    