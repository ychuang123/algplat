from matplotlib import pyplot
from minepy import MINE
from io import BytesIO
from matplotlib.font_manager import FontProperties
import numpy as np
import matplotlib as mpl
import base64
import traceback
import sys

mpl.use('Agg')

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
mine = MINE()

# 加载数据
# firstLineTitle 为 Y|y，表示首行为标题
def em_load_file(file, charset, firstLineTitle, delimiter, col_index):
    col_data = []
    distinct_values = {}
    
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
        v = float(r[col_index])
        distinct_values[v] = 1
        col_data.append(v)

        line = fin.readline()
    fin.close()

    # 直方图箱子数量
    bins = len(distinct_values)
    while bins > 100:
        bins /= 2
    return col_data, bins


# 直方图 histogram
def em_plot_hist(argv):
    if len(argv) != 9:
        return 'usage: em_plot_hist file charset firstLineTitle delimiter col_index x_label y_label title'

    file = argv[1]
    charset = argv[2]
    firstLineTitle = argv[3]
    delimiter = argv[4]
    col_index = int(argv[5])
    x_label = argv[6]
    y_label = argv[7]
    title = argv[8]

    if delimiter == '\\t':
        delimiter = '\t'
	
    ret = ''
    try:
        data, bins = em_load_file(file, charset, firstLineTitle, delimiter, col_index)
        data = np.array(data)

        pyplot.hist(data, bins)
        pyplot.xlabel(x_label, fontproperties=font_set)
        pyplot.ylabel(y_label, fontproperties=font_set)
        pyplot.title(title, fontproperties=font_set)
        pyplot.show()

        sio = BytesIO()
        pyplot.savefig(sio, format='png')
        ret = base64.encodebytes(sio.getvalue()).decode()
        pyplot.close()

    except Exception as e:
        et, ev, tb = sys.exc_info()
        traceback.print_exception(et, ev, tb)

    return ret


if __name__ == "__main__":
    ret = em_plot_hist(sys.argv)
    print(ret)
