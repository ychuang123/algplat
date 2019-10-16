from matplotlib import pyplot
from minepy import MINE
from io import BytesIO
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import numpy as np
import base64
import traceback
import sys
from statsmodels.tsa.seasonal import seasonal_decompose

mpl.use('Agg') # 如果直接运行python，注释掉本行

font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
mine = MINE()

# https://www.jianshu.com/p/09e5218f58b4
# 将时间序列进行周期性分解
def em_decomposition_plot(target_data, freq):
    target_data = np.array(target_data)
    decomposition = seasonal_decompose(target_data, freq=freq, two_sided=False)

    #trend = decomposition.trend
    #seasonal = decomposition.seasonal
    #residual = decomposition.resid

    decomposition.plot()
    pyplot.show()

# 加载数据
# firstLineTitle 为 Y|y，表示首行为标题
def em_load_file(file, charset, firstLineTitle, delimiter, target_col):
    target_data = []

    fin = open(file, encoding=charset)
    line = fin.readline()
    lineNo = 0
    while line:
        line = line.strip()
        lineNo += 1
        if lineNo == 1 and (firstLineTitle == 'Y' or firstLineTitle == 'y'):
            line = fin.readline()
            continue

        r = line.split(delimiter)
        target_data.append(float(r[target_col]))

        line = fin.readline()
    fin.close()
    return target_data

def em_plot_timeseries(argv):
    if len(argv) != 7:
        return 'usage: em_plot_timeseries file charset firstLineTitle delimiter target_col freq'

    file = argv[1]
    charset = argv[2]
    firstLineTitle = argv[3]
    delimiter = argv[4]
    target_col = int(argv[5])
    freq = int(argv[6])

    if delimiter == '\\t':
        delimiter = '\t'

    ret = ''
    try:
        target_data = em_load_file(file, charset, firstLineTitle, delimiter, target_col)
        em_decomposition_plot(target_data, freq)

        sio = BytesIO()
        pyplot.savefig(sio, format='png')
        ret = base64.encodebytes(sio.getvalue()).decode()
        pyplot.close()

    except Exception as e:
        et, ev, tb = sys.exc_info()
        traceback.print_exception(et, ev, tb)
    return ret

if __name__ == "__main__":
    ret = em_plot_timeseries(sys.argv)
    print(ret)
