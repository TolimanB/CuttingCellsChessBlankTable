# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2
import os

#def find_puzzle(image, debug=False):
debug=False
folder_in = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\In'
folder_out = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Out'

path_f = []
names_f = []
for d, dirs, files in os.walk(folder_in):
    for f in files:
        names_f.append(f)  # короткие пути
        path = os.path.join(d, f)  # формирование адреса
        path_f.append(path)  # добавление адреса в список
i=1
for f in path_f:
    print(f)
    image = cv2.imread(f)
    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)

    # apply adaptive thresholding and then invert the threshold map
    thresh = cv2.adaptiveThreshold(blurred, 255,
    	cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    # check to see if we are visualizing each step of the image
    # processing pipeline (in this case, thresholding)
    if debug:
    	cv2.imshow("Puzzle Thresh", thresh)
    	cv2.waitKey(0)

    # find contours in the thresholded image and sort them by size in
    # descending order
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # initialize a contour that corresponds to the puzzle outline
    puzzleCnt = None

    # loop over the contours
    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    	# if our approximated contour has four points, then we can
    	# assume we have found the outline of the puzzle
    	if len(approx) == 4:
    		puzzleCnt = approx
    		break

    # if the puzzle contour is empty then our script could not find
    # the outline of the sudoku puzzle so raise an error
    if puzzleCnt is None:
    	raise Exception(("Could not find sudoku puzzle outline. "
    		"Try debugging your thresholding and contour steps."))

    # check to see if we are visualizing the outline of the detected
    # sudoku puzzle
    if debug:
    	# draw the contour of the puzzle on the image and then display
    	# it to our screen for visualization/debugging purposes
    	output = image.copy()
    	cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)
    	cv2.imshow("Puzzle Outline", output)
    	cv2.waitKey(0)

    # apply a four point perspective transform to both the original
    # image and grayscale image to obtain a top-down birds eye view
    # of the puzzle
    puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
    warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))

    # check to see if we are visualizing the perspective transform
    if debug:
    	# show the output warped image (again, for debugging purposes)
    	cv2.imshow("Puzzle Transform", puzzle)
    	cv2.waitKey(0)
        # return a 2-tuple of puzzle in both RGB and grayscale
        #return (puzzle, warped)
    fss = f.split('\\')
    fsss = fss[-1].split('.')
    # out_fname = f[0] + '_out.' + f[1]
    out_fname = folder_out + '\\' + fsss[0]+'_G.'+fsss[1]
    cv2.imwrite(out_fname, puzzle)
    i=i+1