from Tracker import Tracker

if __name__ == "__main__":
  webcam = Tracker("custom",dev_info=0)
  while webcam.is_cap_open():
    success, image = webcam.read()
    if not success:
      print("Ignore")
      break
    results = webcam.get_pose_results(image)
    image = webcam.draw_annotation(image, results, landmark_list=None, connections=None)
    webcam.show(image)

  webcam.pose_close()
  webcam.release()
