import sys, json
import numpy as np
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import Normalize
plt.rcParams['axes.unicode_minus'] = False

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from windReader.colormap import colormap as cm
from windReader.extract import Extract as extract
from windReader.utils import stepcal, resample

# CONST BLOCK
DEFAULT_WIDTH = 5

def calc_figsize(georange):
    latmin, latmax, lonmin, lonmax = georange
    ratio = (latmax - latmin) / (lonmax - lonmin)
    figsize = (DEFAULT_WIDTH, DEFAULT_WIDTH * ratio)
    return figsize

def grid(config):
    # reading configuration
    route = config["data_route"]
    fname = config["data_file"]
    reader = config["reader"]
    georange = tuple(config["data_georange"])
    sfname = config["save_file"]
    band = config["wind_band"]
    lonlatstep = config["lon_lat_step"]
    num = config["step_in_res"]
    ip = config["ip"]
    crop_area = config["crop_area"]
    full_res = config["full_res"]
    
    # whether using reampling (full resolution scale)
    if str(full_res).upper() in ["0", "TRUE"]:
        full_res = True
    else:
        full_res = False
    
    if str(crop_area).upper() in ["0", "TRUE"]:
        crop_area = True
    else:
        crop_area = False
    
    if isinstance(georange, tuple):
        # get range parameter
        latmin, latmax, lonmin, lonmax = georange
        # process longitude/latitude parameter
        if lonmin < 0:
            lonmin = 360 + lonmin
        if lonmax < 0:
            lonmax = 360 + lonmax
        if lonmin > lonmax:
            lonmin, lonmax = lonmax, lonmin
        if latmin > latmax:
            latmin, latmax = latmax, latmin
        georange = (latmin, latmax, lonmin, lonmax)
        # get an appropriate fig sizes
        figsize = calc_figsize(georange)
    else:
        georange = (-90, 90, 0, 360)
        latmin, latmax, lonmin, lonmax = georange
        # get an appropriate fig sizes
        figsize = calc_figsize(georange)
    
    lats, lons, data_spd, data_dir, data_time, sate_name, res = extract.get_data(route + fname, band, georange, reader=reader)
    
    if not full_res:
        res_num = float(res[:-2])
        bs = stepcal(lonmax, lonmin, res_num, num, ip)
        lons = resample(lons, bs)
        lats = resample(lats, bs)
        data_spd = resample(data_spd, bs)
        data_dir = resample(data_dir, bs)
    
    if crop_area:
        data_spd = data_spd[(lons<=lonmax)&(lons>=lonmin)&(lats<=latmax)&(lats>=latmin)]
        data_dir = data_dir[(lons<=lonmax)&(lons>=lonmin)&(lats<=latmax)&(lats>=latmin)]
        _lons = lons[(lons<=lonmax)&(lons>=lonmin)&(lats<=latmax)&(lats>=latmin)]
        _lats = lats[(lons<=lonmax)&(lons>=lonmin)&(lats<=latmax)&(lats>=latmin)]
        data_spd = data_spd.filled()
        lats, lons = _lats[data_spd!=-32768], _lons[data_spd!=-32768]
        data_spd, data_dir = data_spd[data_spd!=-32768], data_dir[data_spd!=-32768]
    
    # process data's valid time (latest)
    if "CFOSAT" in sate_name:
        try:
            data_time = datetime.strptime(data_time, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            data_time = datetime.strptime(data_time, "%Y-%m-%d %H:%M:%SZ")
    
    '''
    # get area's max wind
    # You can delete these codes if you do not want to show the max wind
    '''
    if len(data_spd) == 0 or isinstance(data_spd.max(), np.ma.core.MaskedConstant):
        print("Empty data for given area.")
        damax = "0.0"
    else:
        damax = "%.01f" % data_spd.max()

    # transfroming resolution string
    sat_title = f"{sate_name}"
    if isinstance(res, str) and res.endswith("KM"):
        sat_title += " " + res
    
    print("...PLOTING...")

    # set figure-dpi
    dpi = 1500 / DEFAULT_WIDTH
    
    # set axes projection
    proj = getattr(ccrs, config["projection"])
    
    # set figure and axis
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection=proj(**config["projection_parameters"])))
    if isinstance(georange, tuple) and not georange == (-90, 90, 0, 360):
        ax.set_extent([lonmin, lonmax, latmin, latmax], crs=ccrs.PlateCarree())
    else:
        ax.set_global()
    ax.patch.set_facecolor("#000000")
    
    # plot brabs with colormap and color-bar
    cmap, vmin, vmax = cm.get_colormap("wind")
    
    ver = np.asarray([spd*np.sin(agl*np.pi/180) for spd,agl in zip(data_spd,data_dir)])
    hriz = np.asarray([spd*np.cos(agl*np.pi/180) for spd,agl in zip(data_spd,data_dir)])
    
    nh = lats > 0
    
    bb = ax.barbs(
        lons,
        lats,
        ver,
        hriz,
        data_spd,
        cmap=cmap,
        norm=Normalize(vmin=vmin, vmax=vmax),
        flip_barb=(~nh),
        pivot='middle',
        length=3.5,
        linewidth=0.25,
        transform=ccrs.PlateCarree(),
    )
    
    cb = plt.colorbar(
        bb,
        ax=ax,
        orientation='vertical',
        pad=0,
        aspect=35,
        fraction=0.03,
        extend='both',
    )
    # set color-bar params
    cb.set_ticks(np.arange(0, 70, 5).tolist())
    cb.ax.tick_params(labelsize=4, length=0)
    cb.outline.set_linewidth(0.3)

    # add coastlines
    ax.add_feature(
        cfeature.COASTLINE.with_scale("10m"),
        facecolor="None",
        edgecolor="k",
        lw=0.5,
    )
    
    # add gridlines
    xticks = np.arange(-180, 181, lonlatstep)
    yticks = np.arange(-90, 91, lonlatstep)
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.6,
        linestyle=':',
        color='k',
        xlocs=xticks,
        ylocs=yticks,
    )
    gl.rotate_labels = False
    gl.top_labels = False
    gl.bottom_labels = True
    gl.right_labels = False
    gl.left_labels = True
    gl.xpadding = 3
    gl.ypadding = 3
    gl.xlabel_style = {'size': 4, 'color': 'k', 'ha': 'center'}
    gl.ylabel_style = {'size': 4, 'color': 'k', 'va': 'center'}

    # add title at the top of figure
    if full_res:
        text = f'{sat_title} Wind (barbs) [kt]'
    else:
        text = f'{sat_title} Wind (barbs) [kt] (Resampled)'
    text += f' (Generated by @Shuitai)\nValid Time: {data_time.strftime("%Y/%m/%d %H%MZ")}'
    ax.set_title(text, loc='left', fontsize=5)
    
    try:
        text = f'Max. Wind: {damax}kt'
        ax.set_title(text, loc='right', fontsize=4)
    except NameError:
        pass
    
    plt.axis("off")
    
    # save figure
    try:
        if sfname == "":
            raise ValueError("File name should not an empty string")
    except ValueError as e:
        print("ERROR:", e)
        sys.exit(0)
    
    ptext = sfname
    plt.savefig(
        ptext,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.02,
    )
    
    plt.close("all")

# main codes
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='HY_plotter')
    parser.add_argument('-c','--config_path', default='config.json')
    args = parser.parse_args()
    with open(args.config_path, "r") as f:
        config = json.load(f)
    main(config)
