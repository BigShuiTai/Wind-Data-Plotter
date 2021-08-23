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

from rpdgrib.colormap import colormap as cm
from rpdgrib.rpdgrib import Rpdgrib as rgrib

CONFIG = True
AUTO_SAVE_FIGURE = False

DEFAULT_WIDTH = 5

data_crs = ccrs.PlateCarree()

def calc_figsize(georange):
    latmin, latmax, lonmin, lonmax = georange
    ratio = (latmax - latmin) / (lonmax - lonmin)
    figsize = (DEFAULT_WIDTH, DEFAULT_WIDTH * ratio)
    return figsize

def grid(route, fname, georange, sfname, **kwargs):
    config = kwargs["config"]
    
    lats, lons, data_spd, data_dir, data_time, sate_name = rgrib.extract(route + fname, 0)
    
    if not georange == None and not georange == False:
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
    else:
        georange = (-89, 89, 1, 359)
        latmin, latmax, lonmin, lonmax = georange
    
    # get an appropriate fig sizes
    figsize = calc_figsize(georange)
    
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
    if not georange == None and not georange == False:
        ax.set_extent([lonmin, lonmax, latmin, latmax], crs=data_crs)
    else:
        ax.set_global()
    ax.patch.set_facecolor("#000000")
    
    # process data's valid time (latest)
    if sate_name == "CFOSAT":
        data_time = datetime.datetime.strptime(data_time, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y/%m/%d %H%MZ')
    else:
        try:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%dT%H:%M:%S").strftime('%Y/%m/%d %H%MZ')
        except Exception:
            data_time = datetime.datetime.strptime(data_time, "%Y%m%dT%H:%M:%S.%f").strftime('%Y/%m/%d %H%MZ')
    
    print("...PLOTING...")
    
    '''
    # get area's max wind
    # You can delete these codes if you do not want to show the max wind
    '''
    dspd = []
    lon, lat, data = lons.filled(), lats.filled(), data_spd.filled()
    for i in range(len(lon)):
        for j in range(len(lon[i])):
            if lon[i][j] == -32768 or lat[i][j] == -32768:
                continue
            if lon[i][j] < 0:
                lon[i][j] = 360 + lon[i][j]
            if lon[i][j] <= lonmax and lon[i][j] >= lonmin and lat[i][j] <= latmax and lat[i][j] >= latmin:
                if not data[i][j] == -32768:
                    dspd.append(data[i][j])
            else:
                continue
    if len(dspd) > 0:
        damax = round(max(dspd), 1)
    else:
        damax = "0.0"
    
    # add annotate at the top of figure
    text = f'{sate_name} Scatterometer Level 2B 10-meter Wind (brabs) [kt]\nValid Time: {data_time}'
    ax.set_title(text, loc='left', fontsize=5)
    text = f'Max. Wind: {damax}kt'
    ax.set_title(text, loc='right', fontsize=4)
    
    # plot brabs with colormap and color-bar
    cmap, vmin, vmax = cm.get_colormap("hy")
    ver = np.asarray([spd*np.sin(agl*np.pi/180) for spd,agl in zip(data_spd,data_dir)])
    hriz = np.asarray([spd*np.cos(agl*np.pi/180) for spd,agl in zip(data_spd,data_dir)])
    bb = ax.barbs(
        lons,
        lats,
        ver,
        hriz,
        data_spd,
        cmap=cmap,
        clim={vmax:vmax, vmin:vmin},
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
        aspect=50,
        fraction=0.02,
    )
    # set color-bar params
    cb.set_ticks([5, 15, 25, 35, 45, 55, 65])
    cb.ax.tick_params(labelsize=4)
    
    # add coastlines
    ax.add_feature(
        cfeature.COASTLINE.with_scale("10m"),
        facecolor="None",
        edgecolor="k",
        lw=0.5,
    )
    
    # add gridlines
    dlon = round((lonmax - lonmin) / 4, 2)
    dlat = round((latmax - latmin) / 4, 2)
    xticks = np.arange(int(lonmin - lonmin%dlon) - dlon, int(lonmax - lonmax%-dlon) + dlon, dlon)
    yticks = np.arange(int(latmin - latmin%dlat) - dlat, int(latmax - latmax%-dlat) + dlat, dlat)
    # fix labels location
    x = xticks[(xticks>lonmin) & (xticks<lonmax)]
    y = yticks[(yticks>latmin) & (yticks<latmax)]
    # fix xticks
    xi = np.where(xticks > 180)
    for i in range(len(xi[0])):
        xticks[xi[0][i]] = xticks[xi[0][i]] - 360
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=False,
        linewidth=0.6,
        linestyle=':',
        color='k',
        xlocs=xticks,
        ylocs=yticks,
    )
    # add x/y labels
    for i in yticks:
        if i < latmin or i > latmax:
            continue
        if i - int(i) == 0:
            i = int(i)
        if i > 0:
            j = str(round(i, 2)) + "°N"
        elif i < 0:
            j = str(round(-1 * i, 2)) + "°S"
        else:
            j = str(int(i)) + "°"
        plt.text(
            transform=data_crs,
            s=j,
            x=lonmin - dlon * 0.05,
            y=i,
            ha="right",
            va="center",
            fontsize=4,
            family="DejaVu Sans",
            weight="500",
            color="k"
        )
    for i in xticks:
        if i - int(i) == 0:
            i = int(i)
        if i > 180:
            j = str(str(round(360 - i, 2))) + "°W"
            k = i
        elif i < 180 and i > 0:
            j = str(round(i, 2)) + "°E"
            k = i
        elif i < 0:
            j = str(round(-1 * i, 2)) + "°W"
            k = 360 + i
        else:
            j = str(int(i)) + "°"
            k = i
        if k < lonmin or k > lonmax:
            continue
        plt.text(
            transform=data_crs,
            s=j,
            x=i,
            y=latmin - dlat * 0.05,
            ha="center",
            va="top",
            fontsize=4,
            family="DejaVu Sans",
            weight="500",
            color="k"
        )
    
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
        georange = tuple(config["data_georange"])
        if AUTO_SAVE_FIGURE:
            save_name = file.split(".")[0]
        else:
            save_name = config["save_file"]
else:
    route = ""
    file = "CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv.nc"
    georange = (16.035, 28.035, 221.122, 233.122) # fill in any tuple what you like
    if AUTO_SAVE_FIGURE:
        save_name = file.split(".")[0]
    else:
        save_name = ""  # fill in any name what you like
if not isinstance(georange, tuple):
    raise
# finish loading config, start gird
grid(route, file, georange, save_name, config=config)
