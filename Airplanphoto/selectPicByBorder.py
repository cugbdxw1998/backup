import os
import json
from matplotlib.path import Path
import shutil
import GoogleZXY2pt as glconvt


def getZXYformpath(filepath):
    if os.path.isdir(filepath):
        print('This is a folder, not a file')
        return
    filepath.replace('\\','/')
    lst = filepath.split('/')
    print(lst)
    lenlst = len(lst)
    y = lst[lenlst-1]
    print(y)
    npos = y.find('.')
    y = y[0:npos]
    ny = int(y)
    x = lst[lenlst-2]
    print(x)
    nx = int(x)
    z = lst[lenlst-3]
    print(y)
    nz = int(z)
    return nz, nx, ny

def picFileSel(poly,filefolder,outFolder):
    for file in os.listdir(filefolder):
        filepath = filefolder + file
        outpath = outFolder + file
        if os.path.isdir(filepath):
            print("checking the folder {}------------".format(filepath))
            if not os.path.exists(outpath):
                os.mkdir(outpath)
            filepath +='/'
            outpath +='/'
            picFileSel(poly,filepath,outpath)
        else:
            Z,X,Y = getZXYformpath(filepath)
            print(Z,X,Y)
            result = glconvt.GoogleXYZtoLonlat(Z,X,Y)
            result1 = glconvt.GoogleXYZtoLonlat(Z,X+1,Y)
            result2 = glconvt.GoogleXYZtoLonlat(Z,X,Y+1)
            result3 = glconvt.GoogleXYZtoLonlat(Z,X+1,Y+1)
            if poly.contains_points([(result[0], result[1])]) or poly.contains_points([(result1[0], result1[1])]) or poly.contains_points([(result2[0], result2[1])]) or poly.contains_points([(result3[0], result3[1])]):
                shutil.copyfile(filepath, outpath)

def selectSatelliteByBorder(borderfile, picFolder,outFolder):
    if not os.path.exists(borderfile):
        print('{} border file is not exist!'.format(borderfile))
        return
    f = open(borderfile, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    #get cordinate
    features = a.get('features')
    feature = features[0]
    geometry = feature.get('geometry')
    coordinates = geometry.get('coordinates')
    coord = coordinates[0][0]
    poly = Path(coord)
    print(poly)
    #get picture point
    if not os.path.exists(picFolder):
        print('{} picture folder is not exist!'.format(picFolder))
        return
    picFileSel(poly,picFolder,outFolder)
    print('Done！')


if __name__ == "__main__":
    borderfile = input("input border json file:")
    picfolder = input("input satellite forlder:")
    outFolder = input("input output forlder:")
    picfolder += '/'
    outFolder += '/'
    selectSatelliteByBorder(borderfile, picfolder,outFolder)
    
       
    

   
    

