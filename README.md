# HY-2-L2B-Data-Plotter
[中文文档](/README_CN.md) 
  
HY-2 A to C Satellite Wind Speed & Wind Dirctory Data Plotter (Based on HDF5)   

## Starting

 * HY Plotter supports HY-2A/HY-2B/HY-2C SCA L2B data based on HDF5
 * If you want to download HY-2 data, you can go to:[国家卫星海洋应用中心 NSOAS](https://osdds.nsoas.org.cn)

## Modify targeted file in HY Plotter

If you want to load HY-2 data in HY Plotter correctly, you must modify the targeted file parameter. Here's an example: 
```py
# demo codes
hy_file = "C:/Users/Administrator/Desktop/Sat/H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
grid(hy_file, (17, 27, 267, 277), hy_file.replace(".h5", ""))
```

## Choosing longitude and latitude range

While plotting HY-2 data, you might need setting longitude and latitude range.

If ```georange``` parameter sets ```None``` or ```false```, HY Plotter will set a global extent.

But if you are not setting any values on ```georange```, or it isn't a four-length turple, HY Plotter will raise an error.

Example:
```py
# demo codes
hy_file = "C:/Users/Administrator/Desktop/Sat/H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv.h5"
georange = (17, 27, 267, 277)
grid(hy_file, georange, hy_file.replace(".h5", ""))
```

If you meet some difficulties or bugs, please submit issues to us.

Demo picture:
![H2B_OPER_SCA_L2B_OR_20210819T225905_20210820T004328_14133_pwp_250_07_owv](https://user-images.githubusercontent.com/54111871/130322471-36a3eb55-6f9f-4e08-9635-f46821782d0d.png)
