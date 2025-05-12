import pandas as pd
import socket
import rsa
import json


class UserManager:
    def __init__(self):
        self.users = pd.read_csv("users.csv")
    
    def regestration(self, login, password, staffRights):
        if login not in self.users["login"]:
            self.users.loc[self.users.shape[0]] = [login, password, "0"*(12-int(len(str(self.users.shape[0])))) + str(self.users.shape[0]), staffRights]
            return "True"
        else:
            return "False"
        
        self.users.to_csv("users.csv")
        
    def login(self, login, password):
        if login in self.users["login"] and password == self.users[self.users["login"] == login]["password"]:
            return "True"
        else:
            return "False"

class OrderManager:
    def __init__(self):
        self.orders = pd.read_csv("orders.csv", index_col="index")
    
    def addOrder(self, orderId, carriageNumber, placeNumber, dishesId, status):
        self.orders.loc[len(self.orders)] = [orderId, carriageNumber, placeNumber, dishesId, status]
        print(orderId, carriageNumber, placeNumber, dishesId, status)
        self.orders.to_csv("orders.csv")
        return "True"

class Server:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(1)
        
        self.um = UserManager()
        self.om = OrderManager()

    def managerRequest(self):
        client_socket, addr = self.sock.accept()
        data = client_socket.recv(4096)
        data = json.loads(data.decode())
        
        if data["action"] == "registrarion":
            client_socket.send((self.um.regestration(data["login"], data["password"], data["staffRight"])).encode())
            client_socket.close()

        if data["action"] == "login":
            client_socket.send((self.um.login(data["login"], data["password"]).encode()))
            client_socket.close()

        if data["action"] == "order":
            client_socket.send((self.om.addOrder(data["orderId"], data["carriageNumber"], data["placeNumber"], data["dishesId"], data["status"]).encode()))
            client_socket.close() 






        
