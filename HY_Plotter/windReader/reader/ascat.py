import netCDF4

import numpy as np
from datetime import datetime, timedelta

class ASCAT(object):

    def extract(fname, georange=(), test=False):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            if test:
                return False
            print("metop_ascat_nc reader warning: file not found or NETCDF file error")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "ASCAT" in init.title:
            if test:
                return True
            if not len(georange) == 4:
                print("metop_ascat_nc reader warning: range should be a 4-D tuple")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            lons, lats = init.variables["lon"][:], init.variables["lat"][:]
            data_spd, data_dir = init.variables["wind_speed"][:], init.variables["wind_dir"][:]
            row_time = init.variables["time"][:]
            sate_name = init.source + " Level 2"
            res = init.pixel_size_on_horizontal.replace(".0", "").replace(" ","")
            # process values
            lons.fill_value = lats.fill_value = data_spd.fill_value = data_dir.fill_value = -32768
            data_spd = data_spd / 0.514 / 0.93
            lons[lons < 0] += 360
            latmin, latmax, lonmin, lonmax = georange
            lon_mean = (lonmin + lonmax) / 2
            lat_mean = (latmin + latmax) / 2
            loc = ()
            for (ilon, lon), (ilat, lat) in zip(np.ndenumerate(lons), np.ndenumerate(lats)):
                if abs(lon_mean - lon) <= 0.5 or abs(lat_mean - lat) <= 0.5:
                    loc = ilon
                    break
            try:
                loc_time = int(row_time[loc[0],loc[1]])
                _time = datetime(1990, 1, 1, 0, 0, 0)
                _time += timedelta(seconds=loc_time)
                data_time = _time.strftime('%Y%m%dT%H:%M:%S')
            except Exception:
                loc_time = int(row_time[-1,-1]_
                _time = datetime(1990, 1, 1, 0, 0, 0)
                _time += timedelta(seconds=loc_time)
                data_time = _time.strftime('%Y%m%dT%H:%M:%S')
        else:
            print("metop_ascat_nc reader warning: content of NETCDF file is not ASCAT data")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res
