from typing import Mapping, Tuple

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from solutions import PoseLandmark

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def helllo() -> Mapping[Tuple[int, int], DrawingSpec]:
    pose_landmark_style = {}
    for a in mp_pose.POSE_CONNECTIONS:
        pose_landmark_style[a] = DrawingSpec()

    pose_landmark_style[(0, 1)] = DrawingSpec(color=(48, 48, 255))
    print(pose_landmark_style)
    return pose_landmark_style


# For webcam input:
cap = cv2.VideoCapture(0)
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
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
        connection_drawing_spec=helllo())
        # PoseLandmark.LEFT_EYE
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
