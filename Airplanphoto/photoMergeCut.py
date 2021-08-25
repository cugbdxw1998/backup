# -*- coding:utf-8 -*-
"""
图片任意拼接，参数化形式代码
使用指南：
    1. 修改常量的数值，可以实现不同样子的图片拼接，例如拼接成5*20，或者100*200的大图，每张小图也可以控制大小
    2. 可以自定义函数让图片不仅仅是全部拼接成一张图，也可以自定义哪些图进行拼接。
"""
from PIL import Image
import os
import GoogleZXY2pt
import cordConvert


IMAGE_SIZE = 256  # 图片大小

# 图像拼接
def image_compose(z, x1, x2, y1, y2, inputpath, savetemppath):
    #clean
    if os.path.exists(savetemppath):
        os.remove(savetemppath)
    # 将x1, x2, y1, y2 之间的所有瓦片合并成一个瓦片，暂时保存在savetemppath中
    IMAGE_COLUMN = x2-x1+1
    IMAGE_ROW = y2-y1+1
    print('IMAGE_COLUMN = {},IMAGE_ROW = {}....'.format(IMAGE_COLUMN, IMAGE_ROW))
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))
    # 循环遍历，把每张图按顺序粘贴到对应位置上
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            fromfilepath = inputpath + str(z) + '/' + str(x) + '/' +str(y) + '.jpg'
            if os.path.exists(fromfilepath):
                from_image = Image.open(fromfilepath).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
                to_image.paste(from_image, ((x - x1) * IMAGE_SIZE, (y - y1) * IMAGE_SIZE))
                print('x={},  y={}, pixX = {}， pixY = {}....'.format(x,y,(x - x1) * IMAGE_SIZE,(y - y1) * IMAGE_SIZE))
    success = to_image.save(savetemppath)
    print('merge pictures success = {}....'.format(savetemppath))
    return success

def image_split(savetemppath,outputpath, z, x1, x2, y1, y2):
    if not os.path.exists(savetemppath):
        return
    fromimage = Image.open(savetemppath)
    width = fromimage.size[0]
    height = fromimage.size[1]

    IMAGE_COLUMN = x2 - x1 + 1
    IMAGE_ROW = y2 - y1 + 1
    cutwidth = IMAGE_SIZE * IMAGE_COLUMN
    cutheight = IMAGE_SIZE * IMAGE_ROW
    if cutwidth!=width or cutheight!=height:
        print('The size of this picture is not right for cut: {}'.format(savetemppath))
        return

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            output_fullname = outputpath + str(z)
            if not os.path.exists(output_fullname):
                os.mkdir(output_fullname)
            output_fullname += '/' + str(x)
            if not os.path.exists(output_fullname):
                os.mkdir(output_fullname)

            BOX_LEFT = (x-x1)*IMAGE_SIZE
            BOX_UP = (y - y1)*IMAGE_SIZE
            BOX_RIGHT = BOX_LEFT + IMAGE_SIZE
            BOX_DOWN = BOX_UP + IMAGE_SIZE

            # 从此图像返回一个矩形区域。 盒子是一个4元组定义左，上，右和下像素坐标。
            box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
            tofilepath = output_fullname + '/' + str(y) + '.jpg'
            to_image = fromimage.crop(box).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            success = to_image.save(tofilepath)
            print('this picture is cut into: {}'.format(tofilepath))
    print('finish')



