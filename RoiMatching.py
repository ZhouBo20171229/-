import os
import zipfile
import struct
import shutil
import numpy as np
from AreaComputing import *
from BatchRename import *
# import time
from math import *
from BatchZip import *



def DicBuild(Path):
    # print(Path)
    # print(os.path.isfile(Path))
    if ~(os.path.isfile(Path)) + 2:
        print('There is no .zip file!')
        return [{},'']
    else:
        if (os.path.splitext(Path))[1] != '.zip':
            print('Need a .zip file!')
            return [{}, '']
        else:
            [DirPath, Relation] = RoiRename(Path)
            Dic = {}
            # files = os.walk(DirPath)
            ######################################################
            for root, dirs, files in os.walk(DirPath):
                for f in files:
                    RoiPath = DirPath+'/'+ f
                    fo = open(RoiPath, "rb+")
                    #####################获取坐标数目##################
                    fo.seek(16,0)
                    bytes = fo.read(2)
                    s = struct.Struct('>H')
                    NumberOfCoordinates = s.unpack(bytes)
                    #####################获取所有边缘点坐标##################
                    ####################left and top###################
                    fo.seek(10, 0)
                    bytes = fo.read(2)
                    s = struct.Struct('>H')
                    Left= s.unpack(bytes)
                    #########################
                    fo.seek(8, 0)
                    bytes = fo.read(2)
                    s = struct.Struct('>H')
                    Top= s.unpack(bytes)
                    #######################X######################
                    fo.seek(64, 0)
                    XCoordinatesList = np.zeros((NumberOfCoordinates[0]))
                    for i in range(NumberOfCoordinates[0]):
                        bytes = fo.read(2)
                        s = struct.Struct('>H')
                        XCoordinates = s.unpack(bytes)
                        XCoordinatesList[i] = (XCoordinates[0])
                    #####################Y########################
                    fo.seek(64+2*NumberOfCoordinates[0], 0)
                    YCoordinatesList = np.zeros((NumberOfCoordinates[0]))
                    # print(XCoordinatesList)
                    for i in range(NumberOfCoordinates[0]):
                        bytes = fo.read(2)
                        s = struct.Struct('>H')
                        YCoordinates = s.unpack(bytes)
                        YCoordinatesList[i] = (YCoordinates[0])
                    SequenceOfRoi = os.path.splitext(f)
                    Xcenter = list(sum(XCoordinatesList) / NumberOfCoordinates[0] + Left)
                    Xcenter = Xcenter[0]
                    Ycenter = list(sum(YCoordinatesList) / NumberOfCoordinates[0] + Top)
                    Ycenter = Ycenter[0]
                    ###########################################################
                    CoordinatesList = list(np.zeros((NumberOfCoordinates[0])))
                    for i in range(NumberOfCoordinates[0]):
                        X = XCoordinatesList[i]
                        Y = YCoordinatesList[i]
                        CoordinatesList[i] = [X,Y]
                    Area = AreaComputing(CoordinatesList)
                    # print(NumberOfCoordinates[0])
                    # Dic[int(SequenceOfRoi[0])] = [int(Xcenter),int(Ycenter),int(Area),
                    #                                   int(NumberOfCoordinates[0]),
                    #                                   int(SequenceOfRoi[0])] # X坐标中心, Y坐标中心, 面积, 点数, 顺序
                    Dic[int(SequenceOfRoi[0])] = [int(Xcenter), int(Ycenter), int(Area),
                                                  int(NumberOfCoordinates[0]),
                                                  0]  # X坐标中心, Y坐标中心, 面积, 点数, 顺序
                    # print(int(NumberOfCoordinates[0]))
                    fo.close()
            ####################################################################################################################
            # z.close()
            # shutil.rmtree(DirPath)
            # os.remove(Path)
            return [Dic, DirPath]

