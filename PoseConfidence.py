from util import get_angel
import numpy as np


class PoseConfidence:

  def __init__(self):
    self.counter = 0
    self.stage = None
    self.ready = None
    self.check = .1
    self.flag = False
    self.wrong = []

  def pushup_preposition_check(self, ls, rs, le, re, lw, rw, lh, rh):
    # 양쪽 엉덩이 카메라 평행 맞추기
    if -self.check > lh[2] or lh[2] > self.check or -self.check > rh[2] or rh[2] > self.check:
      ready = "Take a position"
      return False
    # 양쪽 손 평행 맞추기
    if abs(lw[2] - rw[2]) > self.check:
      ready = "hand"
      return False
    # 양쪽 어깨 손과 z 일치
    if abs(lw[2] - ls[2]) > self.check or abs(rw[2] - rs[2]) > self.check:
      ready = "shoulder"
      return False
    # 양쪽 손에서 어깨까지 x 간격
    if abs(lw[0] - ls[0]) - abs(rw[0] - rs[0]) > self.check:
      ready = "hands width"
      return False
    # 양쪽 어깨 y 값 일치
    if abs(ls[1] - rs[1]) > self.check:
      ready = "shoulder height"
      return False
    # 팔꿈치 밖으로 돌아간지 확인
    if abs(le[0] - lw[0]) > self.check or abs(re[0] - rw[0]) > self.check:
      ready = "elbow"
      return False
    # 엉덩이 높이 어깨와 일치 -> 어떻게??

    return True

  def pushup_position_check(self, ls, rs, le, re, lw, rw, lh, rh):
    # 양쪽 엉덩이 카메라 평행 맞추기
    if -self.check > lh[2] or lh[2] > self.check or -self.check > rh[2] or rh[2] > self.check:
      self.wrong.append((23, 24))
    # 양쪽 어깨 손과 z 일치
    if abs(lw[2] - ls[2]) > self.check:
      self.wrong.append((11, 13))
      self.wrong.append((13, 15))
    if abs(rw[2] - rs[2]) > self.check:
      self.wrong.append((12, 14))
      self.wrong.append((14, 16))
    # 양쪽 어깨 y 값 일치
    if abs(ls[1] - rs[1]) > self.check:
      self.wrong.append((11, 12))
    # 팔꿈치 밖으로 돌아간지 확인
    if abs(le[0] - lw[0]) > self.check:
      self.wrong.append(11, 13)
    if abs(re[0] - rw[0]) > self.check:
      self.wrong.append(12, 14)
    # 엉덩이 높이
    return self.wrong

  def pushup_calculate_angle(self, a: np.array, b: np.array, c: np.array):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
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
      stage = None
      self.counter += 1

  def set_wrong_connection_list(self, wrong_list):
    self.worng = wrong_list

  # TODO 단순히 self.wrong을 return 하지 않고 계산으로 처리하기/
  def get_wrong_connection_list(self):
    return self.wrong
