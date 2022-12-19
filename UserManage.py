from User import User

class Singleton(object):
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls, *args, **kwargs).__new__(cls, *args, **kwargs)
    return cls.instance

class UserManage(Singleton):
  def __init__(self):
    self.user_list = dict()

  def add_user(self, username:str, data:User):
    self.user_list[username] = data

  def remove_user(self, username:str):
    self.user_list[username] = None
