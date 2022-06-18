#测试argparse 参数解析器的使用


import argparse

parser = argparse.ArgumentParser(prog="demo",description="A demo program",epilog="the end of usage")
parser.print_help()

parser.add_argument('-hf', '--height', type=int, help="HEIGHT of frame")  #第一个是命令行输入的参数，第二个是后续脚本调用的参数，1->2
parser.add_argument('-gpu', '--gpu', type=str, help="GPU") #1，2参数名可以一样，但横线数1，2个不能变

args = parser.parse_args() #从命令行获取


HEIGHT = args.height

print(HEIGHT)


# input 
# 输入 python arg.py -h  #显示帮助信息
# 输入 python arg.py -hf 20 或者 python arg.py --height 20 都能输入参数