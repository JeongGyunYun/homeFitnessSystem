import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

BG_COLOR = (192, 192, 192)  # gray
# For webcam input:
cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
stage = None
ready = None
check = 0.1
flag = False

def pushup_preposition_check(ls, rs, le, re, lw, rw, lh, rh):
  global ready
  # 양쪽 엉덩이 카메라 평행 맞추기
  if -check > lh[2] or lh[2] > check or -check > rh[2] or rh[2] > check:
    ready = "Take a position"
    return False
  # 양쪽 손 평행 맞추기
  if abs(lw[2] - rw[2]) > check:
    ready = "hand"
    return False
  # 양쪽 어깨 손과 z 일치
  if abs(lw[2] - ls[2]) > check or abs(rw[2] - rs[2]) > check:
    ready = "shoulder"
    return False
  # 양쪽 손에서 어깨까지 x 간격
  if abs(lw[0] - ls[0]) - abs(rw[0] - rs[0]) > check:
    ready = "hands width"
    return False
  # 양쪽 어깨 y 값 일치
  if abs(ls[1] - rs[1]) > check:
    ready = "shoulder height"
    return False
  # 팔꿈치 밖으로 돌아간지 확인
  if abs(le[0] - lw[0]) > check or abs(re[0] - rw[0]) > check:
    ready = "elbow"
    return False
  # 엉덩이 높이 어깨와 일치 -> 어떻게??

  return True

def pushup_position_check(ls, rs, le, re, lw, rw, lh, rh):
  wrong = []
  # 양쪽 엉덩이 카메라 평행 맞추기
  if -check > lh[2] or lh[2] > check or -check > rh[2] or rh[2] > check:
    wrong.append((23, 24))
  # 양쪽 어깨 손과 z 일치
  if abs(lw[2] - ls[2]) > check:
    wrong.append((11, 13))
    wrong.append((13, 15))
  if abs(rw[2] - rs[2]) > check:
    wrong.append((12, 14))
    wrong.append((14, 16))
  # 양쪽 어깨 y 값 일치
  if abs(ls[1] - rs[1]) > check:
    wrong.append((11, 12))
  # 팔꿈치 밖으로 돌아간지 확인
  if abs(le[0] - lw[0]) > check:
    wrong.append(11,13)
  if abs(re[0] - rw[0]) > check:
    wrong.append(12,14)
  # 엉덩이 높이

  return wrong

def pushup_calculate_angle(a, b, c):
  a = np.array(a) # First
  b = np.array(b) # Mid
  c = np.array(c) # End
  
  radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
  angle = np.abs(radians*180.0/np.pi)
  
  if angle >180.0:
      angle = 360-angle
      
  return angle 

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
      success, image = cap.read()
      if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      # Make detection
      results = pose.process(image)

      # Draw the pose annotation on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      # Extract landmarks
      try:
        landmarks = results.pose_landmarks.landmark
        # print(landmarks)

        # Get coordinates
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        
        # print(left_shoulder, right_shoulder)
        # print(left_elbow, right_elbow)
        # print(left_wrist, right_wrist)
        # print(left_hip, right_hip)
        # print()
        
        if flag == False:
          flag = pushup_preposition_check(left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_elbow, left_hip, right_hip)
        else :
          # Calculate angle
          angle = pushup_calculate_angle(left_shoulder, left_elbow, left_wrist)
          # print(angle)
          
          wrong = pushup_position_check(left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_elbow, left_hip, right_hip)
          
          # Visualize angle
          # cv2.putText(image, str(angle),
          #               tuple(np.multiply(elbow, [640, 480]).astype(int)),
          #               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
          #                     )
          
          # Curl counter logic
          if angle < 180 and stage == None:
            stage = 'down'
          if angle < 110 and stage == 'down':
            stage='up'
          if angle > 170 and stage == 'up':
            stage = None
            counter += 1

      except:
          pass
        
      # ready message
      cv2.putText(image, ready, (240, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

      # Render curl counter
      # Setup status box
      cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

      # Rep data
      cv2.putText(image, 'REPS', (15, 12),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
      cv2.putText(image, str(counter),
                  (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

      # Stage data
      cv2.putText(image, 'STAGE', (65, 12),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
      cv2.putText(image, stage,
                  (60, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

      # Render detections
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                              mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )   
      
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Pose', image)

      if cv2.waitKey(10) & 0xFF == ord('q'):
          break
          
cap.release()
cv2.destroyAllWindows()