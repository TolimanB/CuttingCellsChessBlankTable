from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2

def extract_digit(cell,name, debug=False): #todo - имя сделать необязательным и 3-м параметром
	# apply automatic thresholding to the cell and then clear any
	# connected borders that touch the border of the cell
	thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	if debug:
		cv2.imshow(name, thresh) #"Cell Thresh before borders"
		cv2.waitKey(0)
	thresh = clear_border(thresh)
	#thresh = clear_border(cell)

	# check to see if we are visualizing the cell thresholding step
	if debug:
		cv2.imshow("Cell Thresh", thresh)
		cv2.waitKey(0)

	# find contours in the thresholded cell
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# if no contours were found than this is an empty cell
	if len(cnts) == 0:
		return None

	# otherwise, find the largest contour in the cell and create a
	# mask for the contour
	c = max(cnts, key=cv2.contourArea)
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)

	# compute the percentage of masked pixels relative to the total
	# area of the image
	(h, w) = thresh.shape
	percentFilled = cv2.countNonZero(mask) / float(w * h)

	# if less than 3% of the mask is filled then we are looking at
	# noise and can safely ignore the contour
	if percentFilled < 0.03:
		return None

	# apply the mask to the thresholded cell
	digit = cv2.bitwise_and(thresh, thresh, mask=mask)

	# check to see if we should visualize the masking step
	if debug:
		cv2.imshow("Digit", digit)
		cv2.waitKey(0)

	# return the digit to the calling function
	return digit

#def look_for_digits (image,type_of_search,need_to_split, debug=True):
