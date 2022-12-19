from Tracker import Tracker
from Annotation import Annotation
from solutions import PoseConnection
from PoseConfidence import PoseConfidence
import mediapipe as mp
from util import *

mp_pose = mp.solutions.pose

BG_COLOR = (192, 192, 192)  # gray

# # Curl counter variables
# counter = 0
# stage = None
# ready = None
# check = 0.1
# flag = False
# # Def
# def pushup_preposition_check(ls, rs, le, re, lw, rw, lh, rh):
#   global ready
#   # 양쪽 엉덩이 카메라 평행 맞추기
#   if -check > lh[2] or lh[2] > check or -check > rh[2] or rh[2] > check:
#     ready = "Take a position"
#     return False
#   # 양쪽 손 평행 맞추기
#   if abs(lw[2] - rw[2]) > check:
#     ready = "hand"
#     return False
#   # 양쪽 어깨 손과 z 일치
#   if abs(lw[2] - ls[2]) > check or abs(rw[2] - rs[2]) > check:
#     ready = "shoulder"
#     return False
#   # 양쪽 손에서 어깨까지 x 간격
#   if abs(lw[0] - ls[0]) - abs(rw[0] - rs[0]) > check:
#     ready = "hands width"
#     return False
#   # 양쪽 어깨 y 값 일치
#   if abs(ls[1] - rs[1]) > check:
#     ready = "shoulder height"
#     return False
#   # 팔꿈치 밖으로 돌아간지 확인
#   if abs(le[0] - lw[0]) > check or abs(re[0] - rw[0]) > check:
#     ready = "elbow"
#     return False
#   # 엉덩이 높이 어깨와 일치 -> 어떻게??
#
#   return True
#
#
# def pushup_position_check(ls, rs, le, re, lw, rw, lh, rh):
#   wrong = []
#   # 양쪽 엉덩이 카메라 평행 맞추기
#   if -check > lh[2] or lh[2] > check or -check > rh[2] or rh[2] > check:
#     wrong.append((23, 24))
#   # 양쪽 어깨 손과 z 일치
#   if abs(lw[2] - ls[2]) > check:
#     wrong.append((11, 13))
#     wrong.append((13, 15))
#   if abs(rw[2] - rs[2]) > check:
#     wrong.append((12, 14))
#     wrong.append((14, 16))
#   # 양쪽 어깨 y 값 일치
#   if abs(ls[1] - rs[1]) > check:
#     wrong.append((11, 12))
#   # 팔꿈치 밖으로 돌아간지 확인
#   if abs(le[0] - lw[0]) > check:
#     wrong.append(11, 13)
#   if abs(re[0] - rw[0]) > check:
#     wrong.append(12, 14)
#   # 엉덩이 높이
#
#   return wrong
#
#
# def pushup_calculate_angle(a, b, c):
#   a = np.array(a)  # First
#   b = np.array(b)  # Mid
#   c = np.array(c)  # End
#
#   radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#   angle = np.abs(radians * 180.0 / np.pi)
#
#   if angle > 180.0:
#     angle = 360 - angle
#
#   return angle


if __name__ == "__main__":
  webcam = Tracker("custom", dev_info=0)
  annotation = Annotation()
  poseConfidence = PoseConfidence()

  while webcam.is_cap_open():
    success, image = webcam.read()

    # Normal Set
    if not success:
      print("Ignore")
      break

    results = webcam.get_pose_results()
    connection_style = annotation.make_connection_style_from_result()

    # Extract landmarks
    if results.pose_landmarks:
      # print(landmarks)

      # Get coordinates
      # left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
      #                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
      #                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
      # left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
      #               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
      #               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
      # left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
      #               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
      #               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]
      # right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
      #                   landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
      #                   landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
      # right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
      #                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
      #                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]
      # right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
      #                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
      #                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]
      # left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
      #             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z]
      # right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
      #              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]
      # elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
      left_shoulder = convert_landmark_to_array(results, PoseLandmark.LEFT_SHOULDER)
      left_elbow = convert_landmark_to_array(results, PoseLandmark.LEFT_ELBOW)
      left_wrist = convert_landmark_to_array(results, PoseLandmark.LEFT_WRIST)
      right_shoulder = convert_landmark_to_array(results, PoseLandmark.RIGHT_SHOULDER)
      right_elbow = convert_landmark_to_array(results, PoseLandmark.RIGHT_ELBOW)
      right_wrist = convert_landmark_to_array(results, PoseLandmark.RIGHT_WRIST)
      left_hip = convert_landmark_to_array(results, PoseLandmark.LEFT_HIP)
      right_hip = convert_landmark_to_array(results, PoseLandmark.RIGHT_HIP)

      if not poseConfidence.flag:
        poseConfidence.flag = poseConfidence.pushup_preposition_check(left_shoulder, right_shoulder, left_elbow,
                                                                      right_elbow, left_wrist, right_elbow,
                                                                      left_hip, right_hip)
        print("False")
      else:
        angle = poseConfidence.pushup_calculate_angle(left_shoulder, left_elbow, left_wrist)
        # print(angle)

        poseConfidence.set_wrong_connection_list(
          poseConfidence.pushup_position_check(left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist,
                                               right_elbow,
                                               left_hip, right_hip))

        # Curl counter logic
        poseConfidence.calc_pushup_count(angle)
        print("True")
    ##Test Code
    # #TestCode 임의로 주어진 result 값
    # if webcam.get_right_shoulder_angle():
    #   if webcam.get_right_shoulder_angle() > 90:
    #     annotation.make_connection_style_from_result([PoseConnection.RIGHT_SHOULDER_TO_RIGHT_ELBOW])

      annotation.make_connection_style_from_result(poseConfidence.get_wrong_connection_list())

    webcam.draw_annotation(landmark_list=results.pose_landmarks, connections=annotation.pose_connections,
                           connection_drawing_spec=connection_style)

    webcam.show()

  webcam.pose_close()
  webcam.release()