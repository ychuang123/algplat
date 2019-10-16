from matplotlib import pyplot
from minepy import MINE
from io import BytesIO
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import numpy as np
import base64
import traceback
import sys

mpl.use('Agg')  # 如果直接运行python，注释掉本行

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
mine = MINE()


# 画坐标曲线
def em_plot(data):
    pyplot.figure(figsize=(10, 5))
    for evalute_name, evalute_values in data.items():
        evalute_index = np.array(range(1, len(evalute_values) + 1))
        evalute_values = np.array(evalute_values)
        pyplot.plot(evalute_index, evalute_values, label=evalute_name)
    pyplot.legend(prop=font_set)
    pyplot.xlabel('迭代次数', fontproperties=font_set)
    pyplot.ylabel('评估值', fontproperties=font_set)
    pyplot.title('评估指标变化曲线', fontproperties=font_set)
    pyplot.show()


# 加载评估指标结果数据
# 每行格式：评估指标名=评估值
def em_load_file(file, charset):
    data = {}

    fin = open(file, encoding=charset)
    line = fin.readline()
    while line:
        line = line.strip()
        r = line.split('=')
        n = r[0]
        v = float(r[1])
        if n not in data:
            data[n] = []
        data[n].append(v)
        line = fin.readline()
    fin.close()
    return data


def em_plot_curve_evaluate(argv):
    if len(argv) != 3:
        return 'usage: em_plot_curve_evaluate file charset'

    file = argv[1]
    charset = argv[2]
    ret = ''
    try:
        data = em_load_file(file, charset)
        em_plot(data)

        sio = BytesIO()
        pyplot.savefig(sio, format='png')
        ret = base64.encodebytes(sio.getvalue()).decode()
        pyplot.close()

    except Exception as e:
        et, ev, tb = sys.exc_info()
        traceback.print_exception(et, ev, tb)
    return ret


if __name__ == "__main__":
    ret = em_plot_curve_evaluate(sys.argv)
    print(ret)

