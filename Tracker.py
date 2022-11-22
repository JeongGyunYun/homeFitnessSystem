import cv2
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import DrawingSpec

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)

class Tracker:
  def __init__(self, win_name, dev_info=0, path=""):
    self.pose = mp_pose.Pose(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
    )
    self.cap = cv2.VideoCapture(0)
    self.win_name = win_name

  def read(self):
    return self.cap.read()


  def is_cap_open(self):
    return self.cap.isOpened()

  def get_pose_results(self, image):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = self.pose.process(image)
    return results

  def draw_annotation(self, image, results, landmark_list, connections,
                      landmark_drawing_spec=DrawingSpec(color=RED_COLOR), connection_drawing_spec=DrawingSpec()):
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
      image,
      landmark_list=results.pose_landmarks,
      connections=mp_pose.POSE_CONNECTIONS,
      landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
      connection_drawing_spec=connection_drawing_spec
    )
    return image

  def show(self, image):
    cv2.imshow(self.win_name, cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      None

  def pose_close(self):
    self.pose.close()

  def release(self):
    self.cap.release()
