import cv2
import math

img = cv2.imread('C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34.jpg')
(h, w) = img.shape[:2]
image_size = h*w
mser = cv2.MSER_create()
mser.setMaxArea(math.trunc (image_size/2))
mser.setMinArea(10)

clone = img.copy()
gray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY) #Converting to GrayScale
_, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


regions, rects = mser.detectRegions(bw)

# With the rects you can e.g. crop the letters
for (x, y, w, h) in rects:
    cv2.rectangle(clone, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)

cv2.imshow("Bounding Boxes ", clone)
cv2.waitKey(0)