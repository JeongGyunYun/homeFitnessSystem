from Annotation import Annotation
from Tracker import Tracker
from User import User
import cv2
import util

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


def generate_video(user: User, filename:str, path:str= "./static/samples/"):
  fullPath = path + filename
  print(f"[Log]Video {filename} is Loaded")
  controller = user.get_controller()
  controller.set_video(fullPath)
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


def generate_pose_landmark(filename:str, path:str= "./static/samples/") -> bool:
  json_data = dict()
  fullPath = path + filename
  tracker = Tracker(fullPath)
  while True:
    success, image, frame_num = tracker.read()
    if not success:
      break
    results = tracker.get_pose_results()
    json_data[frame_num] = util.convert_mpResultType_to_Dict(results)

  ex_file = filename.split(".")[0]
  util.save_to_json(json_data, f'{ex_file}.json')
  return True
