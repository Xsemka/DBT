import pandas as pd
import socket
import json


class OrderManager:
    def __init__(self):
        self.orders = pd.read_csv("DBT/server/orders.csv", index_col="index")
        self.foods = pd.DataFrame({"dishes": pd.read_csv("DBT/server/products.csv")["product_name"]})
        for i in range(len(self.foods["dishes"])):
            if pd.read_csv("DBT/server/food.csv")["count"][i] == None:
                self.foods["count"][i] = 0
            else:
                self.foods["count"][i] = pd.read_csv("DBT/server/food.csv")["count"][i]
        self.foods.to_csv("DBT/server/food.csv")
                                  
    
    def addOrder(self, orderId, carriageNumber, placeNumber, dishesId):
        self.orders.loc[len(self.orders)] = [orderId, carriageNumber, placeNumber, dishesId]
        print(orderId, carriageNumber, placeNumber, dishesId)
        self.orders.to_csv("DBT/server/orders.csv")
        return "True"
    
    def getMostPopulatFood(self):
        pass


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
            self.om.foods = self.om.foods.assign(count = data["dishesId"] + self.om.foods["count"])
            self.om.foods.to_csv("DBT/server/food.csv", index=False)
            client_socket.close() 






        
