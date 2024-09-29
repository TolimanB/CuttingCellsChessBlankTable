import os
import time
from Useful_funcs import *

path_f = []
folder_cells = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers'
for d, dirs, files in os.walk(folder_cells):
    for fs in files:
        path = os.path.join(d, fs)  # формирование адреса
        path_f.append(path)  # добавление адреса в список

for f in path_f:
    fname = f.split('\\')
    fss = fname[-1].split('.')
    partfss = fss[0][-7:]
    print (partfss)
    gray = cv2.imread(f)
    gray_bgr2gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    #digit_right2left = gray_bgr2gray[0:gray.shape[0],gray.shape[1]//3:gray.shape[1]]
    #digit = extract_digit(digit_right2left,partfss, debug=True)
    (winW, winH) = (gray_bgr2gray.shape[0]-8, gray_bgr2gray.shape[0]-8)
    # loop over the image pyramid
    for resized in pyramid(gray_bgr2gray, scale=1.0):
        # loop over the sliding window for each layer of the pyramid
        for (x, y, window) in sliding_window_adaptive(resized, stepSize=8, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue
            # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
            # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
            # WINDOW
            # since we do not have a classifier, we'll just draw the window
            clone = resized.copy()
            cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
            cv2.imshow("Window", clone)
            cv2.waitKey(1)
            time.sleep(0.025)