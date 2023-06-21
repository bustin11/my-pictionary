import threading
import socket
from player import Player
from game import Game
from msg import Msg
from collections import defaultdict
import logging
import json
import sys

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logging.root.name = "Server"


class Server(object):
  NUM_PLAYERS = 2
  SERVER_IP = '127.0.0.1'
  SERVER_PORT = 5005
  END_MARKER = "#"

  def __init__(self):
    self.queue = []
    self.game_id = 0
    self.MSG = Msg()
    self.screen_updated = defaultdict(dict)

  # per player thread to update the server state 
  def player_thread(self, connection, player):

    while True:
      try:
        try:
          data = connection.recv(1024)
          data = data.decode()
          data = json.loads(data)
        except Exception as e:
          break

        logging.info(f'Received {data} from {player.name}')
        print(self.screen_updated)
        package = {}
    
        for key in data:
          key = int(key)
          if key == Msg.START:
            package[key] = player.game is not None

          if player.game: # player has not disconnected at this point
            if key == self.MSG.GUESS:  # guess
              correct = player.game.make_player_guess(player, data[str(key)][key])
              package[key] = correct

            elif key == self.MSG.GET_CHAT_BOX:
              package[key] = player.game.current_round.chat_box.get_chat()

            elif key == self.MSG.GRAB_SCREEN:
              print(self.screen_updated)
              if self.screen_updated[player.game.game_id][player.name]:
                package[key] = player.game.screen.get_screen()
                self.screen_updated[player.game.game_id][player.name] = False

            elif key == self.MSG.GET_SCORE:
              package[key] = player.game.get_scores()

            elif key == self.MSG.GET_PLAYERS:
              package[key] = [player.name for player in player.game.players]

            elif key == self.MSG.GET_ROUND:
              package[key] = player.game.round_number

            elif key == self.MSG.GET_WORD:
              package[key] = player.game.current_round.current_word

            elif key == self.MSG.DRAW:
              if player.game.players[player.game.drawing_player_id] == player: # safety check
                color, x, y = data[str(key)]
                player.game.update_screen(x, y, color)
                for p in player.game.players:
                  self.screen_updated[player.game.game_id][p.name] = True

            elif key == self.MSG.TIME_LEFT:
              package[key] = player.game.current_round.time_left

            elif key == self.MSG.CLEAR:
              player.game.screen.clear_screen()

            elif key == self.MSG.DRAWING_PLAYER:          
              package[key] = player.is_drawing()

        if self.MSG.GRAB_SCREEN in package:
          logging.info(f'updating board to player {player.name}')
        else:
          logging.info(f'Sending {package} to player {player.name}')
        msg = json.dumps(package)
        connection.sendall(msg.encode() + "#".encode())
      # catch socket exception

      except socket.error as e:
        logging.error(e)
        break
        
    if player.game:
      del self.screen_updated[player.game.game_id][player.name]
      player.game.player_disconnected(player)
    
    if player in self.queue:
      self.queue.remove(player)

    logging.info(f'Player {player.name} disconnected')

  def rename(self, name):
    for player in self.queue[:min(self.NUM_PLAYERS, len(self.queue))]:
      logging.info(f'Player {name} is already in queue, renaming to {player}')
      if name == player.name:
        name = name + '1'
    return name

  def add_to_queue(self, player):
    self.queue.append(player)
    if (len(self.queue) == self.NUM_PLAYERS):
      players = []
      self.screen_updated[self.game_id]
      for i in range(self.NUM_PLAYERS):
        players.append(self.queue[0])
        self.screen_updated[self.game_id][self.queue[0].name] = False
        self.queue.pop(0)

      new_game = Game(players, self.game_id)
      logging.info(f'New game {self.game_id} created')
      self.game_id += 1
      for player in players:
        player.attach_game(new_game)
      return True

    return False


  def authenticate(self, connection):
    try:
      data = connection.recv(1024)
      name = str(data.decode())
      logging.info(f'Authenticating player {name}')
      if len(name) < 3:
        raise Exception("Name f{name} too short")

      name = self.rename(name)
      new_player = Player(name)
      self.add_to_queue(new_player)      
      connection.sendall(f"{name}".encode())
      threading.Thread(target=self.player_thread, args=(connection,new_player)).start()

    except Exception as e:
      logging.error(e)
      connection.sendall(str(e.args[0]).encode())
      connection.close()


  def connection_thread(self):
    # 1 create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2 bind socket to the port and ip address, handle exceptions
    try:
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # rapid testing
      s.bind((self.SERVER_IP, self.SERVER_PORT))
    except Exception as e:
      logging.error(e)
      sys.exit()

    # 3 listen for incoming connections
    logging.info(f'Listening for connections on {str(s.getsockname())}')
    s.listen(1)
    while True:
      # 4 accept incoming connections
      connection, address = s.accept()
      logging.info(f'Connection from {address}')
      
      # 5 authenticate the connection
      self.authenticate(connection)



if __name__ == "__main__":
  s = Server()
  thread = threading.Thread(target=s.connection_thread).start()