def image_cut(savetemppath,pt00, pt01, xTo, yTo, outputpath, z, x1, x2, y1, y2):
    if not os.path.exists(savetemppath):
        return
    # 打开合并瓦片savetemppath，换算要切割的瓦片的像素范围，切割后，保存成目标瓦片（z, xTo, yTo）
    toimage = Image.open(savetemppath)
    pt1 = GoogleZXY2pt.GoogleXYZtoLonlat(z,x1,y1) # left_top
    pt2 = GoogleZXY2pt.GoogleXYZtoLonlat(z,x2+1,y2+1) # right_bottom

    BOX_LEFT = (pt00[0] - pt1[0])*(x2+1-x1)*256/(pt2[0]-pt1[0])
    BOX_UP = (pt1[1] - pt00[1])*(y2-y1+1)*256/(pt1[1] - pt2[1])
    BOX_RIGHT = (pt01[0] - pt1[0]) * (x2 + 1 - x1) * 256 / (pt2[0] - pt1[0])
    BOX_DOWN = (pt1[1] - pt01[1]) * (y2 + 1 - y1) * 256 / (pt1[1] - pt2[1])

    # 从此图像返回一个矩形区域。 盒子是一个4元组定义左，上，右和下像素坐标。
    box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
    print('BOX_LEFT={},  BOX_UP={}, BOX_RIGHT = {}， pixY = {}....'.format(BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN))
    # 进行ROI裁剪
    roi_area = toimage.crop(box).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    # 裁剪后每个图像全路径
    image_output_fullname = outputpath + str(z)
    if not os.path.exists(image_output_fullname):
        os.mkdir(image_output_fullname)
    image_output_fullname += '/' + str(xTo)
    if not os.path.exists(image_output_fullname):
        os.mkdir(image_output_fullname)
    # 保存处理后的图像
    image_output_fullname += '/' + str(yTo) + '.jpg'
    roi_area.save(image_output_fullname)
    print('{} : Done.'.format(image_output_fullname))

def get_y_range(srcDir):
    y1 = 0
    y2 = 0
    for filename in os.listdir(srcDir):
        path = srcDir + filename
        if (not os.path.isdir(path)) and (".jpg" in filename): #yrange
            ystr = filename[0: len(filename)-4]
            #print(' folders  y = {}......'.format(ystr))
            y = int(ystr)
            if y1 == 0 and y2 == 0:
                y1 = y2 = y
            else:
                y1 = min(y, y1)
                y2 = max(y, y2)
    return y1, y2

def get_xy_range(srcDir):
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    for filename in os.listdir(srcDir):
        path = srcDir + filename
        #print(' folders  x = {}......'.format(filename))
        if os.path.isdir(path) and filename.isdigit(): #xrange
            x = int(filename)
            if x2 == 0 and x1 == 0:
                x1 = x2 = x
            else:
                x1 = min(x, x1)
                x2 = max(x, x2)

            path += '/'
            yrange1, yrange2 = get_y_range(path)
            if y1 == 0 and y2 == 0:
                y1 = yrange1
                y2 = yrange2
            else:
                y1 = min(yrange1, y1)
                y2 = max(yrange2, y2)
    return x1, x2, y1, y2

