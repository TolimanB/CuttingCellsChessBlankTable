# find homography
import sys
import cv2
import numpy as np
import copy
import os

points = []
WINDOW_NAME = 'unwarp'

# fname = sys.argv[1]
folder_in = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\In'
folder_out = 'C:\Projects\PyImageSearch\CuttingCellsChessBlankTable\Out'

def closest_to(x, y):
    best_dist = 10e9
    best_i = -1
    for i in range(len(points)):
        (px, py) = points[i]
        dx = (px - x)
        dy = (py - y)
        d = dx * dx + dy * dy
        if d < best_dist:
            best_dist = d
            best_i = i
    return best_i


def mouse(evt, x, y, flags, ctx):
    """ Mouse Callback function to select the
    four points in the input image """
    if evt == cv2.EVENT_LBUTTONUP:
        global points
        if len(points) >= 4:
            points[closest_to(x, y)] = (x, y)
        else:
            points += [(x, y)]

        show = copy.copy(ctx)
        for (x, y) in points:
            cv2.circle(show, (x, y), 5, (255, 0, 0), 3)
        cv2.imshow(WINDOW_NAME, show)


def order_points(width, height):
    """ order points: (bottom-left, bottom-right, top-right, top-left) """
    global points
    new_points = []

    bl = closest_to(0, height)
    new_points += [points[bl]]
    del points[bl]

    br = closest_to(width, height)
    new_points += [points[br]]
    del points[br]

    tr = closest_to(width, 0)
    new_points += [points[tr]]
    del points[tr]

    tl = closest_to(0, 0)
    new_points += [points[tl]]
    del points[tl]

    points = new_points


def calc(real_width, real_height, width, height):
    """ calculates the homography """
    global points
    if len(points) != 4:
        raise Exception('need exactly four points')

    order_points(width, height)

    p = np.empty((4, 2), dtype=np.int32)
    h = np.empty((4, 2), dtype=np.int32)
    p2h = np.empty((3, 3), dtype=np.int32)

    for i in range(4):
        (x, y) = points[i]
        p[i][0] = (float(real_width) / float(width)) * x
        p[i][1] = (float(real_height) / float(height)) * y

    h[0][0] = 0
    h[0][1] = real_height

    h[1][0] = real_width
    h[1][1] = real_height

    h[2][0] = real_width
    h[2][1] = 0

    h[3][0] = 0
    h[3][1] = 0

    p2h, mask = cv2.findHomography(p, h, cv2.RANSAC)

    return p2h




path_f = []
names_f = []
for d, dirs, files in os.walk(folder_in):
    for f in files:
        names_f.append(f)  # короткие пути
        path = os.path.join(d, f)  # формирование адреса
        path_f.append(path)  # добавление адреса в список
i=1
for f in path_f:
    print (f)
    #print (fn)

    im_in = cv2.imread(f)
    print (im_in)
    im_in_height, im_in_width = im_in.shape[:2]

    width = 600
    height = int(width * (im_in_height / float(im_in_width)))
    print('working on %dx%d' % (width, height))

    im_small = cv2.resize(im_in, (width, height))

    cv2.namedWindow(WINDOW_NAME, 1)
    cv2.imshow(WINDOW_NAME, im_small)
    cv2.setMouseCallback(WINDOW_NAME, mouse, im_small)
    cv2.waitKey(0)

    homo = calc(im_in_width, im_in_height, width, height)
    print(homo)
    out = cv2.warpPerspective(im_in, homo, (im_in_width, im_in_height))

    out_small = cv2.resize(out, (width, height))
    cv2.imshow(WINDOW_NAME, out_small)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #fn_arr = fn.split('.')
    #out_fname = folder_out + '\\' + str(i)+'.jpg' #fn_arr[0] + '_out.' + fn_arr[1]
    #cv2.imwrite(out_fname, out)

    fss = f.split('\\')
    fsss = fss[-1].split('.')
    # out_fname = f[0] + '_out.' + f[1]
    out_fname = folder_out + '\\' + fsss[0]+'_G.'+fsss[1]
    cv2.imwrite(out_fname, out)
    i=i+1