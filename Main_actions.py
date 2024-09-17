# import the necessary packages
# from pyimagesearch.sudoku import extract_digit
# from pyimagesearch.sudoku import find_puzzle
#from keras.src.models import model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
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
#path_to_model = 'C:\Projects\OCR\OCRPractitionerBundle_Code\OCRPractitionerBundle_Code\chapter08-sudoku_solver\output\digit_classifier.h5'
path_to_model = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\H5Output\digits_classifier.keras'
folder_out = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Out'
debug = True
# load the digit classifier from disk
print("[INFO] loading digit classifier...")
model = load_model(path_to_model)

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
	gray_cell_upper = cv2.cvtColor(cell_upper, cv2.COLOR_BGR2GRAY)

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

	digit_upp = extract_digit(gray_cell_upper, debug=True)
	digit1 = extract_digit(gray_cell_first_one, debug=True)
	digit2 = extract_digit(gray_cell_second_one, debug=True)
	# verify that the digit is not empty
	if digit1 is not None:
	 	# resize the cell to 28x28 pixels and then prepare the
	 	# cell for classification
		roi1 = cv2.resize(digit1, (28, 28))
		roi1 = roi1.astype("float") / 255.0
		roi1 = img_to_array(roi1)
		roi1 = np.expand_dims(roi1, axis=0)
	 	# classify the digit and update the sudoku board with the
	 	# prediction
		pred1 = model.predict(roi1).argmax(axis=1)[0]
		print("[INFO] classified digit1: "+ str(pred1))
	if digit2 is not None:
		roi2 = cv2.resize(digit2, (28, 28))
		roi2 = roi2.astype("float") / 255.0
		roi2 = img_to_array(roi2)
		roi2 = np.expand_dims(roi2, axis=0)
		pred2 = model.predict(roi2).argmax(axis=1)[0]
		print("[INFO] classified digit2: "+ str (pred2))
	if digit1 is not None and digit2 is not None:
		numb= int(str(pred1)+str(pred2))
		print("[INFO] classified lower numb: " + str(numb))
	if digit_upp is not None:
	 	# resize the cell to 28x28 pixels and then prepare the
	 	# cell for classification
		roi_upp = cv2.resize(digit_upp, (28, 28))
		roi_upp = roi_upp.astype("float") / 255.0
		roi_upp = img_to_array(roi_upp)
		roi_upp = np.expand_dims(roi_upp, axis=0)
	 	# classify the digit and update the sudoku board with the
	 	# prediction
		pred_upp = model.predict(roi_upp).argmax(axis=1)[0]
		print("[INFO] classified upper digit: "+ str(pred_upp))