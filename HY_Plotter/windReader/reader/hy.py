import h5py

import numpy as np

class HY(object):

    def extract(fname, georange=(), test=False):
        try:
            init = h5py.File(fname, "r")
        except Exception:
            if test:
                return False
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "HY-2" in init.attrs["Platform_ShortName"][-1].decode('utf-8'):
            if test:
                return True
            if georange == ():
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            fns = fname.split("_", -1)
            lons, lats = init["wvc_lon"][:], init["wvc_lat"][:]
            data_spd, data_dir = init["wind_speed_selection"][:], init["wind_dir_selection"][:]
            row_time = init["wvc_row_time"][:]
            sate_name = init.attrs["Platform_ShortName"][-1].decode('utf-8').strip() \
                        + " Scatterometer Level 2B"
            res = "25KM"
            # process values
            lons = np.ma.array(lons, mask=lons == 1.7e+38, fill_value=-32768)
            lats = np.ma.array(lats, mask=lats == 1.7e+38, fill_value=-32768)
            data_spd = np.ma.array(data_spd, mask=data_spd == -32767, fill_value=-32768)
            data_dir = np.ma.array(data_dir, mask=data_dir == -32767, fill_value=-32768)
            data_spd, data_dir = data_spd / 100 / 0.514, data_dir / 10
            lons[lons < 0] += 360
            latmin, latmax, lonmin, lonmax = georange
            lon_mean = (lonmin + lonmax) / 2
            loc = ()
            for ilon, lon in np.ndenumerate(lons):
                if abs(lon_mean - lon) <= 0.25:
                    loc = ilon[0]
                    break
            data_time = row_time[loc].decode('utf-8').strip()
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res