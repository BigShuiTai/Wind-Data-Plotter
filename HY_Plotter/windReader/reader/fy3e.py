import h5py

import numpy as np

class FY3E(object):

    def extract(fname, band="C_band"):
        try:
            init = h5py.File(fname, "r")
        except Exception:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        
        if "FY3E" in str(init.attrs["File Name"]):
            # get values
            fns = str(init.attrs["File Name"]).split("_")
            lons, lats = init[band]["wvc_lon"][:], init[band]["wvc_lat"][:]
            data_spd, data_dir = init[band]["wind_speed_selected"][:], init[band]["wind_dir_selected"][:]
            data_time = fns[7] + fns[8]
            sate_name = str(init.attrs["Satellite Name"]).replace("b","").replace("'","") \
                         + " " + str(init.attrs["Sensor Name"]).replace("b","").replace("'","")
            if band == "C_band":
                res = "20KM"
            elif band == "Ku_band":
                res = "10KM"
            else:
                res = "20KM"
            sate_name += " " + band
            # process values
            data_spd = np.ma.array(data_spd, mask=(data_spd==32767), fill_value=0)
            data_dir = np.ma.array(data_dir, mask=(data_dir==32767), fill_value=0)
            data_spd, data_dir = data_spd / 100 / 0.514, data_dir / 10
            lons[lons < 0] += 360
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res