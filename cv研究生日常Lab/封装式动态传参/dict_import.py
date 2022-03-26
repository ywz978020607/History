# 一键自动引入动态参数，有别于手动修改.conf或是修改parser/sys.argv
import argparse


def auto_import(arg_dict={}, argv_str=""):
    arg_dict = arg_dict or {
        "database_name": "aftercut512",
        "cuda_id": "0",
    }
    parser = argparse.ArgumentParser()
    for key in arg_dict:
        parser.add_argument('--'+key.replace("_","-"), type=type(arg_dict[key]), default=arg_dict[key])
        parser.add_argument('--'+key, type=type(arg_dict[key]), default=arg_dict[key])
    args = parser.parse_args(argv_str)
    return vars(args)