def Match(Dic1, Dic2):
    if ((len(Dic1)) == 0)|((len(Dic2)) == 0):
        print('Error input!')
        return [{},{}]
    else:
        s = 0#用于计数找到的匹配ROI对数
        for key1 in range(len(Dic1)):#注意按照键遍历字典时的方法
            key1 = key1 + 1
            MinDistance = 10000
            key2Remember = 1
            for key2 in range(len(Dic2)):
                key2 = key2 + 1
                XCenter1 = Dic1[key1][0]
                YCenter1 = Dic1[key1][1]
                Area1 = Dic1[key1][2]
                NumberOfCoordinate1 = Dic1[key1][3]
                ######################################
                XCenter2 = Dic2[key2][0]
                YCenter2 = Dic2[key2][1]
                Area2 = Dic2[key2][2]
                NumberOfCoordinate2 = Dic2[key2][3]
                ######################################
                # Distance = sqrt(int(abs(XCenter1-XCenter2))^2 + int(abs(YCenter1-YCenter2))^2) + (1-(min(Area1, Area2))/(max(Area1, Area2)))
                # Distance = (1 - (min(XCenter1, XCenter2)) / (max(XCenter1, XCenter2))) + \
                #            (1 - (min(YCenter1, YCenter2)) / (max(YCenter1, YCenter2))) + \
                #            0.1*(1 - (min(Area1, Area2)) / (max(Area1, Area2))) + \
                #            0.1*abs(NumberOfCoordinate1 - NumberOfCoordinate2)
                # Distance = 5*(1 - (min(XCenter1, XCenter2)) / (max(XCenter1, XCenter2))) + \
                #            5*(1 - (min(YCenter1, YCenter2)) / (max(YCenter1, YCenter2))) + \
                #            (1 - (min(Area1, Area2)) / (max(Area1, Area2))) + \
                #            (1 - (min(NumberOfCoordinate1, NumberOfCoordinate2)) / (max(NumberOfCoordinate1, NumberOfCoordinate2)))
                Distance = abs(XCenter1- XCenter2) + abs(YCenter1- YCenter2) +\
                           abs(Area1- Area2) + abs(NumberOfCoordinate1- NumberOfCoordinate2)
                if Distance < MinDistance:
                    MinDistance = Distance
                    key2Remember = key2
            MinDistance = MinDistance
            # print(MinDistance)
            if MinDistance < 30:#阈值确定较为艰难 计算Distance时的归一化可能没有必要
                s = s + 1
                Dic1[key1][4] = s
                Dic2[key2Remember][4] = s
        ###########################################后续处理###################
        i = s
        # print(s)
        for key1 in range(len(Dic1)):
            key1 = key1 + 1
            if Dic1[key1][4] == 0:
                i = i+1
                Dic1[key1][4] = i
                # print(i)
        ######################################
        j = s
        for key2 in range(1,len(Dic2)+1):
            # key2 = key2 + 1
            if Dic2[key2][4] == 0:
                j = j+1
                Dic2[key2][4] = j
                # print(j)
        return [Dic1, Dic2]



def Rename(Dic,DirPath):#Relation暂不用 ##DirPath——文件夹路径
    if len(Dic) > 0:
        CurrentPath = (os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)))#获取当前工作路径
        ##########################################
        NewPath = DirPath + 'New'
        if os.path.exists(NewPath):
            for root, dirs, files in os.walk(NewPath):
                # print(files)
                for f in files:
                    os.remove(os.path.join(NewPath, f))
            # os.remove(NewPath)
        else:
            os.mkdir(NewPath)
        # a = 1
        for key in range(len(Dic)):
            # print(key)
            key = key + 1
            Oldname = str(key) + '.roi'
            Newname = str(Dic[key][4]) + '.roi'
            # shutil.copy(os.path.join(DirPath, Oldname), os.path.join(NewPath, Newname))
            # shutil.copy(os.path.join(DirPath, Oldname), NewPath)
            if Oldname != Newname:
                shutil.copy(os.path.join(DirPath, Oldname), os.path.join(CurrentPath, Oldname))
                shutil.move(os.path.join(CurrentPath, Oldname), os.path.join(NewPath, Newname))
            else:
                shutil.copy(os.path.join(DirPath, Oldname), os.path.join(NewPath, Newname))
            # print(os.path.join(DirPath, Oldname))
            # shutil.move(os.path.join(DirPath, Oldname), os.path.join(NewPath, Newname))
        # BatchZip(NewPath)
        ###############一顿操作 替换文件名#################3
        shutil.rmtree(DirPath)
        os.rename(NewPath, DirPath)
        BatchZip(DirPath)
        shutil.rmtree(DirPath)
    else:
        print('Error input!')


if __name__ == '__main__':
    # [Dirpath1, Relation1] = RoiRead('C:\Result\JR1.zip')#Path1为Renamed_Roi.zip的路径 下同
    # [Dirpath2, Relation2] = RoiRead('C:\Result\JR5.zip')

    [Dic1, DirPath1] = DicBuild('C:\Result\JR1.zip')
    [Dic2, DirPath2] = DicBuild('C:\Result\JR4.zip')

    # print((Match(Dic1, Dic2))[0])
    # print((Match(Dic1, Dic2))[1])

    Rename((Match(Dic1, Dic2))[0], DirPath1)
    Rename((Match(Dic1, Dic2))[1], DirPath2)

