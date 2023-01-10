from typing import Union

from User import User
from Tracker import Tracker
from PoseChecker import PoseChecker
user_list = dict()

class UserManage:
  @staticmethod
  def add_user(username:str, userType:User, trackerType:Tracker):
    checker = PoseChecker(trackerType, userType)
    user_list[username] = [userType, trackerType, checker]

  @staticmethod
  def remove_user(username:str):
    user_list[username] = None

  @staticmethod
  def get_User_from_username(username:str) -> User:
    if user_list[username]:
      return user_list[username][0]
    return None

  @staticmethod
  def get_Trakcer_from_username(username: str) -> Tracker:
    if user_list[username]:
      return user_list[username][1]
    return None

  @staticmethod
  def get_PoseChecker_from_username(username: str) -> Tracker:
    if user_list[username]:
      return user_list[username][2]
    return None

  @staticmethod
  def get_user_list():
    return user_list

  @staticmethod
  def is_user_in_user_list(username):
    if username in user_list.keys():
      return True
    return False
