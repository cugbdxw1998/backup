from PIL import Image
import os
import math
import shutil
#shutil.copyfile(oldfile, newfile)  # 复制
#shutil.move(oldfile, newfile)  # 移动


def isBlack(pix):
    return sum(pix) < 25
def isWhite(pix):
    return sum(pix) > 255*3-30

def hCheck(img, y, width, step):
    ncntBlack = 0
    ncntWhite = 0
    for x in range(0, width):
        if isBlack(img.getpixel((x, y))):
            if ncntWhite==0:
                ncntBlack += 1
            else:
                ncntWhite =0
                ncntBlack = 1
        if isWhite(img.getpixel((x, y))):
            if ncntBlack==0:
                ncntWhite += 1
            else:
                ncntBlack = 0
                ncntWhite = 1
        if ncntBlack>width/step/2 or ncntWhite>width/step/2:
            return True
        x += step
    return False

def vCheck(img, x, height, step):
    ncntBlack = 0
    ncntWhite = 0
    for y in range(0, height):
        if isBlack(img.getpixel((x, y))):
            if ncntWhite == 0:
                ncntBlack += 1
            else:
                ncntWhite = 0
                ncntBlack = 1
        if isWhite(img.getpixel((x, y))):
            if ncntBlack == 0:
                ncntWhite += 1
            else:
                ncntBlack = 0
                ncntWhite = 1
        if ncntBlack > height / step / 2 or ncntWhite > height / step / 2:
            return True
        y += step
    return False

def isNousePhoto(checkwidth,imgPath):
    img = Image.open(imgPath)
    width = img.size[0]
    height = img.size[1]
    ncheckwidth = int(checkwidth)
    nstepx = 0
    for x in range(0,ncheckwidth*2):
        if vCheck(img,x,height,1):
            nstepx += 1
        if nstepx>ncheckwidth-1:
            print('delete for vCheck is true: {}'.format(imgPath))
            return True
    nstepx = 0
    for x in range(0,ncheckwidth*2):
        if vCheck(img,width-1-x,height,1):
            nstepx += 1
        if nstepx>ncheckwidth-1:
            print('delete for vCheck is true: {}'.format(imgPath))
            return True

    nstepy = 0
    for y in range(0,ncheckwidth*2):
        if hCheck(img,y,width,1):
            nstepy += 1
        if nstepy>ncheckwidth-1:
            print('delete for hCheck is true: {}'.format(imgPath))
            return True
    nstepy = 0
    for y in range(0, ncheckwidth*2):
        if hCheck(img, height-1-y, width, 1):
            nstepy += 1
        if nstepy > ncheckwidth - 1:
            print('delete for hCheck is true: {}'.format(imgPath))
            return True
    return False

def checkNousePhotoByFolder(srcDir,checkwidth,destDir):
    delCnt = 0
    for filename in os.listdir(srcDir):
        path = srcDir + filename
        if os.path.isdir(path) and filename.isdigit(): #Zrange or Xrange
            pathout = destDir + filename
            if not os.path.exists(pathout):
                os.mkdir(pathout)
            path += '/'
            pathout += '/'
            checkNousePhotoByFolder(path,checkwidth,pathout)
        else:
            if (".jpg" in filename) and isNousePhoto(checkwidth, path):
                #os.remove(path)
                shutil.move(path, destDir+filename)
                delCnt += 1
    print('delete {} pictures'.format(delCnt))
    return delCnt

if __name__ == "__main__":
    # 定义的图像地址
    IMAGE_INPUT_PATH = input("input images source Folder:")
    # 定义裁剪后的图像存放地址
    IMAGE_CHECK_WIDTH = input("input check width:")
    IMAGE_OUTPUT_PATH = input("OUTPUT Folder:")
    if not IMAGE_CHECK_WIDTH.isdigit():
        print('the check width is not a number: {}'.format(IMAGE_CHECK_WIDTH))
    else:
        IMAGE_INPUT_PATH += '/'
        IMAGE_OUTPUT_PATH += '/'
        checkNousePhotoByFolder(IMAGE_INPUT_PATH, IMAGE_CHECK_WIDTH, IMAGE_OUTPUT_PATH)