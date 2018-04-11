from RoiMatching import *


def Roimatching(RoiZipPath1, RoiZipPath2):
    # [Dic1, DirPath1] = DicBuild('C:\Result\JR1.zip')
    # [Dic2, DirPath2] = DicBuild('C:\Result\JR4.zip')
    [Dic1, DirPath1] = DicBuild(RoiZipPath1)
    [Dic2, DirPath2] = DicBuild(RoiZipPath2)
    Rename((Match(Dic1, Dic2))[0], DirPath1)
    Rename((Match(Dic1, Dic2))[1], DirPath2)


if __name__ == '__main__':
    # print(os.path.dirname(os.path.realpath(__file__)))
    CurrentProjectPath = os.path.dirname(os.path.realpath(__file__))
    RoiZipPath1 = os.path.join(CurrentProjectPath, 'test1.zip')
    RoiZipPath2 = os.path.join(CurrentProjectPath, 'test2.zip')
    Roimatching(RoiZipPath1, RoiZipPath2)#入参均为roi的.zip文件

