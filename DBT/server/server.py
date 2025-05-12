import pandas as pd
import socket
import json


class OrderManager:
    def __init__(self):
        self.orders = pd.read_csv("orders.csv", index_col="index")
    
    def addOrder(self, orderId, carriageNumber, placeNumber, dishesId, status):
        self.orders.loc[len(self.orders)] = [orderId, carriageNumber, placeNumber, dishesId, status]
        print(orderId, carriageNumber, placeNumber, dishesId, status)
        self.orders.to_csv("DBT/orders.csv")
        return "True"

class Server:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(1)
        
        self.om = OrderManager()

    def managerRequest(self):
        client_socket, addr = self.sock.accept()
        data = client_socket.recv(4096)
        data = json.loads(data.decode())
    
        if data["action"] == "order":
            client_socket.send((self.om.addOrder(data["orderId"], data["carriageNumber"], data["placeNumber"], data["dishesId"]).encode()))
            client_socket.close() 






        
