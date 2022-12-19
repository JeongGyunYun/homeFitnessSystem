from ViedoController import VideoController
from Tracker import Tracker

class PoseChecker:
  @staticmethod
  def test(tracker: Tracker, controller: VideoController):
    #TODO 값이 None일 때 처리해야
    if tracker.get_right_elbow_angle():
      if(tracker.get_right_elbow_angle() > 90):
        controller.stop_video()
      else:
        controller.play_video()


  def is_pose_right(self, video_name, frameNo, cam_result):
    None
