from User import User
user_list = dict()

class UserManage:
  @staticmethod
  def add_user(username:str, data:User):
    user_list[username] = data

  @staticmethod
  def remove_user(username:str):
    user_list[username] = None

  @staticmethod
  def get_User_from_username(username:str) -> User:
    if user_list[username]:
      return user_list[username]
    return None

  @staticmethod
  def get_user_list():
    return user_list
