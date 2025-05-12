from server import Server

s = Server("localhost", 11111)

while True:
    s.managerRequest()
