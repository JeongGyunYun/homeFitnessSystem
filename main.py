from datetime import timedelta

from flask import Flask, Response, render_template, session, jsonify, request, redirect, url_for
from middleware import *
from UserManage import UserManage
from ViedoController import VideoController
from User import User

app = Flask(__name__)
app.secret_key = "Hello World"

#Code for Test
# UserManage.add_user("Hello", User(user="Hello"), Tracker(0))

@app.route("/")
def check_session():
  value = "hello"
  session['username'] = value
  UserManage.add_user(value, User(value),
                      Tracker(dev_info=0))
  return redirect(url_for('main'))

  # if "username" in session:
  #   return jsonify(f"Name is {session['username']}")
  # else:
  #   return jsonify(f"Who are U?")

@app.route("/set/<value>")
def set_session(value):
  session['username'] = value
  UserManage.add_user(value, User(value), Tracker(dev_info=0))
  return jsonify(f"Set Name is {session['username']}")

@app.route("/clear")
def clear_session():
  if 'username' in session:
    UserManage.remove_user(session['username'])
    session.pop('username', None)
  return jsonify("No Session Now")

@app.route('/pre_pushup')
def pre_pushup():
  if 'username' in session and UserManage.is_user_in_user_list(session['username']):
    username = session['username']
    user = UserManage.get_User_from_username(username)
    user.set_train_push_up()
    return render_template('pre_pushup.html')
  else:
    return redirect(url_for('check_session'))
  
@app.route('/pre_squat')
def pre_squat():
    username = session['username']
    user = UserManage.get_User_from_username(username)
    user.set_train_squat()
    return render_template('pre_squat.html')
  
@app.route('/pushup', methods=['GET', 'POST'])
def pushup():
  if 'username' in session and UserManage.is_user_in_user_list(session['username']):
    if request.method == 'POST':
      count = request.form['reps']
      print(count)
    return render_template('pushup.html', value=count)
  else:
    return redirect(url_for('check_session'))


@app.route('/squat', methods=['GET', 'POST'])
def squat():
  if request.method == 'POST':
    count = request.form['reps']
    print(count)
  return render_template('squat.html', value=count)


@app.route('/home')
def main():
  if 'username' in session and\
      UserManage.is_user_in_user_list(session['username']):
    username = session['username']
    user = UserManage.get_User_from_username(username)
    user.clear_count()
    return render_template("main.html")
  else:
    return redirect(url_for('check_session'))


@app.route('/data_feed')
def data_feed():
  username = session['username']
  user = UserManage.get_User_from_username(username)
  return Response(generate_data(user), mimetype='text')

@app.route('/ready_data_feed')
def ready_data_feed():
  username = session['username']
  pose_checker = UserManage.get_PoseChecker_from_username(username)
  return Response(generate_ready_data(pose_checker))

@app.route('/video_feed/<string:filename>/<int:count>')
def video_feed(filename, count):
  username = session['username']
  user = UserManage.get_User_from_username(username)
  user.get_controller().set_max_loop_count(count)
  postChecker = UserManage.get_PoseChecker_from_username(username)
  return Response(generate_video(user=user, posechecker=postChecker, filename=filename),
                  mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/camera')
def camera_feed():
  username = session['username']
  pose_checker = UserManage.get_PoseChecker_from_username(username)
  tracker = UserManage.get_Trakcer_from_username(username)
  return Response(generate_cam(pose_checker, tracker),
                  mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/req/stop')
def video_stop():
  username = session['username']
  controller:VideoController = UserManage.get_User_from_username(username).get_controller()
  controller.stop_video()
  return f"{controller.get_control_flag()}"

@app.route("/req/play")
def video_play():
  username = session['username']
  controller:VideoController = UserManage.get_User_from_username(username).get_controller()
  # controller.play_video()
  return f"{controller.get_control_flag()}"


@app.route("/saveLandmark/<filename>")
def save_pose_landmark(filename):
  status = generate_pose_landmark(filename)
  return f"{status}"

# @app.before_request
# def make_session_permanent():
#   session.permanent = True
#   app.permanent_session_lifetime = timedelta(minutes=3)
#   #TODO session ??????????????? Manage?????? ?????? ????????????
  

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=2204, threaded=True)
