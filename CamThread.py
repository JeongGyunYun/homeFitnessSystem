import cv2
import threading

imageList = []

def camPreView(previewName, camId):
  global imageList
  cam = cv2.VideoCapture(camId)
  if cam.isOpened():
    success, frame = cam.read()
  else:
    success = False
  while success:
    try:
      # cv2.imshow(previewName, frame)
      success, frame = cam.read()
      imageList.append(frame)
      key = cv2.waitKey(1)
    except Exception as e:
      print(e)

  cam.release()


class CamThread(threading.Thread):
  def __init__(self, previewName, camId):
    super(CamThread, self).__init__()
    self.previewName = previewName
    self.camId = camId

  def run(self):
    camPreView(self.previewName, self.camId)
