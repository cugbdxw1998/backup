
# -*- coding: utf-8 -*-
import glob

from osgeo import gdal
import numpy as np
import os

'''
说明：
    提取img数据中的红、绿、近红外波段数据
        Rrs_555	绿波段（62）
        Rrs_645	红波段（63）
        Rrs_859	近红外波段（64）
        注：下划线后的数字为对应波段的中心波长
'''

def writeTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):  # 定义函数writeTiff
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


if __name__ == '__main__':
    gdal.AllRegister()

    year = 2002
    while year < 2021:
        path_mother = os.path.join('H:\\001zone\\00张家口承德地区\\zc_evf\\image\\sebs_Interpolation\\lpp',str(year)) # 输入路径，文件夹
        path_out = os.path.join('H:\\001zone\\00张家口承德地区\\zc_evf\\cal_zc_evf\\ndvi_band',str(year))  # 输出路径，文件夹

        # 获取该目录下所有文件，存入列表中
        os.chdir(path_mother)
        for file in glob.glob('*.img'):
            img_file_name = path_mother + os.sep + file
            dataset = gdal.Open(img_file_name)

            filename = str(file.split('_')[0])
            print(filename)
            
            month = int(filename[4:6])
            adfGeoTransform = dataset.GetGeoTransform()

            band_1 = dataset.GetRasterBand(1)   # 读取数据集的属性，选择待提取波段.62,63,64代表的是波段其在img中的序列号（绿波段在img影像中位于第62个波段）
            #band_2 = dataset.GetRasterBand(63)
            #band_3 = dataset.GetRasterBand(64)

            im_width = dataset.RasterXSize  # 栅格矩阵的列数
            im_height = dataset.RasterYSize  # 栅格矩阵的行数

            Rrs_1 = band_1.ReadAsArray(0, 0, im_width, im_height)  # 目标波段
            #Rrs_2 = band_2.ReadAsArray(0, 0, im_width, im_height)
            #Rrs_3 = band_3.ReadAsArray(0, 0, im_width, im_height)

            im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
            im_proj = dataset.GetProjection()  # 获取投影信息

            im_bands = 1  # band_469.RasterCount  # 输出文件的波段数
            if month == 1:
                B1 = Rrs_1 * 31  # / 10000
            elif month == 2:
                B1 = Rrs_1 * 28
            elif month == 3:
                B1 = Rrs_1 * 31
            elif month == 4:
                B1 = Rrs_1 * 30
            elif month == 5:
                B1 = Rrs_1 * 31
            elif month == 6:
                B1 = Rrs_1 * 30
            elif month == 7:
                B1 = Rrs_1 * 31
            elif month == 8:
                B1 = Rrs_1 * 31
            elif month == 9:
                B1 = Rrs_1 * 30
            elif month == 10:
                B1 = Rrs_1 * 31
            elif month == 11:
                B1 = Rrs_1 * 30
            elif month == 12:
                B1 = Rrs_1 * 31

            #B2 = Rrs_2 * 1.0  # / 10000
            #B3 = Rrs_3 * 1.0  # / 10000

            outpath_1 = path_out + os.sep + filename  + '.tiff'
            writeTiff(B1, im_width, im_height, im_bands, im_geotrans, im_proj, outpath_1)

            #outpath_2 = path_out + os.sep + filename + '_Rrs_645.Red' + '.tif'
            #writeTiff(B2, im_width, im_height, im_bands, im_geotrans, im_proj, outpath_2)

            #outpath_3 = path_out + os.sep + filename + '_Rrs_859.NIR' + '.tif'
            #writeTiff(B3, im_width, im_height, im_bands, im_geotrans, im_proj, outpath_3)
            print('this is ok')
        year += 1
        print(year)
    print('------All is ok------')
    
