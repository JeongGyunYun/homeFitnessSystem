from datetime import timedelta

from flask import Flask, Response, render_template, session, jsonify
from middleware import *
from UserManage import UserManage
from User import User

app = Flask(__name__)
app.secret_key = "Hello World"

#Code for Test
UserManage.add_user("Hello", User(user="Hello"))

@app.route("/")
def check_session():
  if "username" in session:
    return jsonify(f"Name is {session['username']}")
  else:
    return jsonify(f"Who are U?")

@app.route("/set/<value>")
def set_session(value):
  session['username'] = value
  UserManage.add_user(value, User(value))
  return jsonify(f"Set Name is {session['username']}")

@app.route("/clear")
def clear_session():
  if 'username' in session:
    UserManage.remove_user(session['username'])
    session.pop('username', None)
  return jsonify("No Session Now")


@app.route('/home')
def index():
  return render_template("index.html")


@app.route('/video_feed/<string:filename>')
def video_feed(filename):
  username = session['username']
  user = UserManage.get_User_from_username(username)
  return Response(generate_video(user=user, filename=filename),
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
