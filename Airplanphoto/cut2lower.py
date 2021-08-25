import os
from PIL import Image

IMAGE_SIZE = 256
def cutpicintolower(fileYdir, outpath,z,x,y):
    if not os.path.exists(fileYdir):
        return
    toimage = Image.open(fileYdir)

    outDir = outpath
    #save folder of lower Z
    outDir += str(z+1)
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    outDirx1 = outDir + '/' + str(x * 2)
    if not os.path.exists(outDirx1):
        os.mkdir(outDirx1)
    outDirx1 += '/'
    #[0,0]
    outYFile = outDirx1 + str(y * 2) + '.jpg'
    box = (0,0,IMAGE_SIZE,IMAGE_SIZE)
    cut_area = toimage.crop(box).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    cut_area.save(outYFile)
    #[0,1]
    outYFile = outDirx1 + str(y * 2 +1) + '.jpg'
    box = (0, IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE *2)
    cut_area1 = toimage.crop(box).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    cut_area1.save(outYFile)

    outDirx2 = outDir + '/' + str(x * 2 + 1)
    if not os.path.exists(outDirx2):
        os.mkdir(outDirx2)
    outDirx2 += '/'
    #[1,0]
    outYFile = outDirx2 + str(y * 2) + '.jpg'
    box = (IMAGE_SIZE,0,IMAGE_SIZE *2,IMAGE_SIZE)
    cut_area2 = toimage.crop(box).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    cut_area2.save(outYFile)
    #[1,1]
    outYFile = outDirx2 + str(y * 2 +1) + '.jpg'
    box = (IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE*2, IMAGE_SIZE *2)
    cut_area3 = toimage.crop(box).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
    cut_area3.save(outYFile)
    print('{} into Z:{}, X:{}~{},Y:{}~{}: Done.'.format(fileYdir,z+1, x*2, x*2+1, y*2, y*2+1))

def cut2lower(srcDir, outDir):
    for filename in os.listdir(srcDir):
        zpath = srcDir + filename
        if os.path.isdir(zpath) and filename.isdigit():  # Zrange
            print('Handling level z = {} ......'.format(filename))
            z = int(filename)
            zpath += '/'

            for folderX in os.listdir(zpath):
                xpath = zpath + folderX
                if os.path.isdir(xpath) and folderX.isdigit():  # xrange
                    print('Handling level x = {} ......'.format(folderX))
                    x = int(folderX)
                    xpath += '/'
                    for fileY in os.listdir(xpath):
                        ypath = xpath + fileY
                        if not os.path.isdir(ypath) and (".jpg" in fileY) and "-a-" in fileY:
                            print('Handling file = {}:{} ......'.format(folderX,fileY))
                            idx = fileY.find("-a-")
                            ystr = fileY[0:idx]
                            y = int(ystr)
                            print('Begin to cut {}-{}-{}........'.format(z,x,y))
                            cutpicintolower(ypath,outDir,z,x,y)


if __name__ == "__main__":
    print('******此程序用于将上一级别的卫星图（利用Topaz扩大像素4倍数后的卫星图），切分到下一级别。******')
    IMAGE_INPUT_PATH = input("输入待切分卫星图文件夹，选择到Z值文件夹的上层路径:")
    IMAGE_OUTPUT_PATH = input("输入保存路径：")
    IMAGE_INPUT_PATH += '/'
    IMAGE_OUTPUT_PATH += '/'
    cut2lower(IMAGE_INPUT_PATH, IMAGE_OUTPUT_PATH)
    print('全部切分完毕！')