import netCDF4

import numpy as np

class CFOSAT(object):

    def extract(fname, georange=(), test=False):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            if test:
                return False
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if init.platform == "CFOSAT":
            if test:
                return True
            if georange == ():
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            lons, lats = init.variables["wvc_lon"][:], init.variables["wvc_lat"][:]
            data_spd, data_dir = init.variables["wind_speed_selection"][:], init.variables["wind_dir_selection"][:]
            row_time = init.variables["row_time"][:]
            sate_name = f"{init.platform} Scatterometer Level 2B"
            if init.dimensions["numrows"].size == 3248:
                res = 0.125
            else:
                res = 0.25
            # process values
            lons.fill_value = lats.fill_value = data_spd.fill_value = data_dir.fill_value = -32768
            data_spd = data_spd / 0.514
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
                loc_time = row_time[loc[0]]
                data_time = ''
                for t in loc_time:
                    data_time += t.decode('utf-8')
            except Exception:
                loc_time = row_time[-1]
                data_time = ''
                for t in loc_time:
                    data_time += t.decode('utf-8')
        else:
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res