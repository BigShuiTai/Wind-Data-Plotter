import h5py

import numpy as np

class FY3E(object):

    def extract(fname, georange=(), band="C_band", test=False):
        try:
            init = h5py.File(fname, "r")
        except Exception:
            if test:
                return False
            print("fy3e_hdf reader warning: file not found or HDF file error")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "FY3E" in str(init.attrs["File Name"]):
            if test:
                return True
            if not len(georange) == 4:
                print("fy3e_hdf reader warning: range should be a 4-D tuple")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            fns = init.attrs["File Name"].decode('utf-8').split("_")
            lons, lats = init[band]["wvc_lon"][:], init[band]["wvc_lat"][:]
            data_spd, data_dir = init[band]["wind_speed_selected"][:], init[band]["wind_dir_selected"][:]
            data_time = fns[7] + fns[8]
            sate_name = init.attrs["Satellite Name"].decode('utf-8') \
                         + " " + init.attrs["Sensor Name"].decode('utf-8')
            if band == "C_band":
                res = "20KM"
            elif band == "Ku_band":
                res = "10KM"
            else:
                res = "20KM"
            sate_name += " " + band
            # process values
            data_spd = np.ma.array(data_spd, mask=(data_spd==32767), fill_value=-32768)
            data_dir = np.ma.array(data_dir, mask=(data_dir==32767), fill_value=-32768)
            data_spd, data_dir = data_spd / 100 / 0.514, data_dir / 10
            lons[lons < 0] += 360
        else:
            print("fy3e_hdf reader warning: content of HDF file is not FY-3E data")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res