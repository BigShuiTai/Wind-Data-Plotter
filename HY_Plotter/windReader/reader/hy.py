import h5py
import numpy as np
from datetime import datetime

def combine_wvc_time(times):
    out = np.empty(times.shape, dtype=object)
    for idx, t in np.ndenumerate(times):
        time_str = t.decode('utf-8').strip()
        out[*idx] = datetime.strptime(time_str, "%Y%m%dT%H:%M:%S")
    return out

class HY(object):

    def extract(fname, georange=(), test=False):
        try:
            init = h5py.File(fname, "r")
        except Exception:
            if test: return False
            print("hy_hdf reader warning: file not found or HDF file error")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        if "HY-2" in init.attrs["Platform_ShortName"][-1].decode('utf-8'):
            if test: return True
            if not georange or len(georange) == 0:
                # get values
                fns = fname.split("_", -1)
                lons, lats = init["wvc_lon"][:], init["wvc_lat"][:]
                data_spd, data_dir = init["wind_speed_selection"][:], init["wind_dir_selection"][:]
                spd_slope = init["wind_speed_selection"].attrs["scale_factor"]
                dir_slope = init["wind_dir_selection"].attrs["scale_factor"]
                data_time = combine_wvc_time(init["wvc_row_time"][:])
                sate_name = init.attrs["Platform_ShortName"][-1].decode('utf-8').strip() \
                            + " Scatterometer Level 2B"
                res = "25KM"
                # process values
                lons = np.ma.array(lons, mask=lons == 1.7e+38, fill_value=1.7e+38)
                lats = np.ma.array(lats, mask=lats == 1.7e+38, fill_value=1.7e+38)
                data_spd = np.ma.array(data_spd, mask=data_spd == -32767, fill_value=-32767)
                data_dir = np.ma.array(data_dir, mask=data_dir == -32767, fill_value=-32767)
                data_spd, data_dir = (data_spd * spd_slope) / 0.514, data_dir * dir_slope
                lons[lons < 0] += 360
                lons, lats = lons.filled(), lats.filled()
                data_spd, data_dir = data_spd.filled(), data_dir.filled()
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            if not len(georange) == 4:
                print("hy_hdf reader warning: range should be a 4-D tuple")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            fns = fname.split("_", -1)
            lons, lats = init["wvc_lon"][:], init["wvc_lat"][:]
            data_spd, data_dir = init["wind_speed_selection"][:], init["wind_dir_selection"][:]
            spd_slope = init["wind_speed_selection"].attrs["scale_factor"]
            dir_slope = init["wind_dir_selection"].attrs["scale_factor"]
            sate_name = init.attrs["Platform_ShortName"][-1].decode('utf-8').strip() \
                        + " Scatterometer Level 2B"
            res = "25KM"
            # process values
            lons = np.ma.array(lons, mask=lons == 1.7e+38, fill_value=1.7e+38)
            lats = np.ma.array(lats, mask=lats == 1.7e+38, fill_value=1.7e+38)
            data_spd = np.ma.array(data_spd, mask=data_spd == -32767, fill_value=-32767)
            data_dir = np.ma.array(data_dir, mask=data_dir == -32767, fill_value=-32767)
            data_spd, data_dir = (data_spd * spd_slope) / 0.514, data_dir * dir_slope
            lons[lons < 0] += 360
            # get time
            row_time = combine_wvc_time(init["wvc_row_time"][:])
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
                data_time = row_time[loc]
            except Exception:
                data_time = row_time[-1]
        else:
            print("hy_hdf reader warning: content of HDF file is not HY-2 data")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res
