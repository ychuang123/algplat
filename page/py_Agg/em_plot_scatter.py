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


# 散点图
def em_plot_scatter(argv):
    if len(argv) != 10:
        return 'usage: em_plot_scatter file charset firstLineTitle delimiter x_index x_label y_indexs y_labels title'

    file = argv[1]
    charset = argv[2]
    firstLineTitle = argv[3]
    delimiter = argv[4]
    x_index = int(argv[5])
    x_label = argv[6]
    y_indexs = argv[7].split(',')
    y_labels = argv[8].split(',')
    title = argv[9]

    if delimiter == '\\t':
        delimiter = '\t'

    index_id_array = []
    index_id_array.append(x_index)
    for i in y_indexs:
        index_id_array.append(int(i))

    ret = ''
    try:
        cols_data = em_load_file(file, charset, firstLineTitle, delimiter, index_id_array)
        x_col = cols_data[x_index]
        for y_index in range(1, len(cols_data)):
            pyplot.scatter(x_col, cols_data[index_id_array[y_index]])

        #设置横坐标的文字说明
        pyplot.xlabel(x_label, fontproperties=font_set)
        #设置标题
        pyplot.title(title, fontproperties=font_set)
        #将纵坐标的文字说明添加到图例中
        pyplot.legend(y_labels, prop=font_set)
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
    ret = em_plot_scatter(sys.argv)
    print(ret)
