import socket
import json 
import pygame
from game import Game
from msg import Msg
import time as t

class Client(object):

  END_MARKER = '#'

  def __init__(self, name):
    self.name = name
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.addr = ('127.0.0.1', 5005)

  def connect(self):
    try:
      self.client.connect(self.addr)
      self.client.sendall(self.name.encode())
      received = self.client.recv(1024).decode()
      print("Connected to server")
      return received
    except Exception as e:
      print(e)

  def send(self, message):
    try:
      self.client.sendall(json.dumps(message).encode())
      received = ""
      while True:
        last = self.client.recv(1024).decode()
        received += last
        try:
          if received[-1] == '#':
            break
        except:
          pass
      return json.loads(received[:-1])
    except Exception as e:
      print(e)

if __name__ == '__main__':
  pygame.font.init()
  client = Client('Bustin')
  name = client.connect() # can be different if two names exist
  print('Your name is ' + name)

  response = list(client.send({Msg.START : []}).values())[0]
  print("Waiting for other players to join")
  while not response:
    t.sleep(.1)
    response = list(client.send({Msg.START : []}).values())[0]
        
    
  players = client.send({Msg.GET_PLAYERS : []})
  game = Game(name, players, client)
  game.run()