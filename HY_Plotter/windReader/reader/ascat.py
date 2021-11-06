import netCDF4

import numpy as np

class ASCAT(object):

    def extract(fname):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "ASCAT" in init.title:
            # get values
            lons, lats = init.variables["lon"][:], init.variables["lat"][:]
            data_spd, data_dir = init.variables["wind_speed"][:], init.variables["wind_dir"][:]
            data_spd, data_dir = data_spd[:], data_dir[:]
            data_time = f"{init.stop_date} {init.stop_time}"
            sate_name = init.source + " Level 2"
            res = init.pixel_size_on_horizontal.replace(".0", "").replace(" ","")
            # process values
            lons.fill_value = lats.fill_value = data_spd.fill_value = data_dir.fill_value = -32768
            data_spd = data_spd / 0.514
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res