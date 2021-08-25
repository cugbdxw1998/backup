import gdal
from osgeo.gdalconst import *
import numpy as np
import os
import cordConvert as cvt
import copy
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLATED

class GeoTiffManager():
    def __init__(self, in_file):
        self.in_file = in_file  # Tiff或者ENVI文件
        self.dataset = gdal.Open(self.in_file)
        self.XSize = self.dataset.RasterXSize  # 网格的X轴像素数量
        self.YSize = self.dataset.RasterYSize  # 网格的Y轴像素数量
        self.bandCnt = self.dataset.RasterCount #波段数量
        self.GeoTransform = self.dataset.GetGeoTransform()  # 投影转换信息
        #geoTransform = self.dataset.GetTransform()
        self.ProjectionInfo = self.dataset.GetProjection()  # 投影信息
        self.Metadata = self.dataset.GetMetadata()
        self.bands_data = {}
        self.bands_datatype = {}
        for band in range(0, self.bandCnt):
            banddata = self.dataset.GetRasterBand(band+1)
            self.bands_data[band+1] = banddata.ReadAsArray()
            self.bands_datatype[band+1] = banddata.DataType



    def getHeightByBrand(self, x, y, bandnum =1):
        #dataset = gdal.Open(self.in_file)
        #banddata = self.dataset.GetRasterBand(bandnum)
        #data = banddata.ReadAsArray()
        data = self.bands_data[bandnum]
        #datatype = banddata.DataType
        dataheight = data[y][x]
        #print('DT_Type:{}, height :{}'.format(datatype,dataheight))
        return dataheight

    def getDataByBrand(self, bandnum =1):
        #dataset = gdal.Open(self.in_file)
        #banddata = self.dataset.GetRasterBand(bandnum)
        #data = banddata.ReadAsArray()
        #datatype = banddata.DataType
        data = self.bands_data[bandnum]
        return data

    def get_lon_lat(self,x,y):
        gtf = self.GeoTransform
        lon = gtf[0] + x * gtf[1] + y * gtf[2]
        lat = gtf[3] + x * gtf[4] + y * gtf[5]
        return lon, lat

    def getXYByLonLat(self,lon, lat):
        gtf = self.GeoTransform
        if gtf[2]==0.0 and gtf[4]==0.0:
            x = int((lon - gtf[0])/gtf[1])
            y = int((lat - gtf[3])/gtf[5])
        else:
            x = int(( gtf[5]*(lon-gtf[0]) - gtf[2]*(lat-gtf[3]) ) / (gtf[5]*gtf[1] - gtf[2]*gtf[4] ))
            y = int( (lon-gtf[0]-gtf[1]*x) / gtf[2] )
        print('lon:{}-lat:{} vs x:{}-y:{}'.format(lon,lat,x,y))
        return x, y


def getFileNamestr(lon, lat):
    ToLatlonstr = 'ASTGTM2_'
    if lat > 0:
        ToLatlonstr += 'N'
    else:
        ToLatlonstr += 'S'
    ToLatlonstr += str(int(lat))
    if lon > 0:
        ToLatlonstr += 'E'
    else:
        ToLatlonstr += 'W'
    ToLatlonstr += str(int(lon))
    ToLatlonstr += '_dem.tif'
    return ToLatlonstr

def open_around_tiff(inpath,filename):
    aroundRaster = {}
    # ASTGTM2_N36E120_dem.tif
    strs = filename.split('_')
    tifLonlat = strs[1]
    tifLon = 0
    tifLat = 0
    if 'N' in tifLonlat:
        tifLat = int(tifLonlat[1:3])
    else:
        tifLat = -int(tifLonlat[1:3])
    if 'E' in tifLonlat:
        tifLon = int(tifLonlat[4:])
    else:
        tifLon = -int(tifLonlat[4:])


    for lat in range(tifLat - 1, tifLat + 2):
        if lat <-90 or lat >90:
            break
        for lon in range(tifLon - 1, tifLon + 2):
            if lon < -180:
                lon += 360
            if lon > 180:
                lon -= 360

            ToLatlonstr = getFileNamestr(lon, lat)
            ToOpenFile = inpath + ToLatlonstr

            if os.path.exists(ToOpenFile):
                tiffopen = GeoTiffManager(ToOpenFile)
                aroundRaster[ToLatlonstr] = tiffopen
                print('已经将{}加入周边参考栅格图字典...'.format(ToLatlonstr))
    return aroundRaster



