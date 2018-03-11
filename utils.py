import json
import os
import sys
import logging
import ipyparallel
import numpy as np

def load_config(file='config.json'):
    with open(file, 'r') as f:
        return json.load(f)

def load_logger(file='output', level=logging.DEBUG):
    logger = logging.getLogger()

    # File Handler
    fhandler = logging.FileHandler(filename='[{:}.log'.format(file), mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)

    # Output stream Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.setLevel(level)
    ch.setLevel(level)

    return logger

def load_parallel_pool():
    return ipyparallel.Client()

def generateOutputCQTList(out_dir, artist, SUFFIX='_cqtList.txt'):
    return os.path.join(out_dir, artist + SUFFIX)

def pitch_shift_CQT(M, shiftBins):
    """
        pitchshift equivalent of Prof Tsai's code in matlab

        M: a 2-D CQT matrix
        shiftBins: An integer that indicates the pitch to shift to

        return: a pitchshifted matrix
    """
    shifted = np.roll(M, shiftBins, axis=0)
    if shiftBins > 0:
        shifted[:shiftBins, :] = 0.
    else:
        shifted[shiftBins:, :] = 0.
    return shifted

def get_querytoref(artist, listdir):
    '''
        artist: a string representing the artist
        listdir: a string representing the directory of the .list file

        returns an array of integer, where each entry corresponds to the
            reference index
    '''

    ref_idxs = []
    f = open(listdir+artist+'_querytoref.list', 'r')
    for line in f:
        ref_idx = (line.split(' '))[1]
        ref_idxs.append(int(ref_idx))
    f.close()
    return ref_idxs