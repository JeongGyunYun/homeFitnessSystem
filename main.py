from Tracker import Tracker
from Annotation import Annotation
from solutions import PoseConnection

if __name__ == "__main__":
  webcam = Tracker("custom", dev_info=0)
  annotation = Annotation()

  while webcam.is_cap_open():
    success, image = webcam.read()
    if not success:
      print("Ignore")
      break
    results = webcam.get_pose_results()
    connection_style = annotation.make_connection_style_from_result()

    #
    # #TestCode 임의로 주어진 result 값
    # if webcam.get_right_shoulder_angle():
    #   if webcam.get_right_shoulder_angle() > 90:
    #     annotation.make_connection_style_from_result([PoseConnection.RIGHT_SHOULDER_TO_RIGHT_ELBOW])

    webcam.draw_annotation(landmark_list=results.pose_landmarks, connections=annotation.pose_connections,
                           connection_drawing_spec=connection_style)
    print(f'left  elbow angle{webcam.get_left_shoulder_angle()}  right elbow angle{webcam.get_right_shoulder_angle()}')
    webcam.show()

  webcam.pose_close()
  webcam.release()
