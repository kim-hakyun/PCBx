from math import hypot


EPS = 1e-9


def distance(p1, p2):
    return hypot(p1.x - p2.x, p1.y - p2.y)


def remove_duplicate_points(points):
    """연속 중복점 제거"""

    if len(points) < 2:
        return points

    out = [points[0]]

    for p in points[1:]:

        if distance(out[-1], p) > EPS:
            out.append(p)

    return out


def remove_zero_segments(points):
    """길이 0 Segment 제거"""

    if len(points) < 2:
        return points

    out = [points[0]]

    for p in points[1:]:

        if distance(out[-1], p) > EPS:
            out.append(p)

    return out


def close_polygon(points):
    """마지막 점 처리"""

    if len(points) < 3:
        return points

    if distance(points[0], points[-1]) < EPS:

        return points[:-1]

    return points


def polygon_area(points):

    area = 0

    n = len(points)

    for i in range(n):

        j = (i + 1) % n

        area += points[i].x * points[j].y
        area -= points[j].x * points[i].y

    return area / 2.0


def make_ccw(points):

    if polygon_area(points) < 0:

        points.reverse()

    return points


def normalize_polygon(points):

    points = remove_duplicate_points(points)

    points = remove_zero_segments(points)

    points = close_polygon(points)

    points = make_ccw(points)

    return points

print("geometry loaded")