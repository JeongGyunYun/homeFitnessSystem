import json

from solutions import PoseLandmark
from math import atan2, pi


def get_angel(firstLandmark: PoseLandmark, midLandmark: PoseLandmark, lastlandmark: PoseLandmark):
  radian = atan2(lastlandmark.y - midLandmark.y,
                 lastlandmark.x - midLandmark.x) - \
           atan2(firstLandmark.y - midLandmark.y,
                 firstLandmark.x - midLandmark.x)

  degree = abs(radian * 180.0 / pi)
  if degree > 180.0:
    degree = 360.0 - degree
  return degree


def get_angel_from_symbol(results, firstLandmark, midLandmark, lastLandmark):
  degree = None
  if results.pose_landmarks:
    firstPoint = results.pose_landmarks.landmark[firstLandmark]
    midPoint = results.pose_landmarks.landmark[midLandmark]
    lastPoint =results.pose_landmarks.landmark[lastLandmark]

    radian = atan2(lastPoint.y - midPoint.y,
                   lastPoint.x - midPoint.x) - \
             atan2(firstPoint.y - midPoint.y,
                   firstPoint.x - midPoint.x)

    degree = abs(radian * 180.0 / pi)
    if degree > 180.0:
      degree = 360.0 - degree
  return degree


def convert_landmark_to_array(results, poseLandmarkIdx):
  if not results.pose_landmarks:
    return None
  result = results.pose_landmarks.landmark
  return [result[poseLandmarkIdx].x, result[poseLandmarkIdx].y, result[poseLandmarkIdx].z]


def save_to_json(data, ofile: str, path: str = "static/sampleDB/") -> bool:
  """
  list 데이터를 받아서 json 파일로 저장하는 함수
  :param data: json형식으로 저장할 Data
  :param ofile: 저장될 json파일 이름
  :return: 성공/실패
  """
  full_path = path + ofile
  with open(full_path, 'w') as outfile:
    json.dump(data, outfile, indent=4)
  return True


def convert_landmark_to_array(results, poseLandmarkIdx):
  if not results.pose_landmarks:
    return None
  result = results.pose_landmarks.landmark
  return [result[poseLandmarkIdx].x, result[poseLandmarkIdx].y, result[poseLandmarkIdx].z]


def convert_mpResultType_to_Dict(mp_results):
  def convert_landmark_to_list(landmarkList_data):
    landmark_list = []
    for landmark in landmarkList_data:
      landmark_list.append({"x": landmark.x, "y": landmark.y, "z": landmark.z})
    return landmark_list

  result_dic = dict()
  pose_list = convert_landmark_to_list(mp_results.pose_landmarks.landmark)
  pose_word_list = convert_landmark_to_list(mp_results.pose_world_landmarks.landmark)
  result_dic["pose_landmarks"] = pose_list
  result_dic["pose_world_landmarks"] = pose_word_list
  return result_dic
