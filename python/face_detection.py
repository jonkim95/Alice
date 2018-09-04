# Face detection done with dlib (https://github.com/davisking/dlib)
# The landmark scheme used by the default predictor is documented at https://ibug.doc.ic.ac.uk/resources/300-W/

import dlib
import glob
import numpy as np
import os
import sys

predictor_path = "../res/shape_predictor_68_face_landmarks.dat"
faces_folder_path = "../res/faces"

def distance(p1, p2):
    dif = p1 - p2
    return np.linalg.norm([dif.x, dif.y])

# Note that slopes and curves will have the opposite cardinality when plotted on a traditional plane.
# This is because the closer a point is to the bottom of the image, the higher the y-value.
def curve(points, deg=2):
    X = [part.x for part in points]
    Y = [part.y for part in points]
    return np.polyfit(X, Y, deg)

def area(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i].x * points[j].y
        area -= points[j].x * points[i].y
    area = abs(area) / 2.0
    return area

# Returns set of points with given start and end indices, inclusive!
def get_points_in_range(shape, start, end):
    return [shape.part(i) for i in xrange(start, end + 1)]

def calc_eyebrows(shape):
    l_points = get_points_in_range(shape, 17, 21)
    r_points = get_points_in_range(shape, 22, 26)
    l_width = distance(shape.part(17), shape.part(21))
    r_width = distance(shape.part(22), shape.part(26))
    l_curve = curve(l_points, 2)
    r_curve = curve(l_points, 2)
    print("Left eyebrow curve : {}x^2 + {}x + {}".format(l_curve[0], l_curve[1], l_curve[2]))
    print("Left eyebrow width : {}".format(l_width))
    print("Right eyebrow curve : {}x^2 + {}x + {}".format(r_curve[0], r_curve[1], r_curve[2]))
    print("Right eyebrow width : {}".format(r_width))

def calc_eyes(shape):
    l_points = get_points_in_range(shape, 36, 41)
    r_points = get_points_in_range(shape, 42, 47)
    l_area = area(l_points)
    r_area = area(r_points)
    l_width = distance(shape.part(36), shape.part(39))
    r_width = distance(shape.part(42), shape.part(45))
    l_slope = curve([shape.part(36), shape.part(39)], 1)
    r_slope = curve([shape.part(42), shape.part(45)], 1)
    print("Left eye area : {}".format(l_area))
    print("Left eye width : {} with slope : {}".format(l_width, l_slope[0]))
    print("Right eye area : {}".format(r_area))
    print("Right eye width : {} with slope : {}".format(r_width, r_slope[0]))

def calc_jaw(shape):
    jaw_points = get_points_in_range(shape, 0, 16)
    jaw_curve = curve(jaw_points, 2)
    print("Jaw curve : {}x^2 + {}x + {}".format(jaw_curve[0], jaw_curve[1], jaw_curve[2]))

def calc_nose(shape):
    nose_width = distance(shape.part(31), shape.part(35))
    # Area of the small triangle-like area at the base of the nose.
    nose_area = area(get_points_in_range(shape, 31, 35))
    print("Nose width : {}".format(nose_width))
    print("Nose area : {}".format(nose_area))

def calc_lips(shape):
    lips_width = distance(shape.part(48), shape.part(54))
    lips_height = distance(shape.part(51), shape.part(57))
    lips_area = area(get_points_in_range(shape, 48, 67))
    # Slope of lower bound of upper lip (equivalent to the line between the lips, assuming the mouth is closed).
    lips_curve = curve(get_points_in_range(shape, 60, 64), 2)
    print("Lips width : {}".format(lips_width))
    print("Lips height : {}".format(lips_height))
    print("Lips area : {}".format(lips_area))
    print("Lips curve : {}x^2 + {}x + {}".format(lips_curve[0], lips_curve[1], lips_curve[2]))

def calculate_face_parts(shape):
    calc_eyebrows(shape)
    calc_eyes(shape)
    calc_jaw(shape)
    calc_nose(shape)
    calc_lips(shape)

def main():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    win = dlib.image_window()
    
    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        print("Processing file: {}".format(f))
        img = dlib.load_rgb_image(f)

        win.clear_overlay()
        win.set_image(img)

        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = predictor(img, d)
            # Draw the face landmarks on the screen.
            win.add_overlay(shape)
            calculate_face_parts(shape)
        win.add_overlay(dets)
        dlib.hit_enter_to_continue()

if __name__ == "__main__":
    main()