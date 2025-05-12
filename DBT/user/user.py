import socket
import json
import rsa



class Client:
    def __init__(self, host, port):
        self.port = port
        self.host = host

class Authorization(Client):
    def registration(self, login, password, staffRight = False):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        self.clientSocket.send(json.dumps({"action":"registrarion", "login":login, "password":password, "staffRight":staffRight}, ensure_ascii=False, indent=2).encode())
        self.clientSocket.recv(1024)
        self.clientSocket.close()

    def login(self, login, password):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        self.clientSocket.send(json.dumps({"action":"login","login":login, "password":password}, ensure_ascii=False, indent=2).encode())
        self.clientSocket.recv(1024)
        self.clientSocket.close() 

class OrderManager(Client):
    def SendOrder(self, orderId, carriageNumber, placeNumber, dishesId, status = "notStarted"):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        self.clientSocket.send(json.dumps({"action":"order", "orderId":orderId, "carriageNumber":carriageNumber, "placeNumber":placeNumber, "dishesId":dishesId, "status":status}, ensure_ascii=False, indent=2).encode())
        self.clientSocket.recv(1024)
        self.clientSocket.close()


