#!/usr/bin/python
"""
  Evaluation of Maize Field complexity (from navigation point of view)
  usage:
       ./eval_field.py <laser data/gaps>
"""
import sys
import math
import os
import matplotlib.pyplot as plt
import numpy as np

def getArray( filename ):
    arr = []
    for line in open(filename):
        if "gapsize:" in line:
            arr.append( int(line.split()[-1]) )
    return arr

def draw( arr ):
    time = np.arange(0.0, len(arr)/10., 0.1)
    plt.plot(time, arr, 'o-', linewidth=2)
    plt.ylabel("gap size", fontsize=24)
    plt.xlabel("time (sec)", fontsize=24)
    plt.show()

#------------------------------------------------

def gen10th( arr ):
    "return index,distance pairs for every 10th element"
    for i in xrange(len(arr)/10):
        best = arr[i*10]
        for j in xrange(10):
            if arr[i*10+j][1] < best[1]:
                best = arr[i*10+j]
        yield best

def drawScan():     
    dist = [4235, 4254, 0, 0, 4736, 4732, 4721, 4581, 4527, 4528, 4268, 4168,
            4133, 3323, 3333, 4032, 4023, 4017, 4049, 4171, 4993, 5208, 5216,
            7237, 7114, 7046, 5812, 5508, 5467, 5476, 5512, 5684, 5650, 5646,
            5640, 193, 231, 231, 234, 238, 194, 6289, 6300, 6279, 8664, 7380,
            7083, 7116, 7632, 7110, 6999, 200, 244, 257, 251, 230, 233, 233,
            244, 253, 263, 179, 11675, 11860, 11899, 12054, 19317, 19656, 1849,
            1857, 1855, 1852, 1892, 0, 0, 0, 2646, 2213, 2003, 1962, 2151,
            2657, 2007, 1839, 1832, 1936, 2951, 2843, 2067, 1931, 1961, 1905,
            1884, 2175, 3460, 1863, 1838, 1939, 1835, 1273, 1137, 1123, 1135,
            1138, 2171, 2063, 1533, 1223, 1164, 1162, 1293, 1270, 1084, 1070,
            1056, 1084, 1179, 1249, 702, 333, 372, 346, 350, 364, 379, 400,
            590, 711, 1136, 2086, 2055, 1352, 1226, 1264, 1410, 2047, 2072,
            1533, 1402, 1378, 1328, 655, 499, 397, 386, 412, 660, 801, 1898,
            1412, 1371, 1419, 1648, 1817, 1811, 1786, 1638, 1620, 955, 663,
            599, 625, 699, 766, 614, 505, 501, 502, 495, 474, 496, 599, 685,
            806, 747, 620, 579, 574, 583, 587, 583, 590, 560, 561, 524, 493,
            500, 510, 524, 543, 553, 540, 543, 615, 638, 609, 580, 645, 696,
            752, 807, 847, 990, 1337, 1397, 1421, 1409, 956, 838, 825, 835,
            758, 657, 637, 787, 995, 980, 984, 982, 1123, 1116, 1145, 1226,
            1188, 1213, 1196, 1185, 1181, 1172, 1175, 1198, 1178, 1166, 1191,
            1213, 1208, 1207, 1207, 1219, 1234, 1236, 1218, 1234, 1247, 1244,
            1260, 1266, 1257, 1265, 1267, 1260, 1251, 1259, 1273, 1260, 1266,
            1266, 1259, 1268, 1263, 1255, 1258, 1268, 1268, 1262, 1272, 1269,
            1270, 1250, 1238, 1234, 1270, 1247, 1243, 1204, 1261, 1267, 1256,
            1247, 1254, 1249, 1233, 1262, 1255, 1270, 1257, 1246, 1258, 1249,
            1228, 1219, 1154, 1164, 1269, 1299, 1264, 1278, 1229, 1118, 1124,
            1139, 1167, 1086, 1002, 1039, 1172, 991, 932, 991, 920, 984, 1140,
            910, 859, 886, 1006, 930, 874, 959, 1263, 1360, 1021, 824, 753,
            713, 753, 779, 878, 921, 1423, 1001, 926, 943, 949, 924, 757, 642,
            630, 633, 631, 626, 634, 706, 812, 925, 978, 1072, 1698, 1737, 964,
            727, 627, 486, 444, 430, 433, 452, 469, 670, 684, 790, 1083, 1077,
            1207, 2082, 2079, 2119, 1030, 769, 705, 729, 606, 403, 383, 381,
            404, 440, 2467, 2457, 2472, 2527, 2544, 431, 507, 483, 2927, 2951,
            499, 536, 546, 537, 563, 575, 576, 3326, 3351, 3404, 3441, 3445,
            3460, 3508, 3527, 3700, 3875, 3951, 4092, 4273, 4368, 4421, 4687,
            4816, 5080, 5265, 5559, 5730, 6197, 6377, 6606, 7073, 7605, 8452,
            380, 416, 382, 377, 382, 416, 444, 455, 422, 4428, 4376, 4354,
            4362, 4408, 4454, 4428, 4378, 4376, 4405, 9909, 9937, 9919, 2468,
            2450, 2424, 2411, 2396, 2422, 2406, 2400, 2273, 2213, 2194, 2204,
            2203, 2211, 2234, 2296, 9986, 4766, 4745, 4764, 4813, 9993, 10038,
            10077, 10102, 1876, 1821, 1816, 1828, 1803, 1777, 1780, 1783, 1801,
            1808, 1816, 1853, 4257, 4181, 4200, 4260, 4329, 10691, 10726,
            10740, 10759, 10798, 10821, 4160, 4121, 4090, 1743, 1698, 1679,
            1649, 1667, 1648, 1651, 1663, 1690, 1801, 2077, 3211, 3236, 3218,
            3228, 3262, 11950, 3262, 3267, 3287, 3322, 12297, 12362, 12395,
            12464, 12503, 12596, 3750, 3710, 3652, 3534, 3498, 3497, 3476,
            3466, 3462, 3472, 3447, 3477, 3497, 3540, 3608, 3634, 3621, 3664,
            0, 0] 

    plt.plot( [d/1000. for d in dist], 'o-' )
    arr = [a for a in enumerate(dist)]
    arr = [d for (i,d) in gen10th(arr)]
    a2 = []
    for a in arr:
        a2.extend( [a]*10 )
    plt.plot( [d/1000. for d in a2], 'sr-' )

    plt.plot( [d > 1000. for d in a2], 'sg-' )

    plt.show()

    return
    x = [math.cos(math.radians((i-270)/2.0))*d/1000. for i,d in enumerate(dist)]
    y = [math.sin(math.radians((i-270)/2.0))*d/1000. for i,d in enumerate(dist)]
    plt.plot(x, y, 'o-', linewidth=2)

    arr = [a for a in enumerate(dist)]
    arr = [a for a in gen10th(arr)]
    x = [math.cos(math.radians((i-270)/2.0))*d/1000. for i,d in arr]
    y = [math.sin(math.radians((i-270)/2.0))*d/1000. for i,d in arr]
    plt.plot(x, y, 'rs', linewidth=2, markersize=8)
    plt.show()


