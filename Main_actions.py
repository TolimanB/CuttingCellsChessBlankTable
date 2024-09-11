# import the necessary packages
# from pyimagesearch.sudoku import extract_digit
# from pyimagesearch.sudoku import find_puzzle
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import imutils
import cv2
import os
from Useful_funcs import *

k_try1 = 21
k_try2 = 25
k_try3 = 30
k_try4 = 40

path_f = []
names_f = []
path_to_model = 'C:\Projects\OCR\OCRPractitionerBundle_Code\OCRPractitionerBundle_Code\chapter08-sudoku_solver\output\digit_classifier.h5'
folder_out = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Out'
debug = True
# load the digit classifier from disk
print("[INFO] loading digit classifier...")
#model = load_model(path_to_model)

for d, dirs, files in os.walk(folder_out):
	for f in files:
		names_f.append(f)  # короткие пути
		path = os.path.join(d, f)  # формирование адреса
		path_f.append(path)  # добавление адреса в список
for f in path_f:
	print(f)
	image = cv2.imread(f)

	stepY = image.shape[0]//k_try1
	stepX = stepY+stepY//2

    #первая ячейка, проверяем, что там
	startX_upper = 5
	startY_upper = 5
	endX_upper = stepX
	endY_upper = stepY
	cell_upper = image[startX_upper:endY_upper,startY_upper:endY_upper]

	startX = 5
	startY = (k_try1-1) * stepY
	endX = stepX
	endY = k_try1*stepY

	cell = image[startY:endY, startX:endX]
	gray_cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
	if debug:
		cv2.imshow("Cell_upper", cv2.resize(cell_upper, None, fx=1, fy=1))
		cv2.waitKey(0)
		cv2.imshow("Cell_20", cv2.resize(cell, None, fx=1, fy=1))
		cv2.waitKey(0)

	startX_first_digit = 0
	startY_first_digit = 0
	endX_first_digit = (stepX//2)
	endY_first_digit = stepY

	startX_second_digit = (stepX-20)//2
	startY_second_digit = 0
	endX_second_digit = stepX
	endY_second_digit = stepY

	cell_first_one = cell[startY_first_digit:endY_first_digit, startX_first_digit:endX_first_digit]
	cell_second_one = cell[startY_second_digit:endY_second_digit, startX_second_digit:endX_second_digit]
	gray_cell_first_one = cv2.cvtColor(cell_first_one, cv2.COLOR_BGR2GRAY)
	gray_cell_second_one = cv2.cvtColor(cell_second_one, cv2.COLOR_BGR2GRAY)
	if debug:
		cv2.imshow("Cell_20_1", cv2.resize(cell_first_one, None, fx=1, fy=1))
		cv2.waitKey(0)
		cv2.imshow("Cell_20_2", cv2.resize(cell_second_one, None, fx=1, fy=1))
		cv2.waitKey(0)

	#digit = extract_digit(gray_cell, debug=True)
	digit1 = extract_digit(gray_cell_first_one, debug=True)
	digit2 = extract_digit(gray_cell_second_one, debug=True)
	# # verify that the digit is not empty
	# if digit is not None:
	# 	# resize the cell to 28x28 pixels and then prepare the
	# 	# cell for classification
	# 	roi = cv2.resize(digit, (28, 28))
	# 	roi = roi.astype("float") / 255.0
	# 	roi = img_to_array(roi)
	# 	roi = np.expand_dims(roi, axis=0)
	#
	# 	# classify the digit and update the sudoku board with the
	# 	# prediction
	# 	pred = model.predict(roi).argmax(axis=1)[0]