import cv2
import cv2.dnn_superres

# Создаём sr-объект
sr = cv2.dnn_superres.DnnSuperResImpl_create()

# Считываем изображение
image = cv2.imread('C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34_segmented.png')

# Считываем модель
path = "FSRCNN_x2.pb"
sr.readModel('C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\FSRCNN_x2.pb')

# Устанавливаем модель и масштаб
sr.setModel("fsrcnn", 2)

# Улучшаем
result = sr.upsample(image)

# Сохраняем
cv2.imwrite("C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34_upscaled.png", result)