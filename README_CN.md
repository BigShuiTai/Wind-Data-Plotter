# HY-CFOSAT-ASCAT-Wind-Data-Plotter
 
 ### 开始
 * 支持：HY-2A/HY-2B/HY-2C卫星微波辐射计SCA L2B HDF5数据 & CFOSAT SCA L2B/MetOp L2 Wind netCDF4数据 & FY-3E WindRAD C/Ku band HDF5数据
 * 数据下载：[国家卫星海洋应用中心NSOAS](https://osdds.nsoas.org.cn) [EUMETSAT](https://www.eumetsat.int/) [NSMC](http://satellite.nsmc.org.cn/PortalSite/Data/Satellite.aspx)
 
#### 设置CONFIG
在新版中必须设置CONFIG以绘制HY-2/FY-3E WindRAD/CFOSAT/MetOp-ASCAT的数据。
* 参考以下`config.json`进行配置
```javascript
{
    "projection": "Mercator", // Cartopy投影相关配置
    "projection_parameters": {"central_longitude": 180}, // Cartopy投影相关配置
    "reader": "metop_ascat_nc", // 选择相应的读取数据模块，包含hy_hdf, fy3e_hdf, cfosat_nc和metop_ascat_nc
    "wind_band": 0, // 传感器通道，默认为0
    "lon_lat_step": 2, // 为绘图定位坐标，将设置一个相同的x和y步长（经度和纬度）。
    "full_res": 0, // 是否使用原始分辨率，默认为0
    "step_in_res": 20, // 用于重新取样的数据，在使用full_res时无效。
    "ip": 1, // 扩大重采样程度，在使用full_res时将无效，默认为1。
    "crop_area": -1, // 是否对数据进行裁剪以加快绘图速度，注意返回的数据是一维数组类型。
    "data_georange": [16.6, 24.6, 107.6, 115.6], // 裁剪数据的范围，在没有使用crop_area的情况下无效。
    "data_route": "/www/wwwroot/HY-CFOSAT-ASCAT-Wind-Data-Plotter-main/", // 文件路径, 需要在最后加上"/"
    "data_file": "ascat_20220702_010600_metopb_50781_eps_o_coa_3202_ovw.l2.nc", // 输入文件名
    "save_file": "ascat_20220702_010600_metopb_50781_eps_o_coa_3202_ovw_l2" // 输出文件名
}
```
#### 绘制
运行`hy_plotter.py`

如遇问题请提交Issues  
 
 *  ****注意：目前仅支持CFOSAT EXPR（快交付产品数据），不支持OPER（业务处理数据）****
 
![H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv](https://user-images.githubusercontent.com/54111871/130322471-36a3eb55-6f9f-4e08-9635-f46821782d0d.png)

![CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv](https://user-images.githubusercontent.com/79071461/130332521-a5f5c0ad-99f2-472f-b9ce-4b9e1280b3ae.png)

![ascat_20210705_000600_metopc_13795_eps_o_250_3203_ovw](https://user-images.githubusercontent.com/79071461/131166619-12ff979c-f48c-4421-bda4-ce3613efacfc.png)
