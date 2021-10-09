import os
import shutil
 
#想要移动文件所在的根目录
#rootdir="H:\\Graudate\\image\sebs_lang\\reMOD09A1\\reMOD09A1_B02"
#获取目录下文件名清单
#list=os.listdir(rootdir)
#print(list)
 
#移动图片到指定文件夹
#for j in range(20):
    #year= j + 2001
    #print(year)
#for i in range(0,len(list)):     #遍历目录下的所有文件夹
	#path=os.path.join(rootdir,list[i])    
	#print(path)
year =2001
while year < 2021:
	rootdir = os.path.join("H:\\001zone\\00张家口承德地区\\zc_evf\\image\\sebs_Interpolation\\evf",str(year))
	#rootdir = os.path.join("H:\\Graudate\\image\\sebs_0.005\\dem\\dem_wgs84","stacking")
	print(rootdir)
	list = os.listdir(rootdir)
	for i in range(0,len(list)):     #遍历目录下的所有文件夹
		dirpath=os.path.join(rootdir,list[i])    
		print(dirpath)
		despath = os.path.join("H:\\001zone\\00张家口承德地区\\cal_zc_evf","evf20")
		print(despath)
		shutil.copy(dirpath,despath)
	year +=1
		