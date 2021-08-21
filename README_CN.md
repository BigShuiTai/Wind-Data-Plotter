 ## HY-2-L2B-Data-Plotter
 
 ### 开始
 * 支持：HY-2A/HY-2B/HY-2C卫星微波辐射计SCA L2B HDF5数据  
 * 数据下载：[国家卫星海洋应用中心 NSOAS](https://osdds.nsoas.org.cn)
 
 #### 读取数据
将`hy_plotter.py`中`hy_file = ""`修改为数据所在路径  
```py
hy_file = "C:/Users/Administrator/Desktop/Sat/H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
```  
 #### 选择数据区域
 将`hy_plotter.py`中`grid(hy_file, (-40,-25,150,165), hy_file.replace(".h5", ""))`修改为所需绘制地区经纬，填写时纬度在前经度在后。
 ```py
 grid(hy_file, (17,27,267,277), hy_file.replace(".h5", ""))
 ```
 如遇问题请提交Issues  
 
![H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv](https://user-images.githubusercontent.com/54111871/130322471-36a3eb55-6f9f-4e08-9635-f46821782d0d.png)
