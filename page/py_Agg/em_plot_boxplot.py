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
def em_load_file(file, charset, firstLineTitle, delimiter, field_index_array, fieldNames, filter_index_array, filterFieldNames):
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
        for i in range(len(field_index_array)):
            col_index = field_index_array[i]
            if len(filter_index_array) == 0:
                label = fieldNames[i]
                if label in cols_data:
                    cols_data[label].append(r[col_index])
                else:
                    cols_data[label] = []
                    cols_data[label].append(r[col_index])
            else:
                for j in range(len(filter_index_array)):
                    label = fieldNames[i] + '|' + filterFieldNames[j] + ':' + r[filter_index_array[j]]
                    if label in cols_data:
                        cols_data[label].append(r[col_index])
                    else:
                        cols_data[label] = []
                        cols_data[label].append(r[col_index])

        line = fin.readline()
    fin.close()

    labels = []
    values = []
    for k, v in cols_data.items():
        labels.append(k)
        values.append(v)
    return labels, values


# 箱形图
def em_plot_boxplot(argv):
    if len(argv) != 9:
        return 'usage: em_plot_boxplot file charset firstLineTitle delimiter fieldIds fieldNames filterFieldIds filterFieldNames'

    file = argv[1]
    charset = argv[2]
    firstLineTitle = argv[3]
    delimiter = argv[4]
    fieldIds = argv[5].split(',')
    fieldNames = argv[6].split(',')
    filterFieldIds = argv[7].split(',')
    filterFieldNames = argv[8].split(',')

    if delimiter == '\\t':
        delimiter = '\t'

    field_index_array = []
    for i in fieldIds:
        field_index_array.append(int(i))

    filter_index_array = []
    for i in filterFieldIds:
        filter_index_array.append(int(i))

    ret = ''
    try:
        labels, data = em_load_file(file, charset, firstLineTitle, delimiter, field_index_array, fieldNames, filter_index_array, filterFieldNames)
        pyplot.boxplot(data, labels=labels)
        pyplot.grid(axis="y", ls=":", lw=1, color="gray", alpha=0.4)
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
    ret = em_plot_boxplot(sys.argv)
    print(ret)