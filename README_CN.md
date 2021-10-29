 ## HY-CFOSAT-L2B-Wind-Data-Plotter
 
 ### 开始
 * 支持：HY-2A/HY-2B/HY-2C卫星微波辐射计SCA L2B HDF5数据 & CFOSAT SCA L2B/MetOp L2 Wind netCDF4数据
 * 数据下载：[国家卫星海洋应用中心NSOAS](https://osdds.nsoas.org.cn) [EUMETSAT](https://www.eumetsat.int/)
 
 #### 读取数据
将`hy_plotter.py`中`route = ""`修改为数据所在路径，`hy_file = ""`修改为数据文件名
```py
route = "C:/Users/Administrator/Desktop/Sat/"
hy_file = "H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
```  
为了方便起见，我们添加了一个配置加载方法。如果想使用config，请按照示例配置：
* 开启CONFIG
```py
# demo codes
CONFIG = True   # default is False
```
* 修改`config.json`进行配置
```json
{
    "projection": "PlateCarree",
    "projection_parameters": {"central_longitude": 180},
    "data_route": "C:/Users/Administrator/Desktop/Sat/",
    "data_file": "CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv.nc"
}
```
 #### 选择数据区域
 将`hy_plotter.py`中`grid(route, hy_file, (-40,-25,150,165), hy_file.replace(".h5", ""))`修改为所需绘制地区经纬，填写时纬度在前经度在后。
*  ****注意：在调用`grid`函数之前，若您未开启config自动读取功能，需提前声明`config`变量为`dict()`，否则会报错****
 ```py
# demo codes
config = dict()
route = "C:/Users/Administrator/Desktop/Sat/"
hy_file = "H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
grid(route, hy_file, (17, 27, 267, 277), hy_file.replace(".h5", ""), config=config)

 ```
 如遇问题请提交Issues  
 
 *  ****注意：目前仅支持CFOSAT EXPR（快交付产品数据），不支持OPER（业务处理数据）****
 
![H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv](https://user-images.githubusercontent.com/54111871/130322471-36a3eb55-6f9f-4e08-9635-f46821782d0d.png)

![CFO_EXPR_SCA_C_L2B_OR_20210801T030812_15259_250_33_owv](https://user-images.githubusercontent.com/79071461/130332521-a5f5c0ad-99f2-472f-b9ce-4b9e1280b3ae.png)

![ascat_20210705_000600_metopc_13795_eps_o_250_3203_ovw](https://user-images.githubusercontent.com/79071461/131166619-12ff979c-f48c-4421-bda4-ce3613efacfc.png)
