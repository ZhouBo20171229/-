import zipfile
import os
import shutil

def RoiRename(Path):
    z = zipfile.ZipFile(Path, 'r')
    Dirpath = (os.path.splitext(Path))[0]

    if os.path.exists(Dirpath):
        shutil.rmtree(Dirpath)
        # os.remove(Dirpath)
    else:
        os.mkdir(Dirpath)
    z.extractall(Dirpath)
    Relation = {}
    i = 1
    # print(Dirpath)
    ################################################################
    for file in os.listdir(Dirpath):
        # print(file)
        if os.path.isfile(os.path.join(Dirpath,file)) == True:
            if file.find('.') > 0:
                Roiname = (os.path.splitext(file)[0])
                Relation[i] = [Roiname]
                Newname = str(i) + '.roi'
                os.rename(os.path.join(Dirpath, file), os.path.join(Dirpath, Newname))
                i = i + 1
            else:
                print(file.split('.')[-1])
    # if os.path.exists(Dirpath + '_Renamed.zip'):
    #     os.remove(Dirpath + '_Renamed.zip')
    # zip = zipfile.ZipFile(Dirpath + '_Renamed.zip', 'a', zipfile.ZIP_STORED)
    # for j in range(i-1):
    #     zip.write(Dirpath + '/' + str(j+1)+'.roi', str(j+1)+'.roi')
    # for file in os.listdir(Dirpath):
    #     # print(file)
    #     zip.write(Dirpath +'/'+ file, file)
    # zip.close()
    z.close()
    # shutil.rmtree(Dirpath)
    # os.remove(Path)
    return [Dirpath, Relation]



if __name__ == '__main__':
    RoiRename('C:\Result\JR1.zip')
    print(RoiRename('C:\Result\JR1.zip'))
    RoiRename('C:\Result\JR2.zip')