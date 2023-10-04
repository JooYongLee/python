import argparse
# import mycallback
import a_dll_bind
import importlib
from pysome.pys import some_fun
parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
parser.add_argument('--c', '--count', default=10, help='set the default count')      # option that takes a value
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

args = parser.parse_args()

def main():
    # buf = mycallback.MyBufferf()
    print('counts', args.c)
    # print(buf)
    some_fun()
    pass
    a_dll_bind.mydll.myprint()
    # import mydll
    hiddens = importlib.import_module('pysome.hiddenmodule')
    print(hiddens)
    hiddens.showme()

    # mydll.

if __name__=='__main__':
    main()