import os
import zipfile

def  BatchZip(DirPath):
    #######################################统计Roi数目######################################
    count = 0
    for root, dirs, files in os.walk(DirPath):  # 遍历统计
        for each in files:
            count += 1  # 统计文件夹下文件个数
    ##########################################################################
    if os.path.exists(DirPath + '_Matched.zip'):
        os.remove(DirPath + '_Matched.zip')
    zip = zipfile.ZipFile(DirPath + '_Matched.zip', 'a', zipfile.ZIP_STORED)
    for j in range(count):
        zip.write(DirPath + '/' + str(j + 1) + '.roi', str(j + 1) + '.roi')
    zip.close()


if __name__ == '__main__':
    BatchZip('C:\Result\JR1')