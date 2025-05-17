import pandas as pd
import socket
import json


class OrderManager:
    def __init__(self):
        self.orders = pd.read_csv("DBT/server/orders.csv", index_col="index")
        self.products = pd.read_csv("DBT/server/products.csv")
        
                                  
    
    def addOrder(self, orderId, carriageNumber, placeNumber, dishesId):
        self.orders.loc[len(self.orders)] = [orderId, carriageNumber, placeNumber, dishesId]
        print(orderId, carriageNumber, placeNumber, dishesId)
        self.orders.to_csv("DBT/server/orders.csv")
        return "True"
    
    def getMostPopulatFood(self):
        section_id = self.products["section_id"]
        result = [0] * len(self.products)
        for i in range(len(set(section_id))):
            category = self.products.query(f"section_id == {i}")
            result[section_id.index[i] + category["count"].index(max(category["count"]))] = 1
            
        return result
            
        


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
            self.om.products["count"] = list(map(sum, zip(self.om.products["count"],data["dishesId"])))
            self.om.products.to_csv("DBT/server/orders.csv", index=False)
            client_socket.close()

        if data["action"] == "getMostPopulatFood":
            client_socket.send(str(self.om.getMostPopulatFood()).encode())
            client_socket.close()






        
