from minepy import MINE
from scipy.stats import pearsonr
from scipy import stats
from matplotlib.font_manager import FontProperties
from scipy.spatial.distance import pdist, squareform
import numpy as np
import matplotlib as mpl
import traceback
import sys

mpl.use('Agg')

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
mine = MINE()

# 加载数据
# firstLineTitle 为 Y|y，表示首行为标题
def em_load_file(file, charset, firstLineTitle, delimiter, col_index_array):
    cols_data = {}

    fin = open(file, encoding=charset)
    line = fin.readline()
    lineNo = 0
    rowNo = 0
    while line:
        line = line.strip()
        lineNo += 1
        if lineNo == 1 and (firstLineTitle == 'Y' or firstLineTitle == 'y'):
            line = fin.readline()
            continue

        rowNo += 1
        r = line.split(delimiter)
        for col_index in col_index_array:
            if col_index in cols_data:
                cols_data[col_index].append(r[col_index])
            else:
                cols_data[col_index] = []
                cols_data[col_index].append(r[col_index])

        line = fin.readline()
    fin.close()

    return cols_data

# 距离相关系数
# https://majing.io/posts/10000014601150
# https://blog.csdn.net/jiaoaodechunlv/article/details/80655592
def distcorr(X, Y):
    X = np.atleast_1d(X)
    Y = np.atleast_1d(Y)
    if np.prod(X.shape) == len(X):
        X = X[:, None]
    if np.prod(Y.shape) == len(Y):
        Y = Y[:, None]
    X = np.atleast_2d(X)
    Y = np.atleast_2d(Y)
    n = X.shape[0]
    if Y.shape[0] != X.shape[0]:
        raise ValueError('Number of samples must match')
    a = squareform(pdist(X))
    b = squareform(pdist(Y))
    A = a - a.mean(axis=0)[None, :] - a.mean(axis=1)[:, None] + a.mean()
    B = b - b.mean(axis=0)[None, :] - b.mean(axis=1)[:, None] + b.mean()
    
    dcov2_xy = (A * B).sum()/float(n * n)
    dcov2_xx = (A * A).sum()/float(n * n)
    dcov2_yy = (B * B).sum()/float(n * n)
    dcor = np.sqrt(dcov2_xy)/np.sqrt(np.sqrt(dcov2_xx) * np.sqrt(dcov2_yy))
    return dcor

# 计算数值特征的相关系数
def em_relative_num_data(argv):
    if len(argv) != 8:
        return 'usage: em_relative_num_data file charset firstLineTitle delimiter x_index y_indexs names'

    file = argv[1]
    charset = argv[2]
    firstLineTitle = argv[3]
    delimiter = argv[4]
    x_index = int(argv[5])
    y_indexs = argv[6].split(',')
    names = argv[7].split(',')

    if delimiter == '\\t':
        delimiter = '\t'

    index_id_array = []
    index_id_array.append(x_index)
    for i in y_indexs:
        index_id_array.append(int(i))

    cols_data = em_load_file(file, charset, firstLineTitle, delimiter, index_id_array)
    x = cols_data[x_index]

    ret = ''
    for y_index in range(1, len(cols_data)):
        v = cols_data[index_id_array[y_index]]
        for name in names:
            if ret != '':
                ret += ','

            try:
                if name == 'Pearson皮尔森相关系数':
                    ret += str(pearsonr(x, v)[0])
                elif name == 'MIC最大信息系数':
                    mine.compute_score(x, v)
                    ret += str(mine.mic())
                elif name == 'DC距离相关系数':
                    ret += str(distcorr(x, v))
                elif name == '卡方检验':
                    ret += str(stats.chisquare(x, f_exp=v).statistic)
                else:
                    ret += 'invalid'
            except Exception as e:
                ret += 'fail'
                et, ev, tb = sys.exc_info()
                traceback.print_exception(et, ev, tb)
    return ret

if __name__ == "__main__":
    ret = em_relative_num_data(sys.argv)
    print(ret)
