from windReader.reader import load_reader, test_reader

import numpy as np

class Rpdgrib(object):

    def get_data(fname, band_index, georange, reader_name=""):
        if reader_name == "":
            reader_names = ["hy_hdf", "fy3e_hdf", "cfosat_nc", "metop_ascat_nc"]
            readers = ["HY-Reader", "FY3E-Reader", "CFOSAT-Reader", "ASCAT-Reader"]
            # Auto match reader names
            for _reader_name, _reader in zip(reader_names, readers):
                try:
                    _test = test_reader(_reader_name, fname)
                except Exception:
                    print(f"{_reader} cannot read this file.")
                else:
                    if not _test:
                        print(f"{_reader} cannot read this file.")
                        continue
                    reader_name = _reader_name
                    print(f"Using {_reader} to read this file...")
                    break
            if reader_name == "":
                raise ValueError("Reader name was not found in the support readers list")
            reader = load_reader(reader_name)
            if _reader_name == "fy3e_hdf":
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange, band=band_index)
            else:
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange)
        else:
            reader = load_reader(reader_name)
            if reader_name == "fy3e_hdf":
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange, band=band_index)
            else:
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange)
        return lats, lons, data_spd, data_dir, data_time, sate_name, res