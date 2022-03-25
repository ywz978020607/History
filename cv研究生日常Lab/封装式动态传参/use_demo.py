import sys
from dict_import import auto_import

arg_dict = {
    #--root-name
    "root_name": "Instereo2k" 
}
args = auto_import(arg_dict, sys.argv[1:])


print(args["root_name"])
