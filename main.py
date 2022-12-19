from flask import Flask, Response, render_template
from flask import request
import cv2
import threading

from Annotation import Annotation
from Tracker import Tracker

temp = None
count = 1

app = Flask(__name__)

@app.route('/')
def main():
  return render_template("main.html")

@app.route('/pre_pushup')
def pre_pushup():
    return render_template('pre_pushup.html')
  
@app.route('/pre_squat')
def pre_squat():
    return render_template('pre_squat.html')
  
@app.route('/pushup', methods=['GET', 'POST'])
def pushup():
    if request.method == 'POST':
      count = request.form['reps']
      print(count)
    return render_template('pushup.html', value = count)

@app.route('/squat', methods=['GET', 'POST'])
def squat():
    if request.method == 'POST':
      count = request.form['reps']
      print(count)
    return render_template('squat.html', value = count)

def gen(dev_info):
  annotation = Annotation()
  if dev_info == '0':
    dev_info = 0
  else:
    dev_info = f"./static/samples/{dev_info}"
  print(dev_info)
  dev = Tracker(dev_info)
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

@app.route('/video_feed/<string:dev>')
def video_feed(dev):
  print(f"video_feed run")
  return Response(gen(dev),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=2204, threaded=True)
