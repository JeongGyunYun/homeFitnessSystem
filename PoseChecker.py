import json

from ViedoController import VideoController
from Tracker import Tracker
from User import User
from solutions import PoseLandmark
from solutions import PoseConnection
from PoseConfidence import PoseConfidence
import util


class PoseChecker:
  def __init__(self, tracker, user):
    self.user: User = user
    self.tracker: Tracker = tracker
    self.controller: VideoController = user.get_controller()
    self.before_push_flag = False
    self.checkNum = 0
    self.async_line = set()
    self.ready = None
    self.check = .75
    self.counter = 0
    self.stage = None
    self.wrong_line = set()
    self.is_pre_pose = False

  def stop_video(self):
    self.controller.stop_video()
  def play_video(self):
    self.controller.play_video()

  def set_json_data(self):
    self.json_data = util.json_load(self.controller.get_video_name_without_ex())

  def add_async_line(self, connection:PoseConnection):
    self.async_line.add(connection)

  def clear_async_line(self):
    self.async_line.clear()

  def get_async_line(self):
    return self.async_line

#어깨 영역
  def shoudler_checker(self):
    MAX_ANGLE = 35
    right_shoulder_status = self.right_shoulder_checker(MAX_ANGLE)
    left_shoulder_status = self.left_shoulder_checker(MAX_ANGLE)
    if right_shoulder_status and left_shoulder_status:
      #TODO 실제 구현 True False로 구현
      return True
    else:
      # Log을 위한 부분
      if not right_shoulder_status:
        self.add_async_line(PoseConnection.RIGHT_SHOULDER_TO_RIGHT_ELBOW)
        self.add_async_line(PoseConnection.RIGHT_SHOULDER_TO_RIGHT_HIP)
        print("[Log] right shoulder problem")
      if not left_shoulder_status:
        self.add_async_line(PoseConnection.LEFT_SHOULDER_TO_LEFT_ELBOW)
        self.add_async_line(PoseConnection.LEFT_SHOULDER_TO_LEFT_HIP)
        print("[Log] left shoulder problem")
      # TODO 실제 구현 True False로 구현
      return False

  def diff_left_shoulder_angle(self, cam_landmark_results, video_landmark_one_frame):
    """
        왼쪽 어깨 각도 반환
    """
    global cam_angel, vid_angel
    if cam_landmark_results:
      cam_angel = util.get_angel_from_symbol(cam_landmark_results, PoseLandmark.LEFT_HIP,
                                             PoseLandmark.LEFT_SHOULDER,
                                             PoseLandmark.LEFT_ELBOW)
    if video_landmark_one_frame:
      vid_angel = util.get_angel_from_jsonType(video_landmark_one_frame, PoseLandmark.LEFT_HIP,
                                             PoseLandmark.LEFT_SHOULDER,
                                             PoseLandmark.LEFT_ELBOW)

    if cam_angel is not None and vid_angel is not None:
      return abs(cam_angel - vid_angel)


  def diff_right_shoulder_angle(self, cam_landmark_results, video_landmark_one_frame):
    """
        오른쪽 어깨 각도 반환
    """
    global cam_angel, vid_angel
    if cam_landmark_results:
      cam_angel = util.get_angel_from_symbol(cam_landmark_results, PoseLandmark.RIGHT_HIP,
                                             PoseLandmark.RIGHT_SHOULDER,
                                             PoseLandmark.RIGHT_ELBOW)
    if video_landmark_one_frame:
      vid_angel = util.get_angel_from_jsonType(video_landmark_one_frame, PoseLandmark.RIGHT_HIP,
                                             PoseLandmark.RIGHT_SHOULDER,
                                             PoseLandmark.RIGHT_ELBOW)

    if cam_angel is not None and vid_angel is not None:
      return abs(cam_angel - vid_angel)


  def left_shoulder_checker(self, max_angle) -> bool:
    """
    왼쪽 어깨의 각도측정 후 각도 차이가 max_angle보다 커지면 False을 반환
    :param max_angle:
    :return: max_angle보다 각도가 크면 False
    """
    MAX_ANGLE = max_angle
    diff_left_shoulder = self.diff_left_shoulder_angle(self.tracker.get_result(),
                                                 self.json_data[str(self.controller.get_frame_number())])
    if diff_left_shoulder is None or diff_left_shoulder > MAX_ANGLE:
      return False
    return True


  def right_shoulder_checker(self, max_angle) -> bool:
    """
    오른쪽 어깨의 각도측정 후 각도 차이가 max_angle보다 커지면 False을 반환
    :param max_angle:
    :return: max_angle보다 각도가 크면 False
    """
    MAX_ANGLE = max_angle
    diff_shoulder_shoulder = self.diff_right_shoulder_angle(self.tracker.get_result(),
                                                 self.json_data[str(self.controller.get_frame_number())])
    if diff_shoulder_shoulder is None or diff_shoulder_shoulder > MAX_ANGLE:
      return False
    return True

