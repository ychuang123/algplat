from minepy import MINE
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import math
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


# 建立类型特征的类型值词典
def my_build_label_dict(v):
    dict = {}
    index = 0
    for i in v:
        if i not in dict:
            dict[i] = index
            index = index + 1
    return dict

# 生成类型特征的观察系列
def my_gen_label_feature_observe_list(x, y, x_label_dict, y_label_dict, observe_list, x_count, y_count, gen_x_count):
    for i in range(len(x)):
        x_index = x_label_dict[x[i]]
        y_index = y_label_dict[y[i]]
        observe_list[x_index][y_index] += 1.0
        if gen_x_count:
            x_count[x_index] += 1.0
        y_count[y_index] += 1.0

# 计算类型特征间的卡方检验
# https://baike.baidu.com/item/%E7%9A%AE%E5%B0%94%E6%A3%AE%E5%8D%A1%E6%96%B9%E6%A3%80%E9%AA%8C/22660784?fr=aladdin
def my_gen_label_feature_chisquare(x_dict_len, y_dict_len, observe_list, x_count, y_count, total_count):
    # 计算期望，生成卡方值
    chi2 = 0
    for i in range(x_dict_len):
        for j in range(y_dict_len):

            if x_count[i] == 0 or y_count[j] == 0:
                continue

            observe = observe_list[i][j]
            expect = x_count[i] * y_count[j] / total_count
            dif = observe - expect
            chi2 += dif * dif / expect

    return chi2

# 计算类型特征间的信息增益-互信息
# https://blog.csdn.net/gdanskamir/article/details/54913233
def my_gen_label_feature_mi(x_dict_len, y_dict_len, observe_list, x_count, y_count, total_count):
    mi = 0
    for i in range(x_dict_len):
        for j in range(y_dict_len):

            if x_count[i] == 0 or y_count[j] == 0:
                continue

            v = observe_list[i][j]/total_count*math.log(observe_list[i][j]*total_count/(x_count[i]*y_count[j]))/math.log(2);
            mi += v

    return mi

# 计算类型特征的相关系数
def em_relative_type_data(argv):
    if len(argv) != 8:
        return 'usage: em_relative_type_data file charset firstLineTitle delimiter x_index y_indexs names'

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
    x_label_dict = my_build_label_dict(x)
    x_dict_len = len(x_label_dict)
    x_count = [0] * x_dict_len
    total_count = len(x)

    ret = ''
    for y_index in range(1, len(cols_data)):
        v = cols_data[index_id_array[y_index]]
        y_label_dict = my_build_label_dict(v)
        y_dict_len = len(y_label_dict)

        observe_list = [([0] * y_dict_len) for i in range(x_dict_len)]
        y_count = [0] * y_dict_len

        my_gen_label_feature_observe_list(x, v, x_label_dict, y_label_dict, observe_list, x_count, y_count, i > 0)

        for name in names:
            if ret != '':
                ret += ','

            try:
                if name == '卡方检验':
                    ret += str(my_gen_label_feature_chisquare(x_dict_len, y_dict_len, observe_list, x_count, y_count, total_count))
                elif name == '信息增益-互信息':
                    ret += str(my_gen_label_feature_mi(x_dict_len, y_dict_len, observe_list, x_count, y_count, total_count))
                else:
                    ret += 'invalid'
            except Exception as e:
                ret += 'fail'
                et, ev, tb = sys.exc_info()
                traceback.print_exception(et, ev, tb)
    return ret

if __name__ == "__main__":
    ret = em_relative_type_data(sys.argv)
    print(ret)
