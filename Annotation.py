from typing import Mapping, Tuple

from mediapipe.python.solutions.drawing_utils import DrawingSpec

RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)


class Annotation:
  def __init__(self):
    self.pose_connections = [(0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5),
                             (5, 6), (6, 8), (9, 10), (11, 12), (11, 13),
                             (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
                             (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
                             (18, 20), (11, 23), (12, 24), (23, 24), (23, 25),
                             (24, 26), (25, 27), (26, 28), (27, 29), (28, 30),
                             (29, 31), (30, 32), (27, 31), (28, 32)]
    self.pose_landmark_style: Mapping[Tuple[int, int], DrawingSpec] = {}

    # Set Default
    self.set_default_connection_style()

  def set_default_connection_style(self):
    for connection in self.pose_connections:
      self.pose_landmark_style[connection] = DrawingSpec(color=GREEN_COLOR)

  def make_connection_style_from_results(self, results):
    self.set_default_connection_style()
    for result in results:
      self.set_connection_red(result)

  def set_connection_red(self, result: Tuple[int, int]):
      self.pose_landmark_style[result] = DrawingSpec(color=RED_COLOR)

  def make_connection_style_from_result(self, result: Tuple[int, int] = None):
    self.set_default_connection_style()
    if result == None:
      return self.pose_landmark_style
    for connection in result:
      self.pose_landmark_style[connection] = DrawingSpec(color=RED_COLOR)
    return self.pose_landmark_style

  def get_connection_style(self) -> Mapping[Tuple[int, int], DrawingSpec]:
    return self.pose_landmark_style


  def reset(self):
    self.pose_connections = [(0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5),
                             (5, 6), (6, 8), (9, 10), (11, 12), (11, 13),
                             (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
                             (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
                             (18, 20), (11, 23), (12, 24), (23, 24), (23, 25),
                             (24, 26), (25, 27), (26, 28), (27, 29), (28, 30),
                             (29, 31), (30, 32), (27, 31), (28, 32)]
