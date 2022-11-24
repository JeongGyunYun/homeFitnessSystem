import cv2
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec
import util
from solutions import PoseLandmark

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)


class Tracker:
  def __init__(self, dev_info, win_name=" "):
    self.pose = mp_pose.Pose(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
    )
    self.dev_info = dev_info
    self.cap = cv2.VideoCapture(self.dev_info)
    print(f"Tracker Device name = {self.dev_info} ")
    self.win_name = win_name

  def get_window_name(self):
    return self.win_name

  def read(self):
    self.success, self.image = self.cap.read()
    return self.success, self.image

  def read_image(self):
    self.success, self.image = self.cap.read()
    return self.image

  def is_cap_open(self):
    return self.cap.isOpened()

  def get_pose_results(self, image=None):
    if image == None:
      image = self.image

    image.flags.writeable = False
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = self.pose.process(image)
    self.results = results
    return self.results

  def draw_annotation(self, landmark_list, connections,
                      landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(), connection_drawing_spec=DrawingSpec()):

    self.image.flags.writeable = True
    # self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
      self.image,
      landmark_list=landmark_list,
      connections=connections,
      landmark_drawing_spec=landmark_drawing_spec,
      connection_drawing_spec=connection_drawing_spec
    )
    return self.image

  def show(self, image=None):
    # if image == None:
    #   image = self.image
    cv2.imshow(self.win_name, cv2.flip(self.image, 1))
    cv2.waitKey(1)

  def get_right_elbow_angle(self, results=None):
    if results == None:
      results = self.results
    angle = util.get_angel_from_symbol(results, PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW,
                               PoseLandmark.RIGHT_WRIST)
    return angle

  def get_left_elbow_angle(self, results=None):
    if results == None:
      results = self.results
    angle = util.get_angel_from_symbol(results, PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_ELBOW,
                               PoseLandmark.LEFT_WRIST)
    return angle

  def get_right_shoulder_angle(self):
    angle = util.get_angel_from_symbol(self.results, PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_SHOULDER,
                               PoseLandmark.RIGHT_HIP)
    return angle

  def get_left_shoulder_angle(self):
    angle = util.get_angel_from_symbol(self.results, PoseLandmark.LEFT_ELBOW,PoseLandmark.LEFT_SHOULDER,
                               PoseLandmark.LEFT_HIP)
    return angle

  def pose_close(self):
    self.pose.close()

  def release(self):
    self.pose_close()
    self.cap.release()
