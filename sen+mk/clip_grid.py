#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:31:59 2021

E-mail: 1321378489@qq.com

@author: xiao_gf

"""
import time,os
from osgeo import gdal
import numba 

@numba.jit  # 程序加速
def clip_batch(in_folder, out_folder, in_shape):
    files = os.listdir(in_folder)
    for file in files:
        if file[-5:] == '.tiff':
            filename = os.path.join(in_folder,file)
            
            in_raster = gdal.Open(filename)
            out_raster = os.path.join(out_folder,file)
            
            ds = gdal.Warp(out_raster,in_raster,format = 'GTiff',
                           cutlineDSName = in_shape,
                           cropToCutline = True,
                           creationOptions=["TILED=YES", "COMPRESS=LZW"],
                           cutlineWhere = None, dstNodata = -999)              

            ds=None 

if __name__=="__main__":
    start = time.perf_counter()     # 开始时间
    year = 2001
    while year < 2021:
        in_shape = r"H:\001zone\00张家口承德地区\zc_boundary\zc\张承边界面合并.shp"    # 矢量范围 
        in_folder = os.path.join(r'H:\001zone\00张家口承德地区\zc_evf\cal_zc_evf\ndvi\ndvi_band',str(year))    # 输入栅格路径
        out_folder=os.path.join(r'H:\001zone\00张家口承德地区\zc_evf\cal_zc_evf\ndvi\clip_ndvi',str(year)) #输出路径
        clip_batch(in_folder, out_folder, in_shape)
        
        
        year += 1
        print(year)
    end = time.perf_counter()     # 结束时间
    print('finish')
    print('Running time: %s Seconds'%(end-start))

