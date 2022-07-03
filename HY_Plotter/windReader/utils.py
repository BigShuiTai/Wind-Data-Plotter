import numpy as np

def stepcal(lonmax, lonmin, res, num=15, ip=1):
    totalpt = (lonmax - lonmin) / res * ip
    return int(totalpt / num)

def resample(data, bs):
    if len(data.shape) == 1:
        return data[::bs]
    elif len(data.shape) == 2:
        return data[::bs,::bs]
    else:
        raise RuntimeError("Resampled data's shape should not a more-than-2-D array")