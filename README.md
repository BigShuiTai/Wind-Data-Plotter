# HY-CFOSAT-ASCAT-Wind-Data-Plotter
[中文文档](/README_CN.md) 
  
HY-2 A to D & FY-3E C/Ku band & CFOSAT & MetOp-ASCAT Satellite Wind Speed & Wind Dirctory Data Plotter (Based on HDF5 / netCDF)  

## Starting

 * HY Plotter supports HY-2A/HY-2B/HY-2C/HY-2D SCA L2B data based on HDF5, CFOSAT SCA L2B & MetOp-ASCAT L2 data based on netCDF, and FY-3E WindRAD C/Ku band L2 data based on HDF5.
 * If you want to download HY-2/CFOSAT data, you can visit: [国家卫星海洋应用中心 NSOAS](https://osdds.nsoas.org.cn)
 * For MetOp-ASCAT data, you can visit [EUMETSAT](https://www.eumetsat.int/)
 * For FY-3E WindRAD C/Ku band L2 data, you should visit [NSMC](http://satellite.nsmc.org.cn/PortalSite/Data/Satellite.aspx)

## Modify targeted file in HY-Plotter

If you want to load HY-2/FY-3E WindRAD/CFOSAT/MetOp-ASCAT data in HY-Plotter correctly, you must modify your configuration and change the ```data_route``` & ```data_file```.

****~~For convenience, we have added a config loading method. If you truly want to use config, here's an example for you:~~****

****In the newest HY-Plotter version, we have changed the setting that you must use the configuration, and we will give you an example to help you configure your config file:****
 * Firstly, check the ```hy_plotter``` to find whether its configuration file is invalid or not
 * Then modifying config.json to correct config for HY-Plotter (The usage for configuration is written below):
```javascript
{
    "projection": "Mercator", // cartopy style
    "projection_parameters": {"central_longitude": 180}, // cartopy style
    "reader": "metop_ascat_nc", // readers such as hy_hdf, fy3e_hdf, cfosat_nc, and metop_ascat_nc
    "wind_band": 0, // bands of sensor, like C_band in FY-3E WindRAD, default is 0 (or None)
    "lon_lat_step": 2, // for coordinate, will set a same step in x & y (or longitude & latitude)
    "full_res": 0, // whether using full resolution scale, or resampling data
    "step_in_res": 20, // for resampling data, will invalid in using full_res
    "ip": 1, // enlarge resampling degree, will invalid in using full_res
    "crop_area": -1, // whether cropping data for faster plotting, but NOTICE that the returned data is 1-D array type
    "data_georange": [16.6, 24.6, 107.6, 115.6], // range for cropping data, will invalid in no using crop_area
    "data_route": "/www/wwwroot/HY-CFOSAT-ASCAT-Wind-Data-Plotter-main/", // file route, need adding "/" at the end
    "data_file": "ascat_20220702_010600_metopb_50781_eps_o_coa_3202_ovw.l2.nc", // file name
    "save_file": "ascat_20220702_010600_metopb_50781_eps_o_coa_3202_ovw_l2" // file name in saving figure
}
```

## Choosing longitude and latitude range

 * The setting method is the same as the comment written in the previous section

## NOTICE

 * ****Currently only supports CFOSAT EXPR Data, and doesn't support OPER**** 

If you meet some difficulties or bugs, please submit issues to us.

Demo pictures:

![H2B_OPER_SCA_L2B_OR_20220702T210807_20220702T222820_18502_pwp_250_08_owv.png](https://user-images.githubusercontent.com/79071461/177023454-2a3c70ad-6415-4dff-a448-3ac51e667b5d.png)
