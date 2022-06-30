import netCDF4

import numpy as np

class ASCAT(object):

    def extract(fname, georange=(), test=False):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            if test:
                return False
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "ASCAT" in init.title:
            if test:
                return True
            if georange == ():
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
            data_spd = data_spd / 0.514
            lons[lons < 0] += 360
            latmin, latmax, lonmin, lonmax = georange
            lon_mean = (lonmin + lonmax) / 2
            loc = ()
            for ilon, lon in np.ndenumerate(lons):
                if abs(lon_mean - lon) <= 0.25:
                    loc = ilon
                    break
            loc_time = row_time[loc[0],loc[1]]
            from datetime import date, datetime, timedelta
            _time = date(1990, 1, 1)
            _time += timedelta(seconds=loc_time)
            data_time = _time.strftime('%Y%m%dT%H:%M:%S')
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res