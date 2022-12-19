from util import get_angel
import numpy as np


class PoseConfidence:

  def __init__(self):
    self.counter = 0
    self.stage = None
    self.ready = None
    self.check = .01
    self.flag = False
    self.wrong = []

  def pushup_preposition_check(self, checkNum, LeftShoulder, RightShoulder, LeftElbow, RightElbow, LeftWrist, RightWrist, LeftHip, RightHip):
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
    # 엉덩이 높이 어깨와 일치 -> 어떻게??

    return True

  def pushup_position_check(self,LeftShoulder,RightShoulder, LeftElbow, RightElbow, LeftWrist, RightWrist, LeftHip, RightHip):
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

  def pushup_calculate_angle(self, LeftShoulder, LeftElbow, LeftWrist):
    radians = np.arctan2(LeftWrist[1] - LeftElbow[1], LeftWrist[0] - LeftElbow[0]) - np.arctan2(LeftShoulder[1] - LeftElbow[1], LeftShoulder[0] - LeftElbow[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
      angle = 360 - angle

    return angle

  def calc_pushup_count(self, angle):
    if angle < 180 and self.stage == None:
      self.stage = 'down'
    if angle < 110 and self.stage == 'down':
      self.stage = 'up'
    if angle > 170 and self.stage == 'up':
      self.stage = None
      self.counter += 1

  def set_wrong_connection_list(self, wrong_list):
    self.wrong = wrong_list

  # TODO 단순히 self.wrong을 return 하지 않고 계산으로 처리하기/
  def get_wrong_connection_list(self):
    return self.wrong
