import numpy as np
import matplotlib.pyplot as plt
from draw import draw
from scipy import stats
from TrackingObjects import Line
from math import atan, pi
from DataReader import read_data


class Tracker:
    """Creates a tracker object that takes a dataset and can perform various
    calculations on it.
    data: lst[lst[float]]
    output: lst[tuple(float, float)]
    contains marked parts and their corresponding points at each frame.
    """

    def __init__(self, data):
        self.data = data
        self.left = []
        self.right = []

    def frame_by(self):
        """Goes through each frame worth of data. Analyses and graphs opening
        angle of vocal cords. Prints summary statistics."""
        ac1 = self.data[0]
        # frames dropped
        i = 0
        for item in self.data[1]:
            if item[0] != 0:
                i += 1
        print(i)
        LC = [ac1, self.data[2], self.data[3], self.data[4], self.data[5],
              self.data[6], self.data[7]]
        RC = [ac1, self.data[8], self.data[9], self.data[10], self.data[11],
              self.data[12], self.data[13]]
        graph = []
        for i in range(len(self.data[1])):
            LC_now = []
            RC_now = []
            cords_there = False
            for j in range(len(LC)):
                LC_now.append(LC[j][i])
                RC_now.append(RC[j][i])
                if LC[j][i][0] != 0 or RC[j][i][0] != 0 and len(LC_now) > 2\
                        and len(RC_now) > 2:
                    cords_there = True
            if cords_there:
                angle = self.angle_of_opening(LC_now, RC_now)
                if angle < pi:
                    graph.append(angle)
                else:
                    graph.append(None)
            else:
                self.left.append(None)
                self.right.append(None)
                graph.append(None)
        dgraph = []
        sgraph = []
        for item in graph:
            if item is not None:
                dgraph.append(item * 360 / (2 * pi))
                sgraph.append(item * 360 / (2 * pi))
            else:
                dgraph.append(None)
        arr = np.array(sgraph)
        print(i)
        print('Mean: ')
        print(np.mean(arr))
        print('Std Dev: ')
        print(np.std(arr))
        print('Max: ')
        print(np.max(arr))
        print('Range: ')
        print(np.max(arr) - np.min(arr))
        print('99th: ')
        print(np.percentile(arr, 99.9))
        print('Min: ')
        print(np.min(arr))
        print(len(data[1]) == len(dgraph))
        plt.title('Angle of Opening at Anterior Commissure')
        plt.plot(dgraph)
        plt.xlabel('Frames')
        plt.ylabel('Angle Between Cords')
        print(len(dgraph))
        draw('C:\\Users\\Natad\\Downloads\\vocal1DeepCut_resnet50_vocalMay13shuffle1_1030000_labeled.mp4',
            (self.left, self.right))
        print('Video made')
        plt.show()

    def angle_of_opening(self, left_cord, right_cord):
        """Calculates angle of opening between left and right cord."""
        left_line = calc_reg_line(left_cord)
        left_line.set_end2(left_cord[len(left_cord) - 1])
        if not left_line.slope == 0:
            self.left.append(left_line)
        else:
            self.left.append(None)
        right_line = calc_reg_line(right_cord)
        right_line.set_end2(right_cord[len(right_cord) - 1])
        if not right_line.slope == 0:
            self.right.append(right_line)
        else:
            self.right.append(None)
        if left_line.slope == 0 or right_line.slope == 0:
            return pi
        tan = abs((left_line.slope - right_line.slope) / (1 + left_line.slope *
                                                          right_line.slope))
        return atan(tan)


def calc_reg_line(pt_lst):
    """Given a list corresponding to points plotted on a vocal cord. Calculates
    a regression line from those points which is used to represent the cord."""
    pfx = []
    pfy = []
    for item in pt_lst:
        pfx.append(item[0])
        pfy.append(item[1])
    pf = stats.linregress(pfx, pfy)
    if abs(pf[2]) < .9:
        return Line(0, 0)
    slope = pf[0]
    yint = pf[1]
    return Line(slope, yint)


if __name__ == '__main__':
    data = read_data('vocal1DeepCut_resnet50_vocalMay13shuffle1_1030000.h5')
    t = Tracker(data)
    t.frame_by()
