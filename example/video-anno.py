import os
import sys
import time
import cv2
import pickle
import numpy as np
import pandas as pd

from tqdm import tqdm
from datetime import datetime

DEBUG = False
COLOR = np.array([[0,255, 0], [0,0,255], [255, 255, 255]])


def debug_log(*req):
    if DEBUG:
        for it in req:
            print(it, end=' ')
        
        print("\n------")

def welcome():
    debug_log("=====start=====")
    debug_log("len(argv):", len(sys.argv))
    debug_log("sys.argv:", sys.argv)

def get_input_file():
    n_anno = len(sys.argv) - 2
    assert n_anno >= 1, "argv error"
    video_file = sys.argv[1]
    anno_files = sys.argv[2:]
    
    assert os.path.isfile(video_file), "No such video file"
    for it in anno_files:
        assert os.path.isfile(it), "No such annotation file"
    return video_file, anno_files
    
    
def get_anno(req):
    res = []
    for it in req:
        itype = os.path.basename(it).split('.')[-1]
        if itype == 'npy':
            res.append(np.load(it))
        elif itype == 'pickle':
            res.append(pickle.load(open(it, 'rb')))
        elif itype == 'csv':
            # for deeplabcut csv
            f = pd.read_csv(it, header=2)
            print(len(f))
            n = f.values.shape[1] // 3
            for i in range(n):
                res.append(f.values[:, 1+i*3: 3+i*3])
        else:
            assert 0, 'Annotation file type unsupport'
    return res
    
    
def scatter_lo(X, Y, Xlim, Ylim):
    li = []
    r = 5
    x = int(X)
    y = int(Y)
    for xx in range(x-r, x+r+1):
        for yy in range(y-r, y+r+1):
            d = (xx-X)**2+(yy-Y)**2
            if d <= r*r and xx < Xlim and yy < Ylim and xx >= 0 and yy >= 0:
                li.append((xx,yy))
    return li

    
def main():
    ivideo_file, anno_files = get_input_file()
    ovideo_file = datetime.strftime(datetime.now(),'%Y-%m-%d-%H-%M-%S') + '.avi'
    debug_log("video_file", ivideo_file)
    debug_log("anno_files", anno_files)
    annos = get_anno(anno_files)
    vidcap = cv2.VideoCapture(ivideo_file)
    success, img = vidcap.read()
    
    H, W = img.shape[1], img.shape[0]
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    out = cv2.VideoWriter(ovideo_file, 
                      cv2.VideoWriter_fourcc(*'XVID'), fps, 
                      (H, W))

    for frame in tqdm(range(length)):
        assert success, "Input video reading error"
        for i, it in enumerate(annos):
            try:
                c = it[frame]
            except:
                continue
            area = scatter_lo(c[1], c[0], W, H)
            for p in area:
                img[p[0], p[1], :] = COLOR[i]
        out.write(img)
        success,img = vidcap.read()
    out.release()
    
    
    
    
if __name__ == '__main__':
    welcome()
    main()  
