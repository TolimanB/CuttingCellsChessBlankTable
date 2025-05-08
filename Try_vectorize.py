from matplotlib.image import imread, imsave
from scipy import ndimage
from sklearn.cluster import KMeans


def segment_image(image, n_segments, smoothing_sigma):
    smoothed = ndimage.gaussian_filter(image, (smoothing_sigma, smoothing_sigma, 0))
    kmeans = KMeans(n_segments)
    segment_ids = kmeans.fit_predict(smoothed.reshape(-1, 3)).reshape(*image.shape[:2])
    new_image = kmeans.cluster_centers_.astype('uint8')[segment_ids]
    return new_image


image = imread('C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34.jpg')
segmented = segment_image(image, 2000, 1)
imsave('C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\To_work_with\Just_moves_numbers\DSC_0673_G_34_segmented.png', segmented)