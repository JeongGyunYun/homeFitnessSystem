from ViedoController import VideoController

class User:
  def __init__(self, user):
    self.user = user
    self.video_controller = VideoController()

  def get_controller(self):
    return self.video_controller
