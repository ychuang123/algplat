from matplotlib import pyplot
from minepy import MINE
from io import BytesIO
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import numpy as np
import base64
import traceback
import sys

mpl.use('Agg') # 如果直接运行python，注释掉本行

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
mine = MINE()

# 画坐标曲线
def em_plot(x_data, x_label, y_data, y_label, title):
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    pyplot.plot(x_data, y_data)
    pyplot.xlabel(x_label, fontproperties=font_set)
    pyplot.ylabel(y_label, fontproperties=font_set)
    pyplot.title(title, fontproperties=font_set)
    pyplot.show()

# 加载数据
# firstLineTitle 为 Y|y，表示首行为标题
# x_index 为-1时，横坐标使用行号
def em_load_file(file, charset, firstLineTitle, delimiter, x_index, y_index):
    x_data = []
    y_data = []

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
        if x_index >= 0:
            x_data.append(r[x_index])
        else:
            x_data.append(rowNo)
        y_data.append(float(r[y_index]))

        line = fin.readline()
    fin.close()
    return x_data, y_data

def em_plot_curve(argv):
    if len(argv) != 10:
        return 'usage: em_plot_curve file charset firstLineTitle delimiter x_index x_label y_index y_label title'

    file = argv[1]
    charset = argv[2]
    firstLineTitle = argv[3]
    delimiter = argv[4]
    x_index = int(argv[5])
    x_label = argv[6]
    y_index = int(argv[7])
    y_label = argv[8]
    title = argv[9]

    if delimiter == '\\t':
        delimiter = '\t'

    ret = ''
    try:
        x_data, y_data = em_load_file(file, charset, firstLineTitle, delimiter, x_index, y_index)
        em_plot(x_data, x_label, y_data, y_label, title)

        sio = BytesIO()
        pyplot.savefig(sio, format='png')
        ret = base64.encodebytes(sio.getvalue()).decode()
        pyplot.close()

    except Exception as e:
        et, ev, tb = sys.exc_info()
        traceback.print_exception(et, ev, tb)
    return ret


if __name__ == "__main__":
    ret = em_plot_curve(sys.argv)
    print(ret)

