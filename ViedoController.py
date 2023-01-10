import cv2
import os

class VideoController:
  def __init__(self):
    self.control_flag: bool = False
    self.max_loop_count = 1

  def set_video(self, video):
    """
    :param video: 비디오 파일 fullPath 입력
    """
    self.video: str = video
    self.cap = cv2.VideoCapture(self.video)
    self.clear_property()

  def get_video_name_without_ex(self):
    basename = os.path.basename(self.video)
    name, ext = basename.split(".")
    return name

  def set_max_loop_count(self, n):
    self.max_loop_count = n
    self.cur_loop_count = 1

  def set_frame_to_start(self):
    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)

  def count_loop(self):
    self.cur_loop_count += 1

  def is_end_loop(self) -> bool:
    if self.cur_loop_count >= self.max_loop_count:
      return True
    return False

  def clear_property(self):
    self.status = None
    self.frame = None
    self.frame_no = None
    self.control_flag = False

  def load_on_frame(self):
    self.status, self.frame = self.cap.read()

  def play_video_process(self):
    self.load_on_frame()
    return (self.get_status(), self.get_frame())

  def play_video(self):
    self.control_flag = True

  def stop_video(self):
    self.control_flag = False

  def get_frame_number(self):
    return int(self.cap.get(1))

  def get_frame(self):
    return self.frame

  def get_status(self):
    return self.status

  def get_control_flag(self):
    return self.control_flag

  def get_byte_image(self, frame):
    frame = cv2.flip(frame, 1)
    frame = cv2.flip(frame, 0)
    ret, jpeg = cv2.imencode('.jpg', frame)
    byte_frame = jpeg.tobytes()
    return byte_frame
