import photoMergeCut
import os
from PIL import Image


IMAGE_SIZE = 256
def merge2pic(inPic_1, inPic_2, outpic):
    if os.path.exists(outpic):
        os.remove(outpic)
    if os.path.exists(inPic_1) and os.path.exists(inPic_2):
        to_image = Image.new('RGBA', (IMAGE_SIZE, IMAGE_SIZE))
        from_image1 = Image.open(inPic_1).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
        from_image2 = Image.open(inPic_2).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
        to_image.paste(from_image2, (0, 0))

        r, g, b, a = from_image1.split()
        to_image.paste(from_image1, (0, 0), mask = a)
        success = to_image.save(outpic)
        print('merge pictures success = {}....'.format(outpic))

def mergepicByLevel(inPath1, inPath2, outpath):
    for zfld in os.listdir(inPath1):
        pathz = inPath1 + zfld
        if os.path.isdir(pathz) and zfld.isdigit():
            z = int(zfld)
            print('merge level Z = {}....'.format(zfld))
            
            pathz += '/'
            for xfld in os.listdir(pathz):
                pathx = pathz + xfld
                if os.path.isdir(pathx) and xfld.isdigit():
                    x = int(xfld)
                    print('merge level Z = {}, X = {}....'.format(zfld, xfld))

                    pathx += '/'
                    for yfld in os.listdir(pathx):
                        pathy = pathx + yfld
                        if not os.path.isdir(pathy) and (".png" in yfld):
                            ystr = yfld[0: len(yfld)-4]
                            y = int(ystr)
                            print('merge level Z = {}, X = {}, Y ={}....'.format(zfld, xfld, ystr))

                            inFindPath2 = inPath2 + zfld + '/' + xfld + '/' + ystr + '.jpg'
                            if os.path.exists(inFindPath2):
                                outdir = outpath + zfld
                                if not os.path.exists(outdir):
                                    os.mkdir(outdir)
                                outdir += '/' + xfld
                                if not os.path.exists(outdir):
                                    os.mkdir(outdir)
                                # 保存处理后的图像
                                outdir += '/' + ystr + '.png'
                                merge2pic(pathy, inFindPath2, outdir)

if __name__ == "__main__":
    # 定义自己拍摄的航拍图瓦片路径
    Airphoto_PATH = input("input Airplane photo path:")
    # 定义抓取后处理的卫星图瓦片路径
    Satellite_PATH = input("input Satellite photo path:")
    # 定义合并后图片的保存路径
    output_PATH = input("output path:")
    Airphoto_PATH += '/'
    Satellite_PATH += '/'
    output_PATH += '/'
    mergepicByLevel(Airphoto_PATH, Satellite_PATH, output_PATH)
    







