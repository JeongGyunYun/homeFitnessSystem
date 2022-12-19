import cv2
import mediapipe as mp
import numpy as np
from PoseConfidence import PoseConfidence

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

BG_COLOR = (192, 192, 192)  # gray
# For webcam input:
cap = cv2.VideoCapture(0)

poseCheck = PoseConfidence()
flag = False
checkNum = 0

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
        
        if checkNum < 6:
          if flag == False:
            flag = poseCheck.pushup_preposition_check(checkNum, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_elbow, left_hip, right_hip)
            print(poseCheck.ready)
            print(flag)
          else :
            checkNum += 1
            flag = False
            print(checkNum)
        else :
          wrong = poseCheck.pushup_position_check(left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_elbow, left_hip, right_hip)    
          
          # Calculate angle
          angle = poseCheck.pushup_calculate_angle(left_shoulder, left_elbow, left_wrist)
          # # Visualize angle
          # cv2.putText(image, str(angle),
          #             tuple(np.multiply(elbow, [640, 480]).astype(int)),
          #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
          #                   )
          poseCheck.calc_pushup_count(angle)
          
      except:
          pass
        
      # print(wrong)
      
      # Render detections
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                              mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )   
      image =  cv2.flip(image, 1)
      
      # ready message
      cv2.putText(image, poseCheck.ready, (300, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

      # Render curl counter
      # Setup status box
      cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

      # Rep data
      cv2.putText(image, 'REPS', (15, 12),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
      cv2.putText(image, str(poseCheck.counter),
                  (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

      # Stage data
      cv2.putText(image, 'STAGE', (65, 12),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
      cv2.putText(image, poseCheck.stage,
                  (60, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
      
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Pose', image)

      if cv2.waitKey(10) & 0xFF == ord('q'):
          break
          
cap.release()
cv2.destroyAllWindows()