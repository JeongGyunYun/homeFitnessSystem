import cv2

class VideoController:
  def __init__(self):
    self.control_flag:bool = True

  def set_video(self, video):
    """
    :param video: 비디오 파일 fullPath 입력
    """
    self.video: str = video
    self.cap = cv2.VideoCapture(self.video)
    self.clear_property()

  def clear_property(self):
    self.status = None
    self.frame = None
    self.control_flag = None

  def load_on_frame(self):
    self.status, self.frame = self.cap.read()

  def play_video_process(self):
    self.load_on_frame()
    return (self.get_status(), self.get_frame())

  def play_load_frame(self):
    self.control_flag = True

  def stop_load_frame(self):
    self.control_flag = False

  def get_frame(self):
    return self.frame

  def get_status(self):
    return self.status

  def get_control_flag(self):
    return self.control_flag

  def get_byte_image(self, frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    byte_frame = jpeg.tobytes()
    return byte_frame
