import netCDF4

import numpy as np

class CFOSAT(object):

    def extract(fname):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        
        if init.platform == "CFOSAT":
            # get values
            lons, lats = init.variables["wvc_lon"][:], init.variables["wvc_lat"][:]
            data_spd, data_dir = init.variables["wind_speed_selection"][:], init.variables["wind_dir_selection"][:]
            # data_spd, data_dir = data_spd[:,:,band_index], data_dir[:,:,band_index]
            data_time = init.time_coverage_end
            sate_name = f"{init.platform} Scatterometer Level 2B"
            if init.dimensions["numrows"].size == 3248:
                res = "0.125°"
            else:
                res = "0.25°"
            # process values
            data_spd = data_spd / 0.514
            lons[lons < 0] += 360
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res