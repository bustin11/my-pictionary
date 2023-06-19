import threading

class ChatBox(object):
  def __init__(self):
    self.chat_history = []
    self.chat_history_lock = threading.Lock()

  def add_message(self, message):
    with self.chat_history_lock:
      self.chat_history.append(message) 
  
  def get_messages(self):
    with self.chat_history_lock:
      return self.chat_history

  def get_chat(self):
    return self.chat_history

  def clear(self):
    self.chat_history = []