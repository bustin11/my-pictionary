import socket
import json 


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
      print(received)
    except Exception as e:
      print(e)

  def send(self, code, message):
    try:
      self.client.sendall(json.dumps({code : message}).encode())
      received = ""
      while True:
        last = self.client.recv(1024).decode()
        received += last
        try:
          if received[-1] == '#':
            break
        except:
          pass
      return received
    except Exception as e:
      print(e)

if __name__ == '__main__':
  client = Client('Bustin')
  client.connect()