import dlib
import glob
import numpy as np
import os
import sys
from subprocess import call

#asdf
# "Left eyebrow curve : {}x^2 + {}x + {}".format(l_curve[0], l_curve[1], l_curve[2])
#

predictor_path = "../res/shape_predictor_68_face_landmarks.dat"
facial_design_folder_path = "../res/facial design parts"

def parse_arguments(args):
	left_eyebrow_curve = [float(args[0]), float(args[1]), float(args[2])]
	left_eyebrow_width = float(args[3])
	right_eyebrow_curve = [float(args[4]), float(args[5]), float(args[6])]
	right_eyebrow_width = float(args[7])

	left_eye_area = float(args[8])
	left_eye_width = [float(args[9]), float(args[10])]
	right_eye_area = float(args[11])
	Right_eye_width = [float(args[12]), float(args[13])]

	jaw_curve = [float(args[14]), float(args[15]), float(args[16])]

	nose_width = float(args[17])
	nose_area = float(args[18])

	lips_width = float(args[19])
	lips_height = float(args[20])
	lips_area = float(args[21])
	lips_curve = [float(args[22]), float(args[23]), float(args[24])]

	#print("Brow " + str(left_eyebrow_curve[0]) + "\n")






def main():
    print("\nPROCESS #2 Opened: Inside create character")
    myList = sys.argv[1:]
    print("Passed on Arguments: " + ' '.join(myList) + "\n")
    parse_arguments(myList)




if __name__ == "__main__":
    main()