def maizeHeight( filename ):
    "count fraction of maize plants higher than 30cm"
    # laser scanner tilted and mounted at 30cm
    # only "back parts" are used
    # used src_laser_* where array of 541 mm readings
    count = 0
    countMaize = 0
    for line in open(filename):
        if len(line)> 10: # skip short lines with number of updates
            arr = eval(line)
            assert len(arr) == 541, len(arr)
            count += 1
            arr = [x == 0 and 10000 or x for x in arr] 
            if min(arr[:90]) < 1000 and  min(arr[-90:]) < 1000:
                # compensate for potential tilt - must be both sides
                countMaize += 1
    return count, countMaize

def statMaizeHeight( roots ):
    totalCount, totalCountMaize = 0, 0
    for root in roots:
        for currentDir, dirs, files in os.walk( root ):
            if "spin" in currentDir or "followme" in currentDir:
                continue
            for name in files:
                if name.startswith("src_laser"):
                    count, countMaize = maizeHeight( filename=os.path.join(currentDir,name) )
                    print name, count, countMaize
                    totalCount += count
                    totalCountMaize += countMaize
    print totalCount, totalCountMaize, "%.2f" % (totalCountMaize/float(totalCount))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(2)
    draw( getArray(sys.argv[1]) )
#    drawScan()
#    statMaizeHeight( roots = sys.argv[1:] )
# vim: expandtab sw=4 ts=4 

