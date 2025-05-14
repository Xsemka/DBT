import socket
import json

class Client:
    def __init__(self, host, port):
        self.port = port
        self.host = host

class OrderManager(Client):
    def SendOrder(self, orderId, carriageNumber, placeNumber, dishesId):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((self.host, self.port))
        self.clientSocket.send(json.dumps({"action":"order", "orderId":orderId, "carriageNumber":carriageNumber, "placeNumber":placeNumber, "dishesId":dishesId}, ensure_ascii=False, indent=2).encode())
        self.clientSocket.recv(1024)
        self.clientSocket.close()


