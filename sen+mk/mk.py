'''
Created on 2021年4月11日

@author: DXW
'''
#coding:utf-8
import numpy as np
import pymannkendall as mk
import os 
import rasterio as ras



def sen_mk_test(path1,outputPath):
    
    #image_path:影像的存储路径
    #outputPath:结果输出路径
    
    filepaths=[]
    for file in os.listdir(path1):
        filepath1=os.path.join(path1,file)
        filepaths.append(filepath1)
    
    #获取影像数量
    num_images=len(filepaths)
    #读取影像数据
    img1=ras.open(filepaths[0])
    #获取影像的投影，高度和宽度
    transform1=img1.transform
    height1=img1.height
    width1=img1.width 
    array1=img1.read()
    img1.close()
    
    #读取所有影像
    for path1 in filepaths[1:]:
        if path1[-4:]=='tiff':
            print(path1)
            img2=ras.open(path1)
            array2=img2.read()
            array1=np.vstack((array1,array2))
            img2.close()
        
    nums,width,height=array1.shape 
    #写影像
    def writeImage(image_save_path,height1,width1,para_array,bandDes,transform1):
        with ras.open(
               image_save_path,
               'w',
               driver='GTiff',
               height=height1,
               width=width1,
               count=1,
               dtype=para_array.dtype,
               crs='+proj=latlong',
               transform=transform1,
        ) as dst:
                   dst.write_band(1,para_array)
                   dst.set_band_description(1,bandDes)
        del dst
    
    #输出矩阵，无值区用-9999填充    
    slope_array=np.full([width,height],-9999.0000) 
    z_array=np.full([width,height],-9999.0000)
    Trend_array=np.full([width,height],-9999.0000) 
    Tau_array=np.full([width,height],-9999.0000)
    s_array=np.full([width,height],-9999.0000)
    p_array=np.full([width,height],-9999.0000)
    
    #只有有值的区域才进行mk检验
    c1=np.isnan(array1)
    sum_array1=np.sum(c1,axis=0)
    nan_positions=np.where(sum_array1==num_images)
    
    positions=np.where(sum_array1!=num_images) 
    
    
    #输出总像元数量
    print("all the pixel counts are {0}".format(len(positions[0])))
    #mk test
    for i in range(len(positions[0])):
        print(i)
        x=positions[0][i]
        y=positions[1][i]    
        mk_list1=array1[:,x,y]
        trend, h, p, z, Tau, s, var_s, slope, intercept  = mk.original_test(mk_list1)
        '''        
        trend: tells the trend (increasing, decreasing or no trend)
                h: True (if trend is present) or False (if trend is absence)
                p: p-value of the significance test
                z: normalized test statistics
                Tau: Kendall Tau
                s: Mann-Kendal's score
                var_s: Variance S
                slope: Theil-Sen estimator/slope
                intercept: intercept of Kendall-Theil Robust Line
        '''
        
        
        if trend=="decreasing":
            trend_value=-1
        elif trend=="increasing":
            trend_value=1
        else:
            trend_value=0
        slope_array[x,y]=slope#senslope
        s_array[x,y]=s
        z_array[x,y]=z
        Trend_array[x,y]=trend_value
        p_array[x,y]=p
        Tau_array[x,y]=Tau 
        
        
    all_array=[slope_array,Trend_array,p_array,s_array,Tau_array,z_array]   
    
    slope_save_path=os.path.join(result_path,"slope.tiff")
    Trend_save_path=os.path.join(result_path,"Trend.tiff")
    p_save_path=os.path.join(result_path,"p.tiff")
    s_save_path=os.path.join(result_path,"s.tiff")
    tau_save_path=os.path.join(result_path,"tau.tiff")
    z_save_path=os.path.join(result_path,"z.tiff")
    image_save_paths=[slope_save_path,Trend_save_path,p_save_path,s_save_path,tau_save_path,z_save_path]
    band_Des=['slope','trend','p_value','score','tau','z_value']
    for i in range(len(all_array)):
        writeImage(image_save_paths[i], height1, width1, all_array[i], band_Des[i],transform1)

#调用
if __name__ == '__main__':

    path1="H:\\001zone\\00张家口承德地区\\cal_zc_evf\\evf_year"  #目录里边需包含长时间序列的遥感影像
    result_path="H:\\001zone\\00张家口承德地区\\cal_zc_evf\\result"  #输出路径
    sen_mk_test(path1, result_path)
