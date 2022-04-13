import cv2
import math
import numpy
import numpy as np

class CellCounting:
    def __init__(self):
        pass

    def fill_my_blob(self, image, box, x, y, blob):
        if image[x][y] == 0 or box[x][y] == blob:
            return
        checkx = checky = [-1, 0, 1]
        if image[x][y] == 255:
            box[x][y] = blob
            for k in checkx:
                row = x+k
                if row < 0 or row >= image.shape[0]:
                    continue
                for j in checky:
                    col = y + j
                    if col < 0 or col >= image.shape[1]:
                        continue
                    if row == x and col == y:
                        continue

                    self.fill_my_blob(image, box, row, col, blob)
        return

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""
        regions = dict()
        box = np.zeros(image.shape, np.uint8)
        track = 1

        for i in range(image.shape[1]):
            for j in range(image.shape[0]):
                if image[j][i] == 255 and box[j][i] == 0:
                    regions[track] = []
                    self.fill_my_blob(image, box, j, i, track)
                    track += 1

        for i in range(box.shape[0]):
            for j in range(box.shape[1]):
                if box[i][j] == 0:
                    continue
                regions[box[i][j]].append([i, j])

        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)
        stats = dict()
        for key in region.keys():
            a = len(region[key])
            minx = miny = 10000
            maxx = maxy = 0
            for k in range(a):
                minx = min(minx, region[key][k][0])
                maxx = max(maxx, region[key][k][0])

                miny = min(miny, region[key][k][1])
                maxy = max(maxy, region[key][k][1])

            finalx = int((maxx + minx) / 2)
            math.floor(finalx)
            finaly = int((maxy + miny) / 2)
            math.floor(finaly)
            stats[key] = [[finalx, finaly], a]
            print(key, stats[key])

        return stats

    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""
        m = image.copy()
        me = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        mycolor = (140, 140, 140)
        for key in stats.keys():
            if stats[key][1] < 15:
                continue
            writeString = "* {}, {}".format(me, stats[key][1])
            m = cv2.putText(m, writeString, (stats[key][0][1] - 2, stats[key][0][0] + 2), font, 0.35, mycolor, 1)
            me += 1

        return m

