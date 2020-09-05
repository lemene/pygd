import sys
import traceback

def pygd_detect(sys):
    '''检测存在哪些那种集群系统
'''
    try:

        pass
    except:
        traceback.print_exc()
        print("----------------")
        print(pygd_detect.__doc__)

if __name__ == '__main__':
    if len(sys.argv) > 1:
       locals()[sys.argv[1]](sys.argv[1:])
    else:
       for func in list(locals().keys()):
           if func.startswith("pygd_"):
               print("%s: %s" % (func, locals()[func].__doc__.split("\n")[0]))
