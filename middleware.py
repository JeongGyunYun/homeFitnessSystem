from Annotation import Annotation
from Tracker import Tracker
from ViedoController import VideoController
from PoseChecker import PoseChecker
from User import User
import cv2
import util

control_flag = True

def generate_cam(poseChecker: PoseChecker, tracker:Tracker):
  """
  Cam을 프레임단위로 Response 하는 함수
  :param tracker:
  :return:
  """
  annotation = Annotation()
  dev = tracker
  dev.capture_start()
  poseChecker = poseChecker

  while True:
    success, image, _ = dev.read()
    if not success:
      break
    results = dev.get_pose_results()
    # TODO 여기서 Cam 한프레임마다 영상 Frame을 비교하여 동영상을 제어함
    # PoseChecker.test(dev, controller)

    poseChecker.play()

    annotation_img = dev.draw_annotation(landmark_list=results.pose_landmarks, connections=annotation.pose_connections)

    ret, jpeg = cv2.imencode('.jpg', annotation_img)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def generate_video(user: User, posechecker: PoseChecker, filename:str, path:str= "./static/samples/"):
  """
  동영상을 프레임 단위로 나누어서 프레임을 Response하는 함수
  :param user:
  :param filename:
  :param path:
  :return:
  """
  fullPath = path + filename
  print(f"[Log]Video {filename} is Loaded")
  controller = user.get_controller()
  controller.set_video(fullPath)
  posechecker.set_json_data()
  controller.load_on_frame()

  #flag에 따라 동영상을 제어하는 영역
  while controller.get_status():
    if controller.get_control_flag():  # flag가 true
      controller.load_on_frame()  # 새로운 frame을 읽음
    if not controller.get_status():
      if controller.is_end_loop():
        break
      else:
        controller.count_loop()
        controller.set_frame_to_start()
        controller.load_on_frame()
    frame = controller.get_frame()
    byte_image = controller.get_byte_image(frame)
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + byte_image + b'\r\n\r\n')


def generate_pose_landmark(filename:str, path:str= "./static/samples/") -> bool:
  """
  동영상 파일을 입력하면 pose을 인식한 결과를 json파일로 저장해주는 함수
  :param filename:
  :param path:
  :return:
  """
  json_data = dict()
  fullPath = path + filename
  tracker = Tracker(fullPath)
  tracker.capture_start()
  while True:
    success, image, frame_num = tracker.read()
    if not success:
      break
    results = tracker.get_pose_results()
    json_data[frame_num] = util.convert_mpResultType_to_Dict(results)

  ex_file = filename.split(".")[0]
  util.save_to_json(json_data, f'{ex_file}.json')
  return True
