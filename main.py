from datetime import timedelta

from flask import Flask, Response, render_template, session, jsonify
from middleware import *
from UserManage import UserManage

app = Flask(__name__)
app.secret_key = "Hello World"
user_manage = UserManage()


@app.route("/")
def check_session():
  if "username" in session:
    return jsonify(f"Name is {session['username']}")
  else:
    return jsonify(f"Who are U?")

@app.route("/set/<value>")
def set_session(value):
  session['username'] = value
  return jsonify(f"Set Name is {session['username']}")

@app.route("/clear")
def clear_session():
  if 'username' in session:
    session.pop('username', None)
  return jsonify("No Session Now")


@app.route('/home')
def index():
  return render_template("index.html")


@app.route('/video_feed/<string:filename>')
def video_feed(filename):
  return Response(generate_video(filename),
                  mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/camera')
def camera_feed():
  return Response(generate_cam(),
                  mimetype='multipart/x-mixed-replace; boundary=frame')


@app.before_request
def make_session_permanent():
  session.permanent = True
  app.permanent_session_lifetime = timedelta(minutes=3)
  #TODO session 자동삭제시 Manage에서 자동 삭제필요
  

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=2204, threaded=True)