def shift_tiff_byGrid(inpath, filename,outpath):
    #Open and read file
    filepath = inpath + filename
    inRaster = GeoTiffManager(filepath)
    print('正在偏移卫星图：{}......'.format(filepath))
    #Open around files:周边栅格图字典
    aroundRaster = open_around_tiff(inpath, filename)
    #write file
    print('创建输出栅格图：......')
    driver = gdal.GetDriverByName('Gtiff')
    outFilepath = outpath + filename
    outRaster = driver.Create(outFilepath, inRaster.XSize, inRaster.YSize, inRaster.bandCnt, gdal.GDT_Int16 )  #gdal.GDT_Byte  ？
    outRaster.SetGeoTransform(inRaster.GeoTransform)  # 参数2,6为水平垂直分辨率，参数3,5表示图片是指北的
    outRaster.SetProjection(inRaster.ProjectionInfo)  # 将几何对象的数据导出为wkt格式
    outRaster.SetMetadata(inRaster.Metadata)
    # read brand data
    for brand in range(inRaster.bandCnt):
        data = inRaster.getDataByBrand(brand + 1)
        dataWrite = copy.deepcopy(data)
        outband = outRaster.GetRasterBand(brand + 1)
        #outband.SetDataType(data.DataType)

        for x in range(0,inRaster.XSize):
            for y in range(0,inRaster.YSize):
                height_Old = data[y][x]
                print('height of old x{}-y{}: {}'.format(x,y,height_Old))
                lon, lat = inRaster.get_lon_lat(x,y)
                lonshift, latshift = cvt.gcj02towgs84(lon,lat)
                xWrite,yWrite = inRaster.getXYByLonLat(lonshift,latshift)
                if xWrite not in range(0,inRaster.XSize) or yWrite not in range(0,inRaster.YSize):
                    print('out of range that : lon-{}, lat-{}, lonshift-{}, latshift-{}'.format(lon, lat, lonshift, latshift))
                    LonFromOpen = int(lonshift)
                    LatFromOpen = int(latshift)
                    FromLatlonstr = getFileNamestr(LonFromOpen, LatFromOpen)
                    if FromLatlonstr in aroundRaster:
                        RasterFrombands = aroundRaster[FromLatlonstr]
                        xWrite, yWrite = RasterFrombands.getXYByLonLat(lonshift, latshift)
                        Rasterbanddata = RasterFrombands.getDataByBrand(brand+1)
                        height_new = Rasterbanddata[yWrite][xWrite]
                        #write new data
                        dataWrite[y][x] = height_new
                        print('height of new x{}-y{}: {}'.format(x, y, height_new))
                else:
                    dataWrite[y][x] = data[yWrite][xWrite]
                    print('height of new x{}-y{}: {}'.format(x, y, dataWrite[y][x]))
        outband.WriteArray(dataWrite)
    outRaster.FlushCache()
    aroundRaster.clear()

def shift_tiff_forMerged(inpath, filename, outpath):
    filepath = inpath + filename
    inRaster = GeoTiffManager(filepath)
    print('正在偏移卫星图：{}......'.format(filepath))

    #write file
    print('创建输出栅格图：......')
    driver = gdal.GetDriverByName('Gtiff')
    outFilepath = outpath + filename
    outRaster = driver.Create(outFilepath, inRaster.XSize, inRaster.YSize, inRaster.bandCnt, gdal.GDT_Int16 )  #gdal.GDT_Byte  ？
    outRaster.SetGeoTransform(inRaster.GeoTransform)  # 参数2,6为水平垂直分辨率，参数3,5表示图片是指北的
    outRaster.SetProjection(inRaster.ProjectionInfo)  # 将几何对象的数据导出为wkt格式
    outRaster.SetMetadata(inRaster.Metadata)
    # read brand data
    for brand in range(inRaster.bandCnt):
        data = inRaster.getDataByBrand(brand + 1)
        dataWrite = copy.deepcopy(data)
        outband = outRaster.GetRasterBand(brand + 1)
        #outband.SetDataType(data.DataType)

        for x in range(0,inRaster.XSize):
            for y in range(0,inRaster.YSize):
                height_Old = data[y][x]
                print('height of old x{}-y{}: {}'.format(x,y,height_Old))
                lon, lat = inRaster.get_lon_lat(x,y)
                lonshift, latshift = cvt.gcj02towgs84(lon,lat)
                xWrite,yWrite = inRaster.getXYByLonLat(lonshift,latshift)
                if xWrite not in range(0,inRaster.XSize) or yWrite not in range(0,inRaster.YSize):
                    #dataWrite[y][x] = data[y][x]
                    print('out of range x{}-y{}: {}... height no Change'.format(x, y, dataWrite[y][x]))
                else:
                    dataWrite[y][x] = data[yWrite][xWrite]
                    print('height of new x{}-y{}: {}'.format(x, y, dataWrite[y][x]))
        outband.WriteArray(dataWrite)
    outRaster.FlushCache()

def shift_tiff_byGrid_Path(inpath, outpath):
    for filename in os.listdir(inpath):
        # ASTGTM2_N36E120_dem.tif
        if '_dem.tif' in filename:
            fileOutpath = outpath + filename
            if not os.path.exists(fileOutpath):
                shift_tiff_byGrid(inpath,filename, outpath)

    #with ThreadPoolExecutor(max_workers=10) as executor:
        #futures = []
        #for filename in os.listdir(inpath):
            ## ASTGTM2_N36E120_dem.tif
            #if '_dem.tif' in filename:
                #fileOutpath = outpath + filename
                #if not os.path.exists(fileOutpath):
                    #future =  executor.submit(shift_tiff_byGrid,inpath,filename, outpath)
                    #futures.append(future)
                    ##shift_tiff_byGrid(inpath,filename, outpath)
    #wait(futures, return_when = ALL_COMPLATED)
    print('全部偏移完毕！')

def shift_tiff_forMerged_Path(inpath, outpath):
    for filename in os.listdir(inpath):
        # ASTGTM2_N36E120_dem.tif
        if '_dem.tif' in filename:
            fileOutpath = outpath + filename
            if not os.path.exists(fileOutpath):
                shift_tiff_byGrid(inpath,filename, outpath)

    #with ThreadPoolExecutor(max_workers=10) as executor:
        #futures = []
        #for filename in os.listdir(inpath):
            # # ASTGTM2_N36E120_dem.tif
            #if '_dem.tif' in filename:
                #fileOutpath = outpath + filename
                #if not os.path.exists(fileOutpath):
                    #future =  executor.submit(shift_tiff_forMerged,inpath,filename, outpath)
                    #futures.append(future)
                    ##shift_tiff_byGrid(inpath,filename, outpath)
    #wait(futures, return_when = ALL_COMPLATED)
    print('全部偏移完毕！')


if __name__ == "__main__":
    IMAGE_INPUT_PATH = input("输入tiff原图所在文件夹（tif文件需要以_dem.tif结尾）：")
    IMAGE_OUTPUT_PATH = input("偏移后输出文件夹:")
    IMAGE_INPUT_PATH += '/'
    IMAGE_OUTPUT_PATH += '/'
    print('开始偏移卫星图.......')
    #shift_tiff_forMerged_Path(IMAGE_INPUT_PATH, IMAGE_OUTPUT_PATH)
    shift_tiff_byGrid_Path(IMAGE_INPUT_PATH, IMAGE_OUTPUT_PATH)
    print('结束偏移!')


    #data, geoTransform, proj = read_tiff('d:/a.tif')
    #array2raster("d:/b.tif", np.zeros[2400, 2400], geoTransform, proj)

    # 以下代码演示读取E:/data/dataset.tif的第一个通道的数据，并且获取经纬度信息
    #dir_path = r"C:\Users\qiaoshiyun\Downloads\ASTGTM2_N36E120"
    #filename = "ASTGTM2_N36E120_dem.tif"
    #file_path = os.path.join(dir_path, filename)
    #dataset = Dataset(file_path)


    #longitude, latitude = dataset.get_lon_lat()  # 获取经纬度信息

    #lon = 120.6264
    #lat = 36.1782
    #x, y = dataset.getXYByLonLat(lon, lat)
    #band = 1
    #dataheight = dataset.getDataByBrand(x, y, band)  # 获取第一个通道的数据
    #print(dataheight)