#팔꿈치 Checker
  def elbow_checker(self):
    MAX_ANGLE = 35
    right_elbow_status = self.right_elbow_checker(MAX_ANGLE)
    left_elbow_status = self.left_elbow_checker(MAX_ANGLE)
    if right_elbow_status and left_elbow_status:
      #TODO 실제 구현 True False로 구현
      return True
    else:
      # Log을 위한 부분
      if not right_elbow_status:
        self.add_async_line(PoseConnection.RIGHT_SHOULDER_TO_RIGHT_ELBOW)
        self.add_async_line(PoseConnection.RIGHT_ELBOW_TO_RIGHT_WRIST)
        print("[Log] right elbow problem")
      if not left_elbow_status:
        self.add_async_line(PoseConnection.LEFT_SHOULDER_TO_LEFT_ELBOW)
        self.add_async_line(PoseConnection.LEFT_ELBOW_TO_LEFT_WRIST)
        print("[Log] left elbow problem")
      # TODO 실제 구현 True False로 구현
      return False

  def right_elbow_checker(self, max_angle) -> bool:
    """
    오른쪽 팔꿈치의 각도측정 후 각도 차이가 max_angle보다 커지면 False을 반환
    :param max_angle:
    :return: max_angle보다 각도가 크면 False
    """
    MAX_ANGLE = max_angle
    diff_right_elbow = self.diff_right_elbow_angle(self.tracker.get_result(),
                                                   self.json_data[str(self.controller.get_frame_number())])

    if diff_right_elbow is None or diff_right_elbow > MAX_ANGLE:
      return False
    return True


  def left_elbow_checker(self, max_angle) -> bool:
    """
    왼쪽 팔꿈치의 각도측정 후 각도 차이가 max_angle보다 커지면 False을 반환
    :param max_angle:
    :return: max_angle보다 각도가 크면 False
    """
    MAX_ANGLE = max_angle
    diff_left_elbow = self.diff_left_elbow_angle(self.tracker.get_result(),
                                                   self.json_data[str(self.controller.get_frame_number())])
    if diff_left_elbow is None or diff_left_elbow > MAX_ANGLE:
      return False

    return True


  def diff_right_elbow_angle(self, cam_landmark_results, video_landmark_one_frame):
    """
    오른쪽 팔꿈치 각도 반환
    """
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


  def diff_left_elbow_angle(self, cam_landmark_results, video_landmark_one_frame):
    """
        왼쪽 팔꿈치 각도 반환
    """
    global cam_angel, vid_angel
    if cam_landmark_results:
      cam_angel = util.get_angel_from_symbol(cam_landmark_results, PoseLandmark.LEFT_SHOULDER,
                                             PoseLandmark.LEFT_ELBOW,
                                             PoseLandmark.LEFT_WRIST)
    if video_landmark_one_frame:
      vid_angel = util.get_angel_from_jsonType(video_landmark_one_frame, PoseLandmark.LEFT_SHOULDER,
                                               PoseLandmark.LEFT_ELBOW,
                                               PoseLandmark.LEFT_WRIST)

    if cam_angel is not None and vid_angel is not None:
      return abs(cam_angel - vid_angel)

  def clac_angle(self, cam_landmark_results, video_landmark_one_frame, point1: PoseLandmark, point2: PoseLandmark,
                 point3: PoseLandmark):
    """
    카메라 각도와 비디오 각도를 p1, p2, p3을 이용해 출력
    :param cam_landmark_results:
    :param video_landmark_one_frame:
    :param point1:
    :param point2:
    :param point3:
    :return:
    """
    global cam_angel, vid_angel
    if cam_landmark_results:
      cam_angel = util.get_angel_from_symbol(cam_landmark_results, point1, point2, point3)

    if video_landmark_one_frame:
      vid_angel = util.get_angel_from_jsonType(video_landmark_one_frame, point1, point2, point3)

    return (cam_angel, vid_angel)

  def pushup_preposition_check(self) -> bool:
    checkNum = self.checkNum
    results = self.tracker.get_result()

    LeftShoulder = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_SHOULDER)
    LeftElbow = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_ELBOW)
    LeftWrist = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_WRIST)
    RightShoulder = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_SHOULDER)
    RightElbow = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_ELBOW)
    RightWrist = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_WRIST)
    LeftHip = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_HIP)
    RightHip = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_HIP)

    # 양쪽 엉덩이 카메라 평행 맞추기
    try:
      if checkNum == 0:
        self.ready = "Take a position"
        if -self.check > LeftHip[2] or LeftHip[2] > self.check or -self.check > RightHip[2] or RightHip[2] > self.check:
          return False
      elif checkNum == 1:
        # 양쪽 손 평행 맞추기
        self.ready = "hand"
        if abs(LeftWrist[2] - RightWrist[2]) > self.check:
          return False
      elif checkNum == 2:
        # 양쪽 어깨 손과 z 일치
        self.ready = "shoulder"
        if abs(LeftWrist[2] -LeftShoulder[2]) > self.check or abs(RightWrist[2] -RightShoulder[2]) > self.check:
          return False
      elif checkNum == 3:
      # 양쪽 손에서 어깨까지 x 간격
        if abs(LeftWrist[0] -LeftShoulder[0]) - abs(RightWrist[0] -RightShoulder[0]) > self.check:
          self.ready = "hands width"
          return False
      elif checkNum == 4:
      # 양쪽 어깨 y 값 일치
        self.ready = "shoulder height"
        if abs(LeftShoulder[1] -RightShoulder[1]) > self.check:
          return False
      # 팔꿈치 밖으로 돌아간지 확인
      elif checkNum == 5:
        self.ready = "elbow"
        if abs(LeftElbow[0] - LeftWrist[0]) > self.check or abs(RightElbow[0] - RightWrist[0]) > self.check:
          return False
      return True
    except:
      return False

  def squat_preposition_check(self, checkNum) -> bool:

    return True

  def calc_pushup_count(self):
    global angle
    print(self.stage)
    cam_landmark_results = self.tracker.get_result()
    if cam_landmark_results:
      angle = util.get_angel_from_symbol(cam_landmark_results, PoseLandmark.LEFT_SHOULDER,
                                             PoseLandmark.LEFT_ELBOW,
                                             PoseLandmark.LEFT_WRIST)
    try:
      if angle < 180 and self.stage == None:
        self.stage = 'down'
      if angle < 110 and self.stage == 'down':
        self.stage = 'up'
      if angle > 170 and self.stage == 'up':
        self.stage = None
        self.user.up_count()
        print(self.user.get_count())
    except:
      None


  def check_before_pushup(self):
    if self.checkNum < 6:
      if not self.before_push_flag:
        self.before_push_flag = self.pushup_preposition_check()
      else:
        self.checkNum += 1
        self.before_push_flag = False
        print(f"[Log]Pre Pose State Ready{self.ready}")
        print(f"[Log]Pre Pose State CheckNum{self.checkNum}")
    else:
      self.is_pre_pose = True


  def is_ready_push_up(self):
    return self.is_pre_pose


  def check_wrong_push_up_pose(self):
    results = self.tracker.get_result()

    LeftShoulder = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_SHOULDER)
    LeftElbow = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_ELBOW)
    LeftWrist = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_WRIST)
    RightShoulder = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_SHOULDER)
    RightElbow = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_ELBOW)
    RightWrist = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_WRIST)
    LeftHip = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.LEFT_HIP)
    RightHip = util.get_one_landmark_by_PoseLandMark(results, PoseLandmark.RIGHT_HIP)

    try:
      # 양쪽 엉덩이 카메라 평행 맞추기
      if -self.check > LeftHip[2] or LeftHip[2] > self.check or -self.check > RightHip[2] or RightHip[2] > self.check:
        self.wrong_line.add((23, 24))
      # 양쪽 어깨 손과 z 일치
      if abs(LeftWrist[2] -LeftShoulder[2]) > self.check:
        self.wrong_line.add((11, 13))
        self.wrong_line.add((13, 15))
      if abs(RightWrist[2] -RightShoulder[2]) > self.check:
        self.wrong_line.add((12, 14))
        self.wrong_line.add((14, 16))
      # 양쪽 어깨 y 값 일치
      if abs(LeftShoulder[1] -RightShoulder[1]) > self.check:
        self.wrong_line.add((11, 12))
      # 팔꿈치 밖으로 돌아간지 확인
      if abs(LeftElbow[0] - LeftWrist[0]) > self.check:
        self.wrong_line.add((11, 13))
      if abs(RightElbow[0] - RightWrist[0]) > self.check:
        self.wrong_line.add((12, 14))
      # 엉덩이 높이
    except:
      None

  def get_wrong_line(self):
    return self.wrong_line

  def clear_wrong_line(self):
    self.wrong_line.clear()
