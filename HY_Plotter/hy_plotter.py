import os
import glob
import sys

import json

import datetime
import numpy as np

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from windReader.colormap import colormap as cm
from windReader.rpdgrib import Rpdgrib as rgrib

CONFIG = True
AUTO_SAVE_FIGURE = False

DEFAULT_WIDTH = 5

data_crs = ccrs.PlateCarree()

def calc_figsize(georange):
    latmin, latmax, lonmin, lonmax = georange
    ratio = (latmax - latmin) / (lonmax - lonmin)
    figsize = (DEFAULT_WIDTH, DEFAULT_WIDTH * ratio)
    return figsize

def stepcal(lonmax, lonmin, res, num=15, ip=1):
    totalpt = (lonmax - lonmin) / res * ip
    return int(totalpt / num)

def grid(route, fname, georange, sfname, band, lonlatstep=5, num=15, ip=1, full_res=-1, **kwargs):
    config = kwargs["config"]
    
    lats, lons, data_spd, data_dir, data_time, sate_name, res = rgrib.get_data(route + fname, band, georange)
    
    # transfroming resolution into degree if it's string type
    _res_temp = res
    if isinstance(_res_temp, str):
        if "°" in _res_temp:
            _res_temp = float(_res_temp[:-1])
            res = f"{_res_temp * 100}"
            if res.endswith(".0"):
                res = res[:-2] + "KM"
            else:
                res += "KM"
        elif "KM" in _res_temp.upper():
            _res_temp = float(_res_temp[:-2]) / 100
        else:
            _res_temp = float(_res_temp)
            if "." in res:
                res = f"{_res_temp * 100}"
                if res.endswith(".0"):
                    res = res[:-2] + "KM"
                else:
                    res += "KM"
            else:
                res += "KM"
    
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
        # get an appropriate fig sizes
        figsize = calc_figsize(georange)
    else:
        grange = (-90, 90, 0, 360)
        latmin, latmax, lonmin, lonmax = grange
        # get an appropriate fig sizes
        figsize = calc_figsize(grange)
    
    # set figure-dpi
    dpi = 1500 / DEFAULT_WIDTH
    
    # set axes projection
    if CONFIG:
        proj = getattr(ccrs, config["projection"])
    else:
        proj = ccrs.PlateCarree(central_longitude=180)
    
    
    # set figure and axis
    if CONFIG:
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection=proj(**config["projection_parameters"])))
    else:
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection=proj))
    if isinstance(georange, tuple):
        ax.set_extent([lonmin, lonmax, latmin, latmax], crs=data_crs)
    else:
        ax.set_global()
    ax.patch.set_facecolor("#000000")
    
    # process data's valid time (latest)
    if "CFOSAT" in sate_name:
        try:
            data_time = datetime.datetime.strptime(data_time, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y/%m/%d %H%MZ')
        except Exception:
            data_time = datetime.datetime.strptime(data_time, "%Y-%m-%d %H:%M:%SZ").strftime('%Y/%m/%d %H%MZ')
    elif "HY-2" in sate_name:
        try:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%dT%H:%M:%S").strftime('%Y/%m/%d %H%MZ')
        except Exception:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%dT%H:%M:%S.%f").strftime('%Y/%m/%d %H%MZ')
    elif "FY-3E" in sate_name:
        try:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%d%H%M").strftime('%Y/%m/%d %H%MZ')
        except Exception:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%d %H:%M:%S.%f").strftime('%Y/%m/%d %H%MZ')
    else:
        try:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%dT%H:%M:%S").strftime('%Y/%m/%d %H%MZ')
        except Exception:
            data_time = datetime.datetime.strptime(data_time, "%Y-%m-%d %H:%M:%S").strftime('%Y/%m/%d %H%MZ')
    
    print("...PLOTING...")
    
    # plot brabs with colormap and color-bar
    cmap, vmin, vmax = cm.get_colormap("wind")
    
    ver = np.asarray([spd*np.sin(agl*np.pi/180) for spd,agl in zip(data_spd,data_dir)])
    hriz = np.asarray([spd*np.cos(agl*np.pi/180) for spd,agl in zip(data_spd,data_dir)])
    
    if full_res == -1:
        bs = stepcal(lonmax, lonmin, _res_temp, num, ip)
        _ver = ver[::bs,::bs]
        _hriz = hriz[::bs,::bs]
        _spd = data_spd[::bs,::bs]
        lons, lats = lons[::bs,::bs], lats[::bs,::bs]
    else:
        _ver = ver
        _hriz = hriz
        _spd = data_spd
    
    nh = lats > 0
    
    bb = ax.barbs(
        lons,
        lats,
        _ver,
        _hriz,
        _spd,
        cmap=cmap,
        clim={vmax:vmax, vmin:vmin},
        flip_barb=(~nh),
        pivot='middle',
        length=3.5,
        linewidth=0.5,
        transform=data_crs,
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
    
    '''
    # get area's max wind
    # You can delete these codes if you do not want to show the max wind
    '''
    dspd = data_spd[(lons<=lonmax)&(lons>=lonmin)&(lats<=latmax)&(lats>=latmin)]
    if len(dspd) > 0 and not isinstance(dspd.max(), np.ma.core.MaskedConstant):
        damax = round(dspd.max(), 1)
    else:
        damax = "0.0"

    # add title at the top of figure
    text = f'{sate_name} {res} Wind (barbs) [kt] (Generated by @Shuitai)\nValid Time: {data_time}'
    ax.set_title(text, loc='left', fontsize=5)
    text = f'Max. Wind: {damax}kt'
    ax.set_title(text, loc='right', fontsize=4)
    
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
        crs=data_crs,
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
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.axis("off")
    
    # save figure
    try:
        if sfname == "":
            raise ValueError("File name should not an empty string")
    except ValueError as e:
        print(repr(e))
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
# loading CONFIG parameter for next step on the method of reading config file
if CONFIG:
    with open("config.json", "r") as f:
        config = json.load(f)
        route = config["data_route"]
        file = config["data_file"]
        band = config["wind_band"]
        step = config["lon_lat_step"]
        f_res = int(config["full_res"])
        georange = tuple(config["data_georange"])
        if AUTO_SAVE_FIGURE:
            save_name = file.split(".")[0]
        else:
            save_name = config["save_file"]
else:
    config = dict()
    route = ""
    file = "CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv.nc"
    band = 0
    step = 10
    f_res = -1
    georange = (16.035, 28.035, 221.122, 233.122) # fill in any tuple what you like
    if AUTO_SAVE_FIGURE:
        save_name = file.split(".")[0]
    else:
        save_name = ""  # fill in any name what you like

# finish loading config, start gird
grid(route, file, georange, save_name, band, num=15, ip=1, lonlatstep=step, full_res=f_res, config=config)