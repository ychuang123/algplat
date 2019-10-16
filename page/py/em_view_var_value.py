import numpy as np
from sklearn.externals import joblib
import traceback
import sys

def em_view_var_value(argv):
    if len(argv) != 2:
        return 'usage: em_view_var_value file'

    file = argv[1]
	
    ret = ''
    try:
        v = joblib.load(file)
        ret = str(v)
    except Exception as e:
        et, ev, tb = sys.exc_info()
        traceback.print_exception(et, ev, tb)
    return ret

if __name__ == "__main__":
    ret = em_view_var_value(sys.argv)
    print(ret)
