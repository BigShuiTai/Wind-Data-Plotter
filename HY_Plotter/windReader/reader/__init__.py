from windReader.reader.ascat import ASCAT
from windReader.reader.cfosat import CFOSAT
from windReader.reader.hy import HY
from windReader.reader.fy3e import FY3E

WIND_READER_CONFIG = {"metop_ascat_nc": ASCAT, "cfosat_nc": CFOSAT, "hy_hdf": HY, "fy3e_hdf": FY3E}

def load_reader(reader_name):
    return WIND_READER_CONFIG[reader_name]

def test_reader(reader_name, fname):
    try:
        lats, lons, data_spd, data_dir, data_time, sate_name, res = WIND_READER_CONFIG[reader_name].extract(fname)
        if res == "":
            return False
        else:
            return True
    except Exception:
        return False