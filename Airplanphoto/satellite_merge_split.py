import photoMergeCut
import os

def getRange(srcDir):
    print('正在查询文件夹{}中的X range， y Range ...')
    for filename in os.listdir(srcDir):
        path = srcDir + filename
        if os.path.isdir(path) and filename.isdigit(): #zrange
            # print('您选择的等级Z={}...'.format(filename))
            path += '/'
            x1,x2,y1,y2 = photoMergeCut.get_xy_range(path)
            z = int(filename)
            print('您选择的等级Z={}, xyRange = {}, xRange = {}, yRange = {}...'.format(filename,[x1,x2,y1,y2], x2-x1+1, y2-y1+1))
            return z,x1,x2,y1,y2

if __name__ == "__main__":
    MERGE_CUT_MODE = input("请选择模式： 1-- 合并卫星图； 2--拆分卫星图: ")
    if '1' in MERGE_CUT_MODE:
        IMAGE_INPUT_PATH = input("输入原图所在的文件夹(Z-所在文件夹)： ")
        XY_RANGE = input("输入预计合并的x和y的范围：(z,x1,x2,y1,y2) ,仅输入0默认全部合并(0): ")
        IMAGE_OUTPUT_PATH = input("输出保存文件夹: ")
        IMAGE_INPUT_PATH += '/'
        IMAGE_OUTPUT_PATH += '/'
        z = 0
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        merge_limit = 0
        if not ',' in XY_RANGE:
            merge_limit = input("请输入合并的图片行和列的最大图片数（最大值255）: ")
            z,x1,x2,y1,y2 = getRange(IMAGE_INPUT_PATH)
        else:
            lstRange = XY_RANGE.split(',')
            z = int(lstRange[0])
            x1 = int(lstRange[1])
            x2 = int(lstRange[2])
            y1 = int(lstRange[3])
            y2 = int(lstRange[4])
            merge_limit = max(x2 - x1 + 1, y2 - y1 + 1)

        print(merge_limit)
        row = y2 - y1 + 1
        column = x2 - x1 + 1
        limitsize = int(merge_limit)
        x= x1
        while x < x2+1:
            xTo = x + limitsize
            if xTo > x2 - 1:
                xTo = x2
            y=y1
            while y< y2+1:
                yTo = y + limitsize
                if yTo >y2-1:
                    yTo = y2
                filesave = IMAGE_OUTPUT_PATH + '{}_{}_{}_{}_{}.jpg'.format(z, x, xTo, y, yTo)
                print('正在合并文件 = {}...'.format(filesave))
                photoMergeCut.image_compose(z, x, xTo, y, yTo, IMAGE_INPUT_PATH, filesave)
                y = yTo +1
            x = xTo +1
    else:
        IMAGE_INPUT_PATH = input("输入合并图所在文件夹：")
        IMAGE_OUTPUT_PATH = input("输出切分图保存文件夹:")
        IMAGE_INPUT_PATH += '/'
        IMAGE_OUTPUT_PATH += '/'
        for filename in os.listdir(IMAGE_INPUT_PATH):
            path = IMAGE_INPUT_PATH + filename
            if (not os.path.isdir(path)) and (".jpg" in filename):
                ystr = filename[0: len(filename) - 4]
                lstRange = ystr.split('_')
                z = int(lstRange[0])
                x1 = int(lstRange[1])
                x2 = int(lstRange[2])
                y1 = int(lstRange[3])
                y2 = int(lstRange[4])
                photoMergeCut.image_split(path,IMAGE_OUTPUT_PATH,z,x1,x2,y1,y2)