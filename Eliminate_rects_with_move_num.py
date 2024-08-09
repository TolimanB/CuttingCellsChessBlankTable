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

    #вычислим для начала площадь и периметр наших изображений
    for (i, cn) in enumerate(contours):


        print(i,'\n')
        print ([cn])
        area = cv2.contourArea(cn)
        perimeter = cv2.arcLength(cn, True)
        (x, y, w, h) = cv2.boundingRect(cn)
        print("Area of  " + str(i) + " = "+ str(area) + '\n')
        print("Perimeter  " + str(i) + " = " + str(perimeter) + '\n')

        #arr = np.array()
        #np.append (arr,[i,area,perimeter,x,y,w,h],axis=0)
    # draw the contour on the image

    #среднего ограничения по площади вполне достаточно, средний периметр можно не смотреть, ибо у некоторых прямогольников он раза в 1.5 больше среднего
        #if (area > 1500 and perimeter >100) and (area<7000 and perimeter<500): #and (area > 3812.44*0.85 and area<3812.44*1.15) :#and (perimeter > 312.61*0.8 and perimeter<312.61*1.2) :
        if (area > 30000 and perimeter >700) and (area<38000 and perimeter<800):
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
    cv2.imshow("Bounding Boxes "+fname[-1], clone)
    cv2.waitKey(0)
    cv2.imwrite(folder_cells + '\\' + out_file_name, clone)

    shutil.move(f, folder_done+'\\'+fname[-1])

