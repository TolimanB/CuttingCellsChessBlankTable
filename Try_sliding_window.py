import os
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
    digit_right2left = gray_bgr2gray[0:gray.shape[0],gray.shape[1]//3:gray.shape[1]]
    digit = extract_digit(digit_right2left,partfss, debug=True)