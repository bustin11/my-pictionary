import socket
import json
import time as t
import pytest 
from msg import Msg

class ServerTester:
  SERVER_IP = '127.0.0.1'
  SERVER_PORT = 5005
  END_MARKER = "#"

  def __init__(self, name):
    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # no need to bind if client
    self.name = name
    self.connect_to_server()

  def connect_to_server(self):
    try:
      self.connection.connect((self.SERVER_IP, self.SERVER_PORT))
      self.connection.sendall(self.name.encode())
      print("Connected to server")
      print(self.connection.recv(2048).decode())
    except Exception as e:
      self.disconnect(e)

  def send(self, data):
      try:
        self.connection.send(json.dumps(data).encode())
        received = ""
        while True:
          last = self.connection.recv(1024).decode()
          received += last
          try:
            if received.count(self.END_MARKER) == 1:
                break
          except:
            pass
        return json.loads(received[:-1])
      except Exception as e:
        self.disconnect(e)

  def disconnect(self, msg):
    print(f"Disconnected from server: {msg}")
    self.connection.close()


network = ServerTester("Bustin")
msg = Msg()

print("Testing Guess")
out = network.send({msg.GUESS:["banana"]})
print(out)

t.sleep(0.1)
print("Testing Grab Screen")
out = network.send({msg.GRAB_SCREEN:[]})
print(out)

t.sleep(0.1)
print("Testing Get Score")
out = network.send({msg.GET_SCORE:[]})
print(out)

t.sleep(0.1)
print("Testing Get Players")
out = network.send({msg.GET_PLAYERS:[]})
print(out)

t.sleep(0.1)
print("Testing Get Chat Box")
out = network.send({msg.GET_CHAT_BOX:[]})
print(out)

t.sleep(0.1)
print("Testing Get Round")
out = network.send({msg.GET_ROUND:[]})
print(out)

t.sleep(0.1)
print("Testing Get Word")
out = network.send({msg.GET_WORD:[]})
print(out)

t.sleep(0.1)
print("Testing Draw")
out = network.send({msg.DRAW:[(11,11,11), 100, 200]})
print(out)

t.sleep(0.1)
print("Testing Clear")
out = network.send({msg.CLEAR:[]})
print(out)

t.sleep(0.1)
print("Testing time left")
out = network.send({msg.TIME_LEFT:[]})
print(out)

t.sleep(0.1)
print("Testing Drawing player")
out = network.send({msg.DRAWING_PLAYER:[]})
print(out)



