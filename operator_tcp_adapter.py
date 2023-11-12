from src.json_protocol import JSONProtocol
import socket
import time
from tank_operator import TankOperator
from tank_operator import OperatorActions
from tank_operator import GameState

from src.tcp_server import TcpServer
from src.tcp_client import TcpClient

class NameResponse:
    def __init__(self, name):
        self.name = name

class OperatorTCPadaptor_Server(TankOperator):
    def __init__(self, serverIp):
        self.tcp_server = TcpServer(serverIp)
        self.name = None
        self.json_protocol = JSONProtocol()
        self.latestOperatorAction = OperatorActions()

    def _run_server(self, object_to_send = None):
        try:
            bytes_to_send = None
            if object_to_send:
                bytes_to_send = self.json_protocol.encode(object_to_send)
            received_bytes = self.tcp_server.run_server(bytes_to_send)
            if received_bytes:
                jsonresponse = self.json_protocol.decode(received_bytes)
                if jsonresponse:
                    if "turn" in jsonresponse:
                        self.latestOperatorAction =  OperatorActions(**jsonresponse)
                    elif "name" in jsonresponse:
                        nr = NameResponse(**jsonresponse)
                        self.name = nr.name
        except:
            self.json_protocol = JSONProtocol()
  
            
    def tank_action(self, game_state):
        self._run_server(game_state)
        return self.latestOperatorAction #always repeat latest action if nothing new

    def get_operator_name(self):       
        # designed for polling
        self._run_server()
        return self.name

             

class OperatorTCPadaptor_Client:
    def __init__(self, serverIp, serverPort, tankoperator):
        self.tankoperator = tankoperator
        self.json_protocol = JSONProtocol()
        self.tcp_client = TcpClient(serverIp, serverPort)
        self.bytes_to_send = None
        self.name_sent = False
        
    def run_client(self):
        try:
            received_bytes = self.tcp_client.run_client(self.bytes_to_send)
            self.bytes_to_send = None
            if received_bytes:
                jsonresponse = self.json_protocol.decode(received_bytes)
                if jsonresponse:
                    try:
                        gamestate = GameState(**jsonresponse)
                        action = self.tankoperator.tank_action(gamestate)
                        self.bytes_to_send = self.json_protocol.encode(action)
                    except:
                        print("Message from server not understood: " + str(jsonresponse))
        except:
            self.json_protocol = JSONProtocol()
            self.bytes_to_send = None
        
        if self.bytes_to_send == None and self.tcp_client.connected and not self.name_sent:
            self.bytes_to_send = self.json_protocol.encode(NameResponse(self.tankoperator.get_operator_name()))
            self.name_sent = True
        return None != self.bytes_to_send #True if more work, call again asap.


class MockTankOperator(TankOperator):
    def tank_action(self, game_state):
        return OperatorActions(0.5,0.1,True)

    def get_operator_name(self):
        return "MockOperator"

ss = OperatorTCPadaptor_Server('localhost')
cc = OperatorTCPadaptor_Client('localhost', ss.tcp_server.serverPort, MockTankOperator())
nn = None
while not nn:
    nn = ss.get_operator_name()
    cc.run_client()
    
print(nn)

from src.vec import Vec
from tank_operator import GameObject
vv = Vec(1,1)
gg = GameObject(vv, vv)


while True:
    aa = ss.tank_action(GameState(gg, [gg,gg,gg], [gg,gg,gg,gg,gg]))
    if aa:
        print(aa.turn, aa.engine, aa.shoot)
    cc.run_client()
    time.sleep(1/30)
    