import math


def get_line_equation(pointA, pointB):
    # 输入两点，确定直线方程Ax + By + C = 0:
    A = pointA[1] - pointB[1]
    B = pointB[0] - pointA[0]
    C = pointA[0] * pointB[1] - pointA[1] * pointB[0]
    result = (A, B, C)
    return result


def get_distance_p2l(point, lineParams):
    # 点到直线距离, 输入点point， 直线的方程系数lineparams:(A,B,C)
    # 直线方程Ax + By + C = 0
    A, B, C = lineParams
    distance = abs(A*point[0] + B*point[1] + C) / (math.sqrt(A*A + B*B))
    return distance


def get_distance_p2p(p1, p2):
    # 两点间距离
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))


def get_mid_point(x1, y1, x2, y2):
    return ((x1+x2)/2, (y1+y2)/2)


def get_mid_point_int(x1, y1, x2, y2):
    return (int((x1+x2)/2), int((y1+y2)/2))


def get_intersection_2l(lineParamsA, lineParamsB):
    # 输入两条直线的系数belike Ax + By + C = 0，输出焦点坐标
    A1, B1, C1 = lineParamsA
    A2, B2, C2 = lineParamsB
    y = int((A2 * C1 - A1 * C2)/(A1 * B2 - A2 * B1))
    x = int((B2 * C1 - B1 * C2)/(A2 * B1 - A1 * B2))
    return (x, y)


def get_line_angle(lineParams):
    # input be like: (A,B,C)
    A, B, C = lineParams
    if A != 0:
        k = -1*A/B
    else:
        return 90
    angle = (math.atan(k))*180/math.pi
    return angle


def NG_judgment():
    print('NG')
