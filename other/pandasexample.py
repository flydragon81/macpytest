import pandas as pd
import time
from configure import config

start_time = time.time()
a = pd.read_fwf('/Volumes/Data/Python/macpytest/data/mirfa.X', header=None, chunksize=10000, colspecs=config.colspecsx)
sn = 0
tn = 0
for i in a:
    for indexs in i.index:
        # print(type(i))
        # print(i.loc[indexs].values[2])
        chans = i.loc[indexs].values[9] - i.loc[indexs].values[8] + 1

        # print(i.loc[indexs].values[0:-1])
        sn = sn + chans
    # print(sn)
    tn = tn + sn
print(tn)
# print(i[1], i[2], i[3])
end_time = time.time()
print(end_time - start_time)
