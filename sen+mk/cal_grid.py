def gdal_analysis(in_path,out_csv):
    """
    读取栅格文件，批量统计栅格的文件名、计数、最小值、最大值、总和、平均值、中位数、标准差。并将统计结果保存为表格（.csv）文件。
    in_path:待统计的栅格所在的文件夹
    out_csv:生成的表格.csv文件所存放的位置
    """
    from osgeo import gdal
    import pandas as pd
    import numpy as np
    import os
    tifs = [os.path.join(in_path,i) for i in os.listdir(in_path) if i.endswith(".tif")]
    res = []
    for in_tif in tifs:
        bname = os.path.basename(in_tif)
        fname = os.path.splitext(bname)[0]
        rds = gdal.Open(in_tif)  # type:gdal.Dataset
        if rds.RasterCount != 1:
            print("Warning, RasterCount > 1")
        band = rds.GetRasterBand(1)  # type:gdal.Band
        ndv = band.GetNoDataValue() # nodata value
        low = 0 # ndvi<0的区域为水体，对这部分的点进行排除

        # 读取栅格至大小为n*1的数组中
        values = np.array(band.ReadAsArray()).ravel() 
        # 排除空值区
        values = values[values != ndv]
        # 排除水域
        values = values[values > low]
        # 植被指数乘以缩放因子scale_factor,默认为0.0001
        #scale_factor = 0.0001
        scale_factor = 1
        values = values * scale_factor
        temp = [fname,values.size,np.min(values),np.max(values),np.sum(values),np.mean(values),np.median(values),np.std(values)]
        res.append(temp)
    res = pd.DataFrame(res)
    res.columns = ["fileName","count","min","max","sum","mean","median","std"]
    res.to_csv(out_csv)

if __name__ == '__main__':
    
    path1 = r"H:\scriptTest\input" # 输入：待统计栅格所在的文件夹
    csv1 = r"H:\scriptTest\input\result.csv" # 输出：包含统计结果的表格文件
    gdal_analysis(path1,csv1)

