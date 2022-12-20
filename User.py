from ViedoController import VideoController

class User:
  def __init__(self, user):
    self.user = user
    self.video_controller = VideoController()
    self.count = 0
    self.sel_train = None

  def set_train_push_up(self):
    self.sel_train = 0

  def set_train_squat(self):
    self.sel_train = 1

  def get_select_train(self):
    return self.sel_train

  def get_controller(self):
    return self.video_controller

  def get_count(self):
    return self.count

  def set_count(self, num):
    self.count = num

  def clear_count(self):
    self.count = 0

  def up_count(self):
    self.count += 1
