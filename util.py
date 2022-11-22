from solutions import PoseLandmark
from math import atan2, pi

def get_angel(firstLandmark: PoseLandmark, midLandmark: PoseLandmark, lastlandmark:PoseLandmark):
    radian = atan2(lastlandmark.y - midLandmark.y,
                   lastlandmark.x - midLandmark.x) - \
             atan2(firstLandmark.y - midLandmark.y,
                   firstLandmark.x - midLandmark.x)

    degree = abs(radian * 180.0 / pi)
    if degree > 180.0:
        degree = 360.0 - degree
    return degree


def get_angel_from_symbol(results, firstLandmark: PoseLandmark, midLandmark: PoseLandmark, lastLandmark:PoseLandmark):
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
