#!/usr/bin/python
# vim: set fileencoding=utf-8 et sts=4 sw=4:
from __future__ import absolute_import, division, print_function, unicode_literals
from common import Position, transponse
from logparser import EduroMaxiReader
import sys, os
from math import sin, cos, atan, radians

reader_x, reader_y, reader_z = -0.3, 0.14, 0.23

def tag2pos(tag):
    zone = tag&0xff
    x=float((tag>>24)&0xff)
    y=7.- float((tag>>16)&0xff)
    return Position(x, y, zone)


def dist(a,b):
    return ((a.x-b.x)**2+(a.y-b.y)**2)**0.5


def getDistanceToTag(robot, tag):
    reader=transponse(robot, Position(-0.3, 0.14, 0))
    tagposition=tag2pos(tag)
    distance2dsquare = (reader.x-tagposition.x)**2 + (reader.y-tagposition.y)**2
    distance = (distance2dsquare + reader_z**2)**0.5
    return distance


if __name__ == "__main__":
    fn=sys.argv[1]
    run=int(sys.argv[2]) if len(sys.argv)>=3 else None
    outfn=os.path.join('outputs',os.path.splitext(os.path.split(fn)[1])[0])
    if run:
        outfn+=+'_%02i'%run
    outfn+='.csv'
    loggenerator=EduroMaxiReader(fn)
    if run:
        runs=(run-1,)
    else:
        runs=range(len(loggenerator.runconfig))

    with open(outfn, 'w') as f:
        f.write(';'.join(("run", "time", "x", "y", "a", "tagid", "RSSI", "computed"))+'\n')
        for run in runs:
            loggenerator.startrun(run)
            for time, pose, msgs in loggenerator:
                if 'RFU620LOG' in msgs and msgs['RFU620LOG']:
                    _, scans  = msgs['RFU620LOG']
                    for scan in scans:
                        distance = getDistanceToTag(pose, scan.id)
                        data=[run+1,time, pose.x, pose.y, pose.a, hex(scan.id), scan.RSSI, distance ]
                        f.write(';'.join(map(str,data))+'\n')
