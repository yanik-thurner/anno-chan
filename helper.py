from PySide2.QtCore import QRectF, QPointF


class Reference:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


def pos_in_bbox(pos_rel: tuple, bbox_rel: tuple) -> bool:
    """

    :param pos_rel:
    :param bbox_rel: [x, y, w, h]
    :return:
    """
    return bbox_rel[0] < pos_rel[0] < bbox_rel[2] + bbox_rel[0] and bbox_rel[1] < pos_rel[1] < bbox_rel[3] + bbox_rel[1]


def points_to_bbox(point1: tuple, point2: tuple, max_values: tuple = (0, 0)):
    """

    :param point1:
    :param point2:
    :param max_values:
    :return: [x, y, w, h]
    """
    xmin = max(0, min(point1[0], point2[0]))
    ymin = max(0, min(point1[1], point2[1]))
    xmax = min(max_values[0], max(point1[0], point2[0]))
    ymax = min(max_values[1], max(point1[1], point2[1]))
    return [xmin, ymin, xmax - xmin, ymax - ymin]


def xyxy_to_xywh(bbox_xyxy: list):
    return [bbox_xyxy[0], bbox_xyxy[1], bbox_xyxy[2] - bbox_xyxy[0], bbox_xyxy[3] - bbox_xyxy[1]]