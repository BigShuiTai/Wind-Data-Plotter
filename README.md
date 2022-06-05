# HY-CFOSAT-ASCAT-Wind-Data-Plotter
[中文文档](/README_CN.md) 
  
HY-2 A to D & CFOSAT & MetOp-ASCAT Satellite Wind Speed & Wind Dirctory Data Plotter (Based on HDF5 / netCDF)  

## Starting

 * HY Plotter supports HY-2A/HY-2B/HY-2C/HY-2D SCA L2B data based on HDF5, CFOSAT SCA L2B & MetOp-ASCAT L2 data based on netCDF
 * If you want to download HY-2/CFOSAT data, you can visit: [国家卫星海洋应用中心 NSOAS](https://osdds.nsoas.org.cn)
 * There's no MetOp-ASCAT data source temporarily.

## Modify targeted file in HY Plotter

If you want to load HY-2/CFOSAT/MetOp-ASCAT data in HY Plotter correctly, you must modify the targeted file parameter `hy_file` or `file`. Here's an example: 
```py
# demo codes
config = dict() # In the latest module, config must be an assigned variable, or HY-PLOTTER will raise an error
route = "C:/Users/Administrator/Desktop/Sat/"
hy_file = "H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
grid(route, hy_file, (17, 27, 267, 277), hy_file.replace(".h5", ""), config=config)
```
****For convenience, we have added a config loading method. If you truly want to use config, Here's an example for you:****
 * Firstly, changing the status of CONFIG parameter:
```py
# demo codes
CONFIG = True   # default is False
```
* Then, modifying config.json to correct config for HY Plotter:
```json
{
    "projection": "PlateCarree",
    "projection_parameters": {"central_longitude": 180},
    "data_georange": [12, 14, 125, 127],
    "data_route": "C:/Users/Administrator/Desktop/Sat/",
    "data_file": "CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv.nc",
    "save_file": "CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv"
}
```

## Choosing longitude and latitude range

While plotting HY-2/CFOSAT/MetOp-ASCAT data, you might need setting longitude and latitude range.

If ```georange``` parameter sets ```None``` or ```false```, HY Plotter will set a global extent.

But if you are not setting any values on ```georange```, or it isn't a four-length tuple, HY Plotter will raise an error.

Example:
```py
# demo codes
config = dict() # In the latest module, config must be an assigned variable, or HY-PLOTTER will raise an error
route = "C:/Users/Administrator/Desktop/Sat/"
hy_file = "H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
georange = (17, 27, 267, 277)
grid(route, hy_file, georange, hy_file.replace(".h5", ""), config=config)
```
*  ****Currently only supports CFOSAT EXPR Data, and doesn't support OPER**** 

If you meet some difficulties or bugs, please submit issues to us.

Demo pictures:

![CFO_EXPR_SCA_C_L2B_OR_20210723T100441_15127_125_33_owv](https://user-images.githubusercontent.com/79071461/140613081-0293fbb3-0077-445a-8bf4-269ac1454fb5.png)