def handleByZ(srcDir, destDir):
    for filename in os.listdir(srcDir):
        zpath = srcDir + filename
        if os.path.isdir(zpath) and filename.isdigit():  # Zrange
            print('Handling level z = {} ......'.format(filename))
            z = int(filename)
            zpath += '/'
            print('begin get x y range of {} ......'.format(zpath))
            x1, x2, y1, y2 = get_xy_range(zpath)
            xRange_WGS84 = [x1, x2]
            yRange_WGS84 = [y1, y2]
            print('xRange_WGS84: {}, YRange_WGS84: {}'.format(xRange_WGS84, yRange_WGS84))


            #WGS84 box
            ptLeftTop_WGS84 = GoogleZXY2pt.GoogleXYZtoLonlat(z, xRange_WGS84[0], yRange_WGS84[0])
            ptRightBottom_WGS84 = GoogleZXY2pt.GoogleXYZtoLonlat(z, xRange_WGS84[1]+1, yRange_WGS84[1]+1)
            print('ptLeftTop_WGS84: {}, ptRightBottom_WGS84: {}'.format(ptLeftTop_WGS84, ptRightBottom_WGS84))
            #Gcj box
            ptLeftTop_gcj02 = cordConvert.wgs84togcj02(ptLeftTop_WGS84[0],ptLeftTop_WGS84[1])
            ptRightBottom_gcj02 = cordConvert.wgs84togcj02(ptRightBottom_WGS84[0],ptRightBottom_WGS84[1])
            print('ptLeftTop_gcj02: {}, ptRightBottom_gcj02: {}'.format(ptLeftTop_gcj02, ptRightBottom_gcj02))
            #Gcj xy range
            x1y1_gcj02 = GoogleZXY2pt.GoogleLonLatToXYZ(z, ptLeftTop_gcj02[0],ptLeftTop_gcj02[1])
            x2y2_gcj02 = GoogleZXY2pt.GoogleLonLatToXYZ(z, ptRightBottom_gcj02[0], ptRightBottom_gcj02[1])
            xRange_gcj = [x1y1_gcj02[0]-1, x2y2_gcj02[0]+1]
            yRange_gcj = [x1y1_gcj02[1]-1, x2y2_gcj02[1]+1]
            print('xRange_gcj: {}, yRange_gcj: {}'.format(xRange_gcj, yRange_gcj))

            image_output_temp = destDir + str(z)
            if not os.path.exists(image_output_temp):
                os.mkdir(image_output_temp)

            image_output_temp += '/' + 'temp.jpg'

            # create new tiles
            for x_gcj in range(xRange_gcj[0], xRange_gcj[1]+1):
                for y_gcj in range(yRange_gcj[0], yRange_gcj[1]+1):
                    outfile = destDir +str(z) + '/' + str(x_gcj) + '/' +str(y_gcj) +'.jpg'
                    if os.path.exists(outfile):
                        print('finished x: {}, y: {}'.format(x_gcj, y_gcj))
                        continue
                    print('producing x: {}, y: {}'.format(x_gcj, y_gcj))
                    ptxy_gcj_lefttop = GoogleZXY2pt.GoogleXYZtoLonlat(z, x_gcj, y_gcj)
                    ptxy_gcj_rightbottom = GoogleZXY2pt.GoogleXYZtoLonlat(z, x_gcj + 1, y_gcj + 1)

                    ptxy_WGS84_lefttop = cordConvert.gcj02towgs84(ptxy_gcj_lefttop[0], ptxy_gcj_lefttop[1])
                    ptxy_WGS84_rightbottom = cordConvert.gcj02towgs84(ptxy_gcj_rightbottom[0], ptxy_gcj_rightbottom[1])

                    x1y1_WGS84 = GoogleZXY2pt.GoogleLonLatToXYZ(z, ptxy_WGS84_lefttop[0], ptxy_WGS84_lefttop[1])
                    x2y2_WGS84 = GoogleZXY2pt.GoogleLonLatToXYZ(z, ptxy_WGS84_rightbottom[0], ptxy_WGS84_rightbottom[1])
                    x1 = x1y1_WGS84[0]-1
                    x2 = x2y2_WGS84[0]+1
                    y1 = x1y1_WGS84[1]-1
                    y2 = x2y2_WGS84[1]+1

                    pt00 = ptxy_WGS84_lefttop
                    pt01 = ptxy_WGS84_rightbottom

                    print('test x1:{}, x2:{}, y1:{}, y2:{}, pt00:{}, pt01:{}'.format(x1, x2, y1, y2, pt00, pt01))

                    image_compose(z, x1, x2, y1, y2, srcDir, image_output_temp)
                    image_cut(image_output_temp, pt00, pt01, x_gcj, y_gcj, destDir, z, x1, x2, y1, y2)


if __name__ == "__main__":
      # 定义待批量裁剪的图像地址
    IMAGE_INPUT_PATH = input("input WGS84 images source forlder:") #FLAGS.input #'./src/'
    # 定义裁剪后的图像存放地址
    IMAGE_OUTPUT_PATH = input("input Gcj02 images output forlder:") #FLAGS.output #'./final/'
    IMAGE_INPUT_PATH += '/'
    IMAGE_OUTPUT_PATH += '/'
    handleByZ(IMAGE_INPUT_PATH, IMAGE_OUTPUT_PATH)

