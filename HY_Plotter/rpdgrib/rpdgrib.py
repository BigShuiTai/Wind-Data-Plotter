import h5py
import netCDF4

import numpy as np

class Rpdgrib(object):

    def extract(fname, band_index):
        HDF_DATA = True
        
        try:
            init = h5py.File(fname, "r")
        except:
            init = netCDF4.Dataset(fname)
            HDF_DATA = False
        
        if HDF_DATA:
            # get values
            fns = fname.split("_", -1)
            lons, lats = init["wvc_lon"][:], init["wvc_lat"][:]
            data_spd, data_dir = init["wind_speed"][:], init["wind_dir"][:]
            data_spd, data_dir = data_spd[:,:,band_index], data_dir[:,:,band_index]
            data_time = str(init["wvc_row_time"][:][init["wvc_row_time"][:] != b''][-1]).replace("b","").replace("'","").strip()
            sate_name = str(init.attrs["Platform_ShortName"][-1]).replace("b","").replace("'","").strip()
            res = "0.25°"
            # process values
            lons, lats = np.ma.array(lons, mask=lons == 1.7e+38, fill_value=-32768), np.ma.array(lats, mask=lats == 1.7e+38, fill_value=-32768)
            data_spd, data_dir = np.ma.array(data_spd, mask=data_spd == -32767, fill_value=-32768), np.ma.array(data_dir, mask=data_dir == -32767, fill_value=-32768)
            data_spd, data_dir = data_spd / 100 / 0.514, data_dir / 10
        else:
            # get values
            lons, lats = init.variables["wvc_lon"][:], init.variables["wvc_lat"][:]
            data_spd, data_dir = init.variables["wind_speed"][:], init.variables["wind_dir"][:]
            data_spd, data_dir = data_spd[:,:,band_index], data_dir[:,:,band_index]
            data_time = init.time_coverage_end
            sate_name = init.platform
            res = f"{(float(a.geospatial_lon_resolution)+float(a.geospatial_lat_resolution))/2}°"
            # process values
            data_spd = data_spd / 0.514
        return lats, lons, data_spd, data_dir, data_time, sate_name, res
