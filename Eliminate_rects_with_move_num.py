import cv2
import imutils
import os
import shutil
import math
import numpy as np

j = 0
#folder_in = 'Z:\Projects\MyOwnProject\Sorting\FO_2016\Y_15\Gomography'
folder_in = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Out'
#folder_cells = 'Z:\Projects\MyOwnProject\Sorting\FO_2016\Y_15\To_work_with\Strorage_little_cells'
folder_cells = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers'
#folder_done = 'Z:\Projects\MyOwnProject\Sorting\FO_2016\Y_15\To_work_with\Done'
folder_done = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Done'
path_f = []
area_sum = 0.0
perimeter_sum = 0.0
#koeff_min = 368
#koeff_max = 372
k_try1 = 21
kx=0.25
ky=0.25
def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

for d, dirs, files in os.walk(folder_in):
    for fs in files:
        path = os.path.join(d, fs)  # формирование адреса
        path_f.append(path)  # добавление адреса в список

for f in path_f:
    fname = f.split('\\')
    fss = fname[-1].split('.')

    im = cv2.imread(f)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#flipped = cv2.flip(imgray, 0)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    clone = im.copy()
    #image,
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    globalArea = cv2.contourArea (contours[0])
    print("Main Area of image  " + " = " + str(globalArea) + '\n')
    one_rectangle_side = imgray.shape[0] // k_try1
    #вычислим для начала площадь и периметр наших изображений
    for (i, cn) in enumerate(contours):


        #print(i,'\n')
        #print ([cn])
        area = cv2.contourArea(cn)
        perimeter = cv2.arcLength(cn, True)
        (x, y, w, h) = cv2.boundingRect(cn)
        print("Area of  " + str(i) + " = "+ str(area) + '\n')
        #print("Perimeter  " + str(i) + " = " + str(perimeter) + '\n')

        #arr = np.array()
        #np.append (arr,[i,area,perimeter,x,y,w,h],axis=0)
    # draw the contour on the image

    #среднего ограничения по площади вполне достаточно, средний периметр можно не смотреть, ибо у некоторых прямогольников он раза в 1.5 больше среднего
        #if (area > 1500 and perimeter >100) and (area<7000 and perimeter<500): #and (area > 3812.44*0.85 and area<3812.44*1.15) :#and (perimeter > 312.61*0.8 and perimeter<312.61*1.2) :
        #if (area > 3000 and perimeter >70): #and (area<3800 and perimeter<80):
        if ((perimeter > 4*one_rectangle_side) and (perimeter < 5*one_rectangle_side)):
            j+=1
            M = cv2.moments(cn)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        #print ("Rectangle "+ str (i)+ " coordinates"+'\n')
        #print (x, y, w, h)
            cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.drawContours(clone, [cn], -1, (0, 255, 0), 2)
            little_cell = im[y:y + h, x:x + w]


            out_cell_name = fss[0] + '_' + str(i)  + '.'+fss[1]

            cv2.imwrite(
                folder_cells + '\\' + out_cell_name, little_cell)

            cv2.putText(clone, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1)
            area_sum += area
            #area_sigma = math.sqrt()
            perimeter_sum += perimeter

        i += 1

    #avg_area = round (area_sum/j,2)
    #avg_perimetr = round (perimeter_sum/j,2)
    #print ("AVG_AREA = ",avg_area)
    #print ("avg_perimetr=",avg_perimetr)
# show the output image
    out_file_name = fss[0] + '_' + 'marked'  + '.'+ fss[1]
    cv2.imshow("Bounding Boxes "+fname[-1], cv2.resize(clone,None,fx=kx, fy=ky))
    cv2.waitKey(0)
    cv2.imwrite(folder_cells + '\\' + out_file_name, clone)

    shutil.move(f, folder_done+'\\'+fname[-1])

