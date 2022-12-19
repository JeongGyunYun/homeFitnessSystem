import threading

from Annotation import Annotation
from PoseConfidence import PoseConfidence
from Tracker import Tracker
from util import *


class Application(threading.Thread):
  def __init__(self, device: Tracker):
    super(Application, self).__init__()
    self.device = device
    self.annotation = Annotation()
    self.poseConfidence = PoseConfidence()

  def run(self):
    while self.device.is_cap_open():
      success, image = self.device.read()

      # webcam일때는 continue file일때는 break
      if not success:
        print("Ignore")
        break

      results = self.device.get_pose_results()
      connection_style = self.annotation.make_connection_style_from_result()

      if results.pose_landmarks:
        left_shoulder = convert_landmark_to_array(results, PoseLandmark.LEFT_SHOULDER)
        left_elbow = convert_landmark_to_array(results, PoseLandmark.LEFT_ELBOW)
        left_wrist = convert_landmark_to_array(results, PoseLandmark.LEFT_WRIST)
        right_shoulder = convert_landmark_to_array(results, PoseLandmark.RIGHT_SHOULDER)
        right_elbow = convert_landmark_to_array(results, PoseLandmark.RIGHT_ELBOW)
        right_wrist = convert_landmark_to_array(results, PoseLandmark.RIGHT_WRIST)
        left_hip = convert_landmark_to_array(results, PoseLandmark.LEFT_HIP)
        right_hip = convert_landmark_to_array(results, PoseLandmark.RIGHT_HIP)

        if not self.poseConfidence.flag:
          self.poseConfidence.flag = self.poseConfidence.pushup_preposition_check(left_shoulder, right_shoulder,
                                                                                  left_elbow,
                                                                                  right_elbow, left_wrist, right_elbow,
                                                                                  left_hip, right_hip)
          print("False")
        else:
          angle = self.poseConfidence.pushup_calculate_angle(left_shoulder, left_elbow, left_wrist)
          self.poseConfidence.set_wrong_connection_list(
            self.poseConfidence.pushup_position_check(left_shoulder, right_shoulder, left_elbow, right_elbow,
                                                      left_wrist,
                                                      right_elbow,
                                                      left_hip, right_hip))
          self.poseConfidence.calc_pushup_count(angle)
          print("True")
        self.annotation.make_connection_style_from_result(self.poseConfidence.get_wrong_connection_list())

      self.device.draw_annotation(landmark_list=results.pose_landmarks, connections=self.annotation.pose_connections,
                                  connection_drawing_spec=connection_style)

      self.device.show()

    self.device.release()
