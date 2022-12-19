from Annotation import Annotation
from Tracker import Tracker
from User import User
import cv2

control_flag = True

def generate_cam():
  annotation = Annotation()
  dev_info = 0
  dev = Tracker(dev_info)
  print(f"[Log]Dev {dev_info} is Starting")
  while True:
    success, image = dev.read()
    if not success:
      break
    results = dev.get_pose_results()
    annotation_img = dev.draw_annotation(landmark_list=results.pose_landmarks, connections=annotation.pose_connections)

    ret, jpeg = cv2.imencode('.jpg', annotation_img)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#TODO Train 영상도 landmark를 그리나?
def generate_video(user: User, filename:str, path:str= "./static/samples/"):
  fullPath = path + filename
  print(f"[Log]Video {filename} is Loaded")
  controller = user.get_controller()
  controller.set_video(fullPath)

  # dev = Tracker(dev_info)
  # while True:
  #   success, image = dev.read()
  #   if not success:
  #     break
  #   results = dev.get_pose_results()
  #   annotation_img = dev.draw_annotation(landmark_list=results.pose_landmarks, connections=annotation.pose_connections)
  controller.load_on_frame()
  while controller.get_status():
    if controller.get_control_flag(): # flag가 true
      controller.load_on_frame() #새로운 frame을 읽음
    if not controller.get_status():
      break
    frame = controller.get_frame()
    byte_image = controller.get_byte_image(frame)
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + byte_image + b'\r\n\r\n')

  # while True:
  #   success, image = cv2.read()
  #   if not success:
  #     break
  #   ret, jpeg = cv2.imencode('.jpg', image)
  #   frame = jpeg.tobytes()
  #   yield (b'--frame\r\n'
  #          b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
