import math
import changeGPS
import os
from shutil import copyfile

def changeYofGoogleTitle(z, x,y):
    #the y value of tile from pix4dmapper is wrong, need to convert from south to north
    nTo = math.pow(2,z)-1
    newY = nTo-y
    return int(newY)


def checkPath(srcDir, destDir):
    for filename in os.listdir(srcDir):
        path = srcDir + filename
        if os.path.isdir(path):
            path += '/'
            pathdest = destDir + filename
            changeGPS.check_folder([pathdest])
            pathdest += '/'
            checkPath(path, pathdest)
        else:
            checkFile(srcDir, destDir, filename)

def checkFile(image_root, save_root,filename):
    print('begin read file: {}'.format(image_root+filename))
    if (".png" not in filename and ".kml" not in filename):
        copyfile(image_root + filename, save_root + filename)
        return
    else:
        ylen = len(filename)
        y = filename[0:ylen-4]
        if(y.isdigit()):
            print('y: {} '.format(y))
            ny = int(y)
            npos = image_root.rfind('/',0,len(image_root)-1)
            x = image_root[npos+1:len(image_root)-1]
            print('x: {} '.format(x))
            nx = int(x)
            nposz = image_root.rfind('/',0, npos-1)
            z = image_root[nposz+1: npos]
            print('z: {} '.format(z))
            nz = int(z)
            nynew = changeYofGoogleTitle(nz,nx,ny)
            if(".png" not in filename):
                ynewfilename = str(nynew) +'.kml'
            else:
                ynewfilename = str(nynew) + '.png'
            print('Z: {} x: {} y: {} ynew: {}'.format(nz,nx,ny,nynew))
            copyfile(image_root + filename, save_root + ynewfilename)
        else:
            copyfile(image_root + filename, save_root + filename)
            return



if __name__ == "__main__":
    image_root = input("input images source forlder:")  # FLAGS.input #'./src/'
    save_root = input("input images output forlder:")  # FLAGS.output #'./final/'
    image_root += '/'
    save_root += '/'
    changeGPS.check_folder([image_root, save_root])
    checkPath(image_root, save_root)
    