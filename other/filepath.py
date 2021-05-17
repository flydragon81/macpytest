import os

# 读取文件后缀
'''
file_path = "D:/test/testfile.py"
filepath, tempfilename = os.path.split(file_path)
filename, extension = os.path.splitext(file_path)
print(filepath, tempfilename, filename, extension)
print(os.path.splitext(file_path)[0] + '_output' + os.path.splitext(file_path)[1])
'''
obslist = []
valids = []
sn = [0, 0, 0, 0, 0, 0]


# 遍历文件夹
def walkFile(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            #print(os.path.splitext(f)[1])
            #            print(os.path.join(root, f))
            #            print(f)
            na = f.split("_")
            #            for te in na:
            #                print(te)
            if ('ObserverReport' in na) and os.path.splitext(f)[1] == '.csv':
                obsfile = os.path.join(root, f)
                obslist.append(obsfile)
        for fl in obslist:
            with open(fl) as fr:
                for line in fr:
                    line = line.replace('"', '')
                    obstxt = line.split(',')
                    if obstxt[0] == 'Scan Type Id':
                        print(obstxt)
                        sn[0] = obstxt.index('File #')
                        sn[1] = obstxt.index('Line Name')
                        sn[2] = obstxt.index('Point Number')
                        sn[3] = obstxt.index('Point Index')
                        sn[4] = obstxt.index('Comment')
                        sn[5] = obstxt.index('Jday')
                        #print(sn)
                    elif obstxt[sn[4]] == 'N/A':
                        valids.append([int(obstxt[sn[0]]), obstxt[sn[1]], obstxt[sn[2]], obstxt[sn[3]], obstxt[sn[5]]])
                        #print(obstxt[sn[0]], obstxt[sn[1]], obstxt[sn[2]], obstxt[sn[3]], obstxt[sn[4]], obstxt[sn[5]])
                    #else:
                        #print(obstxt[sn[4]])
        for s in valids:
            print(s)

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))


def main():
    walkFile("/Volumes/Data/Python/macpytest/data/sps")


if __name__ == '__main__':
    main()
