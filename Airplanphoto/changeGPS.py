# ecoding:utf-8
import datetime
from PIL import Image
import piexif
import csv
import os
import cordConvert
from shutil import copyfile


def imgExifPath(srcDir, destDir):
    for filename in os.listdir(srcDir):
        path = srcDir + filename
        if os.path.isdir(path):
            path += '/'
            pathdest = destDir + filename
            check_folder([pathdest])
            pathdest += '/'
            imgExifPath(path, pathdest)
        else:
            imgExif(path, destDir + filename)

def imgExif(image_root, save_root):
    print('begin read file: {}'.format(image_root))
    if (".JPG" not in image_root):
        copyfile(image_root,save_root)
        return
    # read and print exif information
    _dictRead = read_exif(image_root)
    lng = formatBack_latlng(_dictRead['GPS'][piexif.GPSIFD.GPSLongitude])
    lat = formatBack_latlng(_dictRead['GPS'][piexif.GPSIFD.GPSLatitude])
    lngref = _dictRead['GPS'][piexif.GPSIFD.GPSLongitudeRef]
    latref = _dictRead['GPS'][piexif.GPSIFD.GPSLatitudeRef]

    #wgs84 to gcj-02
    print('before transfer: lon:{}, lat:{}'.format(lng, lat))
    gcjLatLon = cordConvert.wgs84togcj02(lng,lat)
    print('after transfer: lon:{}, lat:{}'.format(gcjLatLon[0], gcjLatLon[1]))

    ## 将经纬度与相对航高转为exif可用的经纬度与行高
    ## exif需要的航高输入为(20000,2)格式，表示高度为20000/100米
    ## exif需要的经度与维度为((12, 1), (20,1), (41000, 1000))格式表示12度20分41秒
    lng_exif = format_latlng(gcjLatLon[0])
    lat_exif = format_latlng(gcjLatLon[1])
    alt_exif = _dictRead['GPS'][piexif.GPSIFD.GPSAltitude]
    _dictWrite = {"alt": alt_exif, "lng": lng_exif, "lat": lat_exif, "lng_ref": lngref, "lat_ref":latref}

    #modify the exif information
    read_modify_exif(image_root, save_root, _dictWrite)



def format_latlng(latlng):
    """经纬度十进制转为分秒"""
    degree = int(latlng)
    res_degree = latlng - degree
    minute = int(res_degree * 60)
    res_minute = res_degree * 60 - minute
    seconds = round(res_minute * 60.0, 3)
    return ((degree, 1), (minute, 1), (int(seconds * 1000), 1000))

def formatBack_latlng(latlng_dict):
    """经纬度十进制转为分秒"""
    degree = latlng_dict[0][0]
    minute = latlng_dict[1][0]
    seconds = latlng_dict[2][0]/latlng_dict[2][1]

    latlon = degree + (minute+seconds/60)/60
    return latlon


def read_modify_exif(image_path, save_path, _dict):
    """ 读取并且修改exif文件"""
    img = Image.open(image_path)  # 读图
    exif_dict = piexif.load(img.info['exif'])  # 提取exif信息
    exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = _dict['alt']  # 修改高度，GPSAltitude是内置变量，不可修改
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = _dict['lng']  # 修改经度
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = _dict['lat']  # 修改纬度
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = _dict['lng_ref']  # odm需要读取，一般为’W'
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = _dict['lat_ref']  # 一般为‘N'

    exif_bytes = piexif.dump(exif_dict)
    print('alt:{} lng:{} lat:{} lngref:{} latref:{}'.format(exif_dict['GPS'][piexif.GPSIFD.GPSAltitude],
                                        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude],
                                        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude],
                                        exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef],
                                        exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef]))
    img.save(save_path, "jpeg", exif=exif_bytes)  # 保存
    print('{} finished'.format(image_path))

def read_exif(image_path):
        img = Image.open(image_path)  # 读图
        _dict = piexif.load(img.info['exif'])  # 提取exif信息
        print('alt:{} lng:{} lat:{} lngref:{} latref:{}'.format(_dict['GPS'][piexif.GPSIFD.GPSAltitude],
                                            _dict['GPS'][piexif.GPSIFD.GPSLongitude],
                                            _dict['GPS'][piexif.GPSIFD.GPSLatitude],
                                            _dict['GPS'][piexif.GPSIFD.GPSLongitudeRef],
                                            _dict['GPS'][piexif.GPSIFD.GPSLatitudeRef]))
        return _dict


def check_folder(path_list):
    """输入为文件夹列表,文件夹不存在则创建"""
    for path in path_list:
        if not os.path.exists(path):
            os.mkdir(path)


if __name__ == "__main__":
    image_root = input("input images source forlder:") #FLAGS.input #'./src/'
    save_root = input("input images output forlder:") #FLAGS.output #'./final/'
    image_root += '/'
    save_root += '/'
    check_folder([image_root, save_root])
    imgExifPath(image_root, save_root)

    #(tf-gpu) D:\VideoSurv\Airplan photo>python changeGPS.py
    #input images source forlder:E:\test\testGPS
    #input images output forlder:E:\test\final