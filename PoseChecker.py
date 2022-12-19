import json

from ViedoController import VideoController
from Tracker import Tracker
from solutions import PoseLandmark
import util


class PoseChecker:
  def __init__(self, tracker, controller):
    self.tracker: Tracker = tracker
    self.controller: VideoController = controller

  @staticmethod
  def test(tracker: Tracker, controller: VideoController):
    # TODO 값이 None일 때 처리해야
    if tracker.get_right_elbow_angle():
      if (tracker.get_right_elbow_angle() > 90):
        controller.stop_video()
      else:
        controller.play_video()

  def set_json_data(self):
    self.json_data = util.json_load(self.controller.get_video_name_without_ex())

  def play(self):
    MAX_ANGLE = 20
    diff_right_elbow = self.diff_right_elbow_angle(self.tracker.get_result(),
                                        self.json_data[str(self.controller.get_frame_number())])
    if diff_right_elbow is None or diff_right_elbow > MAX_ANGLE:
      if diff_right_elbow is None:
        print(f"[Log] Nan")
      else:
        print(f"[Log] Big Diff Angle")
      self.controller.stop_video()
    else:
      self.controller.play_video()


  def diff_right_elbow_angle(self, cam_landmark_results, video_landmark_one_frame):
    global cam_angel, vid_angel
    if cam_landmark_results:
      cam_angel = util.get_angel_from_symbol(cam_landmark_results, PoseLandmark.RIGHT_SHOULDER,
                                             PoseLandmark.RIGHT_ELBOW,
                                             PoseLandmark.RIGHT_WRIST)
    if video_landmark_one_frame:
      vid_angel = util.get_angel_from_jsonType(video_landmark_one_frame, PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_ELBOW,
                                               PoseLandmark.RIGHT_WRIST)

    if cam_angel is not None and vid_angel is not None:
      return abs(cam_angel - vid_angel)


  def left_elbow_check(self):
    None
