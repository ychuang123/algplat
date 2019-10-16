from matplotlib import pyplot
from minepy import MINE
from io import BytesIO
from matplotlib.font_manager import FontProperties
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
    counter = {}

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
        v = r[col_index]
        if v in counter:
            counter[v] = counter[v] + 1
        else:
            counter[v] = 1

        line = fin.readline()
    fin.close()

    labels = []
    values = []
    for k, v in counter.items():
        labels.append(k)
        values.append(v)
    return labels, values

# 柱状图
def em_plot_bar(argv):
    if len(argv) != 9:
        return 'usage: em_plot_bar file charset firstLineTitle delimiter col_index x_label y_label title'

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
        labels, values = em_load_file(file, charset, firstLineTitle, delimiter, col_index)
        x_coordinate = range(len(labels))

        #第一个参数为柱的横坐标
        #第二个参数为柱的高度
        #参数align为柱的对齐方式，以第一个参数为参考标准
        pyplot.bar(x_coordinate, values, align='center')

        #设置柱的文字说明
        #第一个参数为文字说明的横坐标
        #第二个参数为文字说明的内容
        pyplot.xticks(x_coordinate, labels)

        #设置横坐标的文字说明
        pyplot.xlabel(x_label, fontproperties=font_set)
        #设置纵坐标的文字说明
        pyplot.ylabel(y_label, fontproperties=font_set)
        #设置标题
        pyplot.title(title, fontproperties=font_set)
        #绘图
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
    ret = em_plot_bar(sys.argv)
    print(ret)
