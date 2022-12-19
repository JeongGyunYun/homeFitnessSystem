import json

from ViedoController import VideoController
from Tracker import Tracker
from User import User
from solutions import PoseLandmark
from solutions import PoseConnection
from PoseConfidence import PoseConfidence
import util


class PoseChecker:
  def __init__(self, tracker, controller):
    self.tracker: Tracker = tracker
    self.controller: VideoController = controller
    self.wrong_line = set()
    self.ready = None
    self.check = .05
    self.counter = 0
    self.stage = None
    self.wrong = []


  # def square_check(self):
  #

  def set_json_data(self):
    self.json_data = util.json_load(self.controller.get_video_name_without_ex())

  def add_wrong_line(self, connection:PoseConnection):
    self.wrong_line.add(connection)

  def clear_wrong_line(self):
    self.wrong_line.clear()

  def get_wrong_line(self):
    return self.wrong_line

#어깨 영역
  def shoudler_checker(self):
    MAX_ANGLE = 25
    # TODO 어깨인데 잘못 넣어음
    right_shoulder_status = self.right_shoulder_checker(MAX_ANGLE)
    left_shoulder_status = self.left_shoulder_checker(MAX_ANGLE)
    if right_shoulder_status and left_shoulder_status:
      #TODO 실제 구현 True False로 구현
      self.controller.play_video()
    else:
      # Log을 위한 부분
      if not right_shoulder_status:
        self.add_wrong_line(PoseConnection.RIGHT_SHOULDER_TO_RIGHT_ELBOW)
        self.add_wrong_line(PoseConnection.RIGHT_ELBOW_TO_RIGHT_WRIST)
        print("[Log] right problem")
      if not left_shoulder_status:
        self.add_wrong_line(PoseConnection.LEFT_SHOULDER_TO_LEFT_ELBOW)
        self.add_wrong_line(PoseConnection.LEFT_ELBOW_TO_LEFT_WRIST)
        print("[Log] left problem")
      # TODO 실제 구현 True False로 구현
      self.controller.stop_video()

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
    MAX_ANGLE = 30
    right_elbow_status = self.right_elbow_checker(MAX_ANGLE)
    left_elbow_status = self.left_elbow_checker(MAX_ANGLE)
    if right_elbow_status and left_elbow_status:
      #TODO 실제 구현 True False로 구현
      self.controller.play_video()
    else:
      # Log을 위한 부분
      if not right_elbow_status:
        print("[Log] right problem")
      if not left_elbow_status:
        print("[Log] left problem")
      # TODO 실제 구현 True False로 구현
      self.controller.stop_video()

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

  def pushup_preposition_check(self, checkNum) -> bool:
    landmarks = self.tracker.get_result().pose_landmarks.landmark
    LeftShoulder = [landmarks[PoseLandmark.LEFT_SHOULDER].x,
                    landmarks[PoseLandmark.LEFT_SHOULDER].y, landmarks[PoseLandmark.LEFT_SHOULDER].z]
    LeftElbow = [landmarks[PoseLandmark.LEFT_ELBOW].x,
              landmarks[PoseLandmark.LEFT_ELBOW].y, landmarks[PoseLandmark.LEFT_ELBOW].z]
    LeftWrist = [landmarks[PoseLandmark.LEFT_WRIST].x,
              landmarks[PoseLandmark.LEFT_WRIST].y, landmarks[PoseLandmark.LEFT_WRIST].z]
    RightShoulder = [landmarks[PoseLandmark.RIGHT_SHOULDER].x,
                      landmarks[PoseLandmark.RIGHT_SHOULDER].y, landmarks[PoseLandmark.RIGHT_SHOULDER].z]
    RightElbow = [landmarks[PoseLandmark.RIGHT_ELBOW].x,
                  landmarks[PoseLandmark.RIGHT_ELBOW].y, landmarks[PoseLandmark.RIGHT_ELBOW].z]
    RightWrist = [landmarks[PoseLandmark.RIGHT_WRIST].x,
                  landmarks[PoseLandmark.RIGHT_WRIST].y, landmarks[PoseLandmark.RIGHT_WRIST].z]
    LeftHip = [landmarks[PoseLandmark.LEFT_HIP].x,
              landmarks[PoseLandmark.LEFT_HIP].y, landmarks[PoseLandmark.LEFT_HIP].z]
    RightHip = [landmarks[PoseLandmark.RIGHT_HIP].x,
                  landmarks[PoseLandmark.RIGHT_HIP].y, landmarks[PoseLandmark.RIGHT_HIP].z]

    # 양쪽 엉덩이 카메라 평행 맞추기
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

  def squat_preposition_check(self, checkNum) -> bool:

    return True

  def calc_pushup_count(self):
    global angle
    cam_landmark_results = self.tracker.get_result()
    if cam_landmark_results:
      angle = util.get_angel_from_symbol(cam_landmark_results, PoseLandmark.LEFT_SHOULDER,
                                             PoseLandmark.LEFT_ELBOW,
                                             PoseLandmark.LEFT_WRIST)
    if angle < 180 and self.stage == None:
      self.stage = 'down'
    if angle < 110 and self.stage == 'down':
      self.stage = 'up'
    if angle > 170 and self.stage == 'up':
      self.stage = None
      self.counter += 1

  def pushup_position_check(self):
    landmarks = self.tracker.get_result().pose_landmarks.landmark
    LeftShoulder = [landmarks[PoseLandmark.LEFT_SHOULDER].x,
                    landmarks[PoseLandmark.LEFT_SHOULDER].y, landmarks[PoseLandmark.LEFT_SHOULDER].z]
    LeftElbow = [landmarks[PoseLandmark.LEFT_ELBOW].x,
              landmarks[PoseLandmark.LEFT_ELBOW].y, landmarks[PoseLandmark.LEFT_ELBOW].z]
    LeftWrist = [landmarks[PoseLandmark.LEFT_WRIST].x,
              landmarks[PoseLandmark.LEFT_WRIST].y, landmarks[PoseLandmark.LEFT_WRIST].z]
    RightShoulder = [landmarks[PoseLandmark.RIGHT_SHOULDER].x,
                      landmarks[PoseLandmark.RIGHT_SHOULDER].y, landmarks[PoseLandmark.RIGHT_SHOULDER].z]
    RightElbow = [landmarks[PoseLandmark.RIGHT_ELBOW].x,
                  landmarks[PoseLandmark.RIGHT_ELBOW].y, landmarks[PoseLandmark.RIGHT_ELBOW].z]
    RightWrist = [landmarks[PoseLandmark.RIGHT_WRIST].x,
                  landmarks[PoseLandmark.RIGHT_WRIST].y, landmarks[PoseLandmark.RIGHT_WRIST].z]
    LeftHip = [landmarks[PoseLandmark.LEFT_HIP].x,
              landmarks[PoseLandmark.LEFT_HIP].y, landmarks[PoseLandmark.LEFT_HIP].z]
    RightHip = [landmarks[PoseLandmark.RIGHT_HIP].x,
                  landmarks[PoseLandmark.RIGHT_HIP].y, landmarks[PoseLandmark.RIGHT_HIP].z]

    # 양쪽 엉덩이 카메라 평행 맞추기
    if -self.check > LeftHip[2] or LeftHip[2] > self.check or -self.check > RightHip[2] or RightHip[2] > self.check:
      self.wrong.append((23, 24))
    # 양쪽 어깨 손과 z 일치
    if abs(LeftWrist[2] -LeftShoulder[2]) > self.check:
      self.wrong.append((11, 13))
      self.wrong.append((13, 15))
    if abs(RightWrist[2] -RightShoulder[2]) > self.check:
      self.wrong.append((12, 14))
      self.wrong.append((14, 16))
    # 양쪽 어깨 y 값 일치
    if abs(LeftShoulder[1] -RightShoulder[1]) > self.check:
      self.wrong.append((11, 12))
    # 팔꿈치 밖으로 돌아간지 확인
    if abs(LeftElbow[0] - LeftWrist[0]) > self.check:
      self.wrong.append((11, 13))
    if abs(RightElbow[0] - RightWrist[0]) > self.check:
      self.wrong.append((12, 14))
    # 엉덩이 높이
    return self.wrong

  def squat_position_check(self):
    landmarks = self.tracker.get_result().pose_landmarks.landmark
    LeftShoulder = [landmarks[PoseLandmark.LEFT_SHOULDER].x,
                    landmarks[PoseLandmark.LEFT_SHOULDER].y, landmarks[PoseLandmark.LEFT_SHOULDER].z]
    LeftElbow = [landmarks[PoseLandmark.LEFT_ELBOW].x,
              landmarks[PoseLandmark.LEFT_ELBOW].y, landmarks[PoseLandmark.LEFT_ELBOW].z]
    LeftWrist = [landmarks[PoseLandmark.LEFT_WRIST].x,
              landmarks[PoseLandmark.LEFT_WRIST].y, landmarks[PoseLandmark.LEFT_WRIST].z]
    RightShoulder = [landmarks[PoseLandmark.RIGHT_SHOULDER].x,
                      landmarks[PoseLandmark.RIGHT_SHOULDER].y, landmarks[PoseLandmark.RIGHT_SHOULDER].z]
    RightElbow = [landmarks[PoseLandmark.RIGHT_ELBOW].x,
                  landmarks[PoseLandmark.RIGHT_ELBOW].y, landmarks[PoseLandmark.RIGHT_ELBOW].z]
    RightWrist = [landmarks[PoseLandmark.RIGHT_WRIST].x,
                  landmarks[PoseLandmark.RIGHT_WRIST].y, landmarks[PoseLandmark.RIGHT_WRIST].z]
    LeftHip = [landmarks[PoseLandmark.LEFT_HIP].x,
              landmarks[PoseLandmark.LEFT_HIP].y, landmarks[PoseLandmark.LEFT_HIP].z]
    RightHip = [landmarks[PoseLandmark.RIGHT_HIP].x,
                  landmarks[PoseLandmark.RIGHT_HIP].y, landmarks[PoseLandmark.RIGHT_HIP].z]
