import netCDF4
import numpy as np
from datetime import datetime, timedelta

def combine_wvc_time(seconds):
    # calculate wvc time from 1990-01-01 00:00 UTC
    t0 = datetime(1990, 1, 1, 0, 0, 0)
    out = np.empty(seconds.shape, dtype=object)
    for idx, s in np.ndenumerate(seconds):
        out[*idx] = t0 + timedelta(seconds=s)
    return out

class ASCAT(object):

    def extract(fname, georange=(), test=False):
        try:
            init = netCDF4.Dataset(fname)
        except Exception:
            if test: return False
            print("metop_ascat_nc reader warning: file not found or NETCDF file error")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "ASCAT" in init.title:
            if test: return True
            if not georange or len(georange) == 0:
                # get values
                lons, lats = init.variables["lon"][:], init.variables["lat"][:]
                data_spd, data_dir = init.variables["wind_speed"][:], init.variables["wind_dir"][:]
                data_time = combine_wvc_time(init.variables["time"][:])
                sate_name = init.source + " Level 2"
                res = init.pixel_size_on_horizontal.replace(".0", "").replace(" ","").upper()
                # process values
                lons.fill_value = lats.fill_value = 1.7e+38
                data_spd.fill_value = data_dir.fill_value = -32767
                data_spd = data_spd / 0.514 / 0.93
                lons[lons < 0] += 360
                lons, lats = lons.filled(), lats.filled()
                data_spd, data_dir = data_spd.filled(), data_dir.filled()
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            if not len(georange) == 4:
                print("metop_ascat_nc reader warning: range should be a 4-D tuple")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            lons, lats = init.variables["lon"][:], init.variables["lat"][:]
            data_spd, data_dir = init.variables["wind_speed"][:], init.variables["wind_dir"][:]
            sate_name = init.source + " Level 2"
            res = init.pixel_size_on_horizontal.replace(".0", "").replace(" ","").upper()
            # process values
            lons.fill_value = lats.fill_value = 1.7e+38
            data_spd.fill_value = data_dir.fill_value = -32767
            data_spd = data_spd / 0.514 / 0.93
            lons[lons < 0] += 360
            # get time
            row_time = combine_wvc_time(init.variables["time"][:])
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
                    loc = loc_
            try:
                data_time = row_time[*loc]
            except Exception:
                data_time = row_time[-1,-1]
        else:
            print("metop_ascat_nc reader warning: content of NETCDF file is not ASCAT data")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res
