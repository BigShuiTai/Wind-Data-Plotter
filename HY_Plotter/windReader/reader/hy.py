import h5py

import numpy as np

class HY(object):

    def extract(fname, band_index=0):
        try:
            init = h5py.File(fname, "r")
        except Exception:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        
        if "HY" in str(init.attrs["Platform_ShortName"][-1]):
            # get values
            fns = fname.split("_", -1)
            lons, lats = init["wvc_lon"][:], init["wvc_lat"][:]
            data_spd, data_dir = init["wind_speed_selection"][:], init["wind_dir_selection"][:]
            data_spd, data_dir = data_spd[:,:,band_index], data_dir[:,:,band_index]
            data_time = str(init["wvc_row_time"][:][init["wvc_row_time"][:] != b''][-1]).replace("b","").replace("'","").strip()
            sate_name = str(init.attrs["Platform_ShortName"][-1]).replace("b","").replace("'","").strip() + " Scatterometer Level 2B"
            res = "0.25°"
            # process values
            lons, lats = np.ma.array(lons, mask=lons == 1.7e+38, fill_value=-32768), np.ma.array(lats, mask=lats == 1.7e+38, fill_value=-32768)
            data_spd, data_dir = np.ma.array(data_spd, mask=data_spd == -32767, fill_value=-32768), np.ma.array(data_dir, mask=data_dir == -32767, fill_value=-32768)
            data_spd, data_dir = data_spd / 100 / 0.514, data_dir / 10
            lons[lons < 0] += 360
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res