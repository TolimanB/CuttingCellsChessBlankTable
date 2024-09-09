# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2
import os
from pytesseract import Output
import pytesseract
from Useful_funcs import extract_digit


#def find_table(image, debug=False):
debug=False
folder_in = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\In'
folder_out = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Out'
#в названии католога неприемлемы пути на букву \U -папку надо назвать Unrectangled
#todo - разобраться
folder_unrect = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\RecognizedNot'
kx=0.25
ky=0.25
kTabToBlank=0.4

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
    	cv2.imshow("Puzzle Thresh", cv2.resize(thresh,None,fx=kx, fy=ky))
    	cv2.waitKey(0)

    # find contours in the thresholded image and sort them by size in
    # descending order
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    #print(cnts)
    # initialize a contour that corresponds to the puzzle outline
    puzzleCnt = None

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        #tmpcnt = image.copy()
        #cv2.drawContours(tmpcnt, [approx], -1, (0, 255, 0), 2)
        #cv2.imshow("Puzzle Intermediate Contours", cv2.resize(tmpcnt, None, fx=kx, fy=ky))
        #cv2.waitKey(0)
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
    	cv2.imshow("Puzzle Outline", cv2.resize(output,None,fx=kx, fy=ky))
    	cv2.waitKey(0)

    # apply a four point perspective transform to both the original
    # image and grayscale image to obtain a top-down birds eye view
    # of the puzzle
    puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
    warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))

    # check to see if we are visualizing the perspective transform
    if debug:
    	# show the output warped image (again, for debugging purposes)
    	cv2.imshow("Puzzle Transform", cv2.resize(puzzle,None,fx=kx, fy=ky))
    	cv2.waitKey(0)
        # return a 2-tuple of puzzle in both RGB and grayscale
        #return (puzzle, warped)
    fss = f.split('\\')
    fsss = fss[-1].split('.')
    # out_fname = f[0] + '_out.' + f[1]
    out_fname = folder_out + '\\' + fsss[0]+'_G.'+fsss[1]
    unrect_fname = folder_unrect + '\\' + fsss[0]+'_G.'+fsss[1]

    # предпоследший шаг - проверим, надо ли изображение вращать - через направление текста - также код Адриана
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\79086\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #todo - почему-то надо явно указать путь до tesseract, в path не читает, надо разобраться
    results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
    # display the orientation information
    print("[INFO] detected orientation: {}".format(
        results["orientation"]))
    print("[INFO] rotate by {} degrees to correct".format(
        results["rotate"]))
    print("[INFO] detected script: {}".format(results["script"]))
    rotated = imutils.rotate_bound(puzzle, angle=results["rotate"])
    print ("[INFO] size of rotated image:{}".format (rotated.size))
    print ("[INFO] size of original image:{}".format(image.size))
    print ("[INFO] relation of sizes:{}".format(round(rotated.size/image.size,1)))
    if (round (rotated.size/image.size,2) > kTabToBlank ):
        cv2.imwrite(out_fname, rotated)
    else:
        cv2.imwrite(unrect_fname, rotated)
    i=i+1