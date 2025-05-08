import cv2
import numpy as np

image = cv2.imread('C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34_upscaled.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# kernel = np.array([[0, -1, 0],
#                    [-1, 5,-1],
#                    [0, -1, 0]])

kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
cv2.imshow('AV CV- Winter Wonder Sharpened', image_sharp)
cv2.waitKey()
cv2.imwrite("C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34_sharped_png.png", image_sharp)
cv2.destroyAllWindows()