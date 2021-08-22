# HY-2-L2B-Data-Plotter
[中文文档](/README_CN.md) 
  
HY-2 A to C & CFOSAT Satellite Wind Speed & Wind Dirctory Data Plotter (Based on HDF5 / netCDF)  

## Starting

 * HY Plotter supports HY-2A/HY-2B/HY-2C SCA L2B data based on HDF5, and CFOSAT SCA L2B data based on netCDF
 * If you want to download HY-2/CFOSAT data, you can visit: [国家卫星海洋应用中心 NSOAS](https://osdds.nsoas.org.cn)

## Modify targeted file in HY Plotter

If you want to load HY-2/CFOSAT data in HY Plotter correctly, you must modify the targeted file parameter. Here's an example: 
```py
# demo codes
route = "C:/Users/Administrator/Desktop/Sat/"
hy_file = "H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
grid(route, hy_file, (17, 27, 267, 277), hy_file.replace(".h5", ""))
```
****For convenience, we have added a config loading method. If you truly want to use config, Here's an example for you:****
 * Firstly, changing the status of CONFIG parameter:
```py
# demo codes
CONFIG = True // default is False
```
* Then, modifying config.json to correct config for HY Plotter:
```json
{
    "projection": "PlateCarree", /* projection name */
    "projection_parameters": {"central_longitude": 180}, /* projection parameters */
    "data_route": "", /* HY-2/CFOSAT data file route */
    "data_file": "CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv.nc" /* HY-2/CFOSAT data file name */
}
```

## Choosing longitude and latitude range

While plotting HY-2/CFOSAT data, you might need setting longitude and latitude range.

If ```georange``` parameter sets ```None``` or ```false```, HY Plotter will set a global extent.

But if you are not setting any values on ```georange```, or it isn't a four-length turple, HY Plotter will raise an error.

Example:
```py
# demo codes
route = "C:/Users/Administrator/Desktop/Sat/"
hy_file = "H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
georange = (17, 27, 267, 277)
grid(route, hy_file, georange, hy_file.replace(".h5", ""))
```

If you meet some difficulties or bugs, please submit issues to us.

Demo pictures:
![H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv](https://user-images.githubusercontent.com/54111871/130322471-36a3eb55-6f9f-4e08-9635-f46821782d0d.png)

![CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv](https://user-images.githubusercontent.com/79071461/130332521-a5f5c0ad-99f2-472f-b9ce-4b9e1280b3ae.png)
