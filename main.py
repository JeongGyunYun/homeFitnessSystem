from flask import Flask, Response, render_template
import cv2
import threading

temp = None
count = 1

app = Flask(__name__)


@app.route('/')
def index():
  return render_template("index.html")


def gen(dev):
  if dev == '0':
    dev = 0
  else:
    dev = f"./samples/{dev}"
  print(dev)
  video = cv2.VideoCapture(dev)
  while True:
    success, image = video.read()
    if not success:
      break
    ret, jpeg = cv2.imencode('.jpg', image)
    frame = jpeg.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed/<string:dev>')
def video_feed(dev):
  return Response(gen(dev),
                  mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=2204, threaded=True)
