from windReader.reader import load_reader, test_reader

import numpy as np

class Extract(object):
    
    def get_data(fname, band_index, georange, reader=None, **kwargs):
        if reader in [None, "", "auto"]:
            reader_names = ["hy_hdf", "fy3e_hdf", "cfosat_nc", "metop_ascat_nc"]
            # Auto match reader names
            for _reader_name in reader_names:
                try:
                    _test = test_reader(_reader_name, fname)
                except Exception:
                    print(f"{_reader_name} reader cannot read this file.")
                else:
                    if not _test:
                        print(f"{_reader_name} reader cannot read this file.")
                        continue
                    reader = _reader_name
                    print(f"Using {_reader_name} reader to read this file...")
                    break
            if reader == "":
                raise ValueError("Reader name was not found in the support readers list")
            reader = load_reader(reader)
            if _reader_name == "fy3e_hdf":
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange=georange, band=band_index)
            else:
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange=georange)
        else:
            print(f"Using {reader} reader to read this file...")
            reader = load_reader(reader)
            if reader == "fy3e_hdf":
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange=georange, band=band_index)
            else:
                lats, lons, data_spd, data_dir, data_time, sate_name, res = reader.extract(fname, georange=georange)
        return lats, lons, data_spd, data_dir, data_time, sate_name, res