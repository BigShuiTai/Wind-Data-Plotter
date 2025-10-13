import netCDF4
import numpy as np
from datetime import datetime, timedelta, timezone

class CFOSAT(object):

    def extract(fname, georange=(), test=False):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            if test: return False
            print("cfosat_nc reader warning: file not found or NETCDF file error")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if init.platform == "CFOSAT":
            if test: return True
            if not georange or len(georange) == 0:
                lons, lats = init.variables["wvc_lon"][:], init.variables["wvc_lat"][:]
                data_spd, data_dir = init.variables["wind_speed_selection"][:], init.variables["wind_dir_selection"][:]
                data_time = init.variables["row_time"][:]
                sate_name = f"{init.platform} Scatterometer Level 2B"
                res = "12.5KM" if init.dimensions["numrows"].size == 3248 else "25KM"
                # process values
                lons.fill_value = lats.fill_value = 1.7e+38
                data_spd.fill_value = data_dir.fill_value = -32767
                data_spd = data_spd / 0.514
                lons[lons < 0] += 360
                lons, lats = lons.filled(), lats.filled()
                data_spd, data_dir = data_spd.filled(), data_dir.filled()
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            if not len(georange) == 4:
                print("cfosat_nc reader warning: range should be a 4-D tuple")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            lons, lats = init.variables["wvc_lon"][:], init.variables["wvc_lat"][:]
            data_spd, data_dir = init.variables["wind_speed_selection"][:], init.variables["wind_dir_selection"][:]
            sate_name = f"{init.platform} Scatterometer Level 2B"
            res = "12.5KM" if init.dimensions["numrows"].size == 3248 else "25KM"
            # process values
            lons.fill_value = lats.fill_value = 1.7e+38
            data_spd.fill_value = data_dir.fill_value = -32767
            data_spd = data_spd / 0.514
            lons[lons < 0] += 360
            # get time
            row_time = init.variables["row_time"][:]
            latmin, latmax, lonmin, lonmax = georange
            lon_mean = (lonmin + lonmax) / 2
            lat_mean = (latmin + latmax) / 2
            loc, min_dist = np.nan, 1000
            locs = []
            for (ilon, lon), (ilat, lat) in zip(np.ndenumerate(lons), np.ndenumerate(lats)):
                if lon >= lonmin and lon <= lonmax and lat >= latmin and lat <= latmax:
                    locs.append((ilon, lon, lat))
            for loc_meta in locs:
                loc_, lon_, lat_ = loc_meta
                lon_diff = abs(lon_ - lon_mean)
                lat_diff = abs(lat_ - lat_mean)
                lonlat_dist = np.sqrt(lon_diff**2 + lat_diff**2)
                if lonlat_dist <= min_dist:
                    min_dist = lonlat_dist
                    loc = loc_[0]
            try:
                loc_time = row_time[loc]
                data_time = ''
                for t in loc_time:
                    data_time += t.decode('utf-8')
            except Exception:
                loc_time = row_time[-1]
                data_time = ''
                for t in loc_time:
                    data_time += t.decode('utf-8')
        else:
            print("cfosat_nc reader warning: content of NETCDF file is not CFOSAT data")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res
