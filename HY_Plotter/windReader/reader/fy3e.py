import h5py
import numpy as np
from datetime import datetime, timedelta

def combine_wvc_time(day_count, millisecond_count, ms_slope):
    # calculate date from 2000-01-01 12:00:00 UTC
    t0 = datetime(2000, 1, 1, 12, 0, 0)
    dc = np.asarray(day_count, dtype=np.float64)
    ms = np.asarray(millisecond_count, dtype=np.float64)
    if dc.shape != ms.shape:
        raise ValueError(f"Shape mismatch: {dc.shape=} vs {ms.shape=}")
    s = ms * 1e-3 * ms_slope
    out = np.asarray([t0 + timedelta(days=float(d_), seconds=float(s_)) for d_, s_ in zip(dc, s)], dtype=object)
    return out

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
            if not georange or len(georange) == 0:
                # get values
                fns = init.attrs["File Name"].decode('utf-8').split("_")
                lons, lats = init[band]["wvc_lon"][:], init[band]["wvc_lat"][:]
                data_spd, data_dir = init[band]["wind_speed_selected"][:], init[band]["wind_dir_selected"][:]
                day_count, millisecond_count = init[band]["day_count"][:], init[band]["millisecond_count"][:]
                spd_slope = init[band]["wind_speed_selected"].attrs["Slope"]
                dir_slope = init[band]["wind_dir_selected"].attrs["Slope"]
                ms_slope = init[band]["millisecond_count"].attrs["Slope"]
                data_time = combine_wvc_time(day_count, millisecond_count, ms_slope)
                sate_name = init.attrs["Satellite Name"].decode('utf-8') \
                             + " " + init.attrs["Sensor Name"].decode('utf-8')
                res = "10KM" if data_spd.shape[0] == 2201 else "20KM"
                sate_name += " " + band
                # process values
                data_spd = np.ma.array(data_spd, mask=(data_spd==32767), fill_value=-32767)
                data_dir = np.ma.array(data_dir, mask=(data_dir==32767), fill_value=-32767)
                data_spd, data_dir = (data_spd * spd_slope) / 0.514, data_dir * dir_slope
                lons[lons < 0] += 360
                data_spd, data_dir = data_spd.filled(), data_dir.filled()
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            if not len(georange) == 4:
                print("fy3e_hdf reader warning: range should be a 4-D tuple")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            # get values
            fns = init.attrs["File Name"].decode('utf-8').split("_")
            lons, lats = init[band]["wvc_lon"][:], init[band]["wvc_lat"][:]
            data_spd, data_dir = init[band]["wind_speed_selected"][:], init[band]["wind_dir_selected"][:]
            day_count, millisecond_count = init[band]["day_count"][:], init[band]["millisecond_count"][:]
            spd_slope = init[band]["wind_speed_selected"].attrs["Slope"]
            dir_slope = init[band]["wind_dir_selected"].attrs["Slope"]
            ms_slope = init[band]["millisecond_count"].attrs["Slope"]
            sate_name = init.attrs["Satellite Name"].decode('utf-8') \
                         + " " + init.attrs["Sensor Name"].decode('utf-8')
            res = "10KM" if data_spd.shape[0] == 2201 else "20KM"
            sate_name += " " + band
            # process values
            data_spd = np.ma.array(data_spd, mask=(data_spd==32767), fill_value=-32767)
            data_dir = np.ma.array(data_dir, mask=(data_dir==32767), fill_value=-32767)
            data_spd, data_dir = (data_spd * spd_slope) / 0.514, data_dir * dir_slope
            lons[lons < 0] += 360
            # get time
            row_time = combine_wvc_time(day_count, millisecond_count, ms_slope)
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
            print("fy3e_hdf reader warning: content of HDF file is not FY-3E data")
            lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
        return lats, lons, data_spd, data_dir, data_time, sate_name, res
