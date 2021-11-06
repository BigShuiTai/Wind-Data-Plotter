from windReader.reader import load_reader, test_reader

import numpy as np

class Rpdgrib(object):

    def get_data(fname, band_index, reader_name=""):
        if reader_name == "":
            # Auto match reader names
            try:
                _test = test_reader("hy_hdf", fname)
                _reader_name = "hy_hdf"
            except Exception:
                _test = False
                print("HY-Reader cannot read this file.")
            if _test:
                reader = load_reader(_reader_name)
                if _reader_name == "hy_hdf":
                    lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, band_index)
                else:
                    lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname)
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            else:
                print("HY-Reader cannot read this file.")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            
            try:
                _test = test_reader("metop_ascat_nc", fname)
                _reader_name = "metop_ascat_nc"
            except Exception:
                _test = False
                print("ASCAT-Reader cannot read this file.")
            if _test:
                reader = load_reader(_reader_name)
                if _reader_name == "hy_hdf":
                    lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, band_index)
                else:
                    lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname)
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            else:
                print("ASCAT-Reader cannot read this file.")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            
            try:
                _test = test_reader("cfosat_nc", fname)
                _reader_name = "cfosat_nc"
            except Exception:
                _test = False
                print("CFOSAT-Reader cannot read this file.")
            if _test:
                reader = load_reader(_reader_name)
                if _reader_name == "hy_hdf":
                    lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, band_index)
                else:
                    lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname)
                return lats, lons, data_spd, data_dir, data_time, sate_name, res
            else:
                print("CFOSAT-Reader cannot read this file.")
                lats, lons, data_spd, data_dir, data_time, sate_name, res = [], [], [], [], "", "", ""
            
            return lats, lons, data_spd, data_dir, data_time, sate_name, res
        else:
            reader = load_reader(reader_name)
            if reader_name == "hy_hdf":
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, band_index)
            else:
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname)
            return lats, lons, data_spd, data_dir, data_time, sate_name, res