# coding=utf-8
import colorama
 
colorama.init(autoreset=True)
import os, random

all_files = os.popen('dir /s /b').read().split('\n')
mod = "\033[0;{};40m{}\033[0m"
colors = list(range(30, 37, 1))

def print_with_auto_color(line):
    random.shuffle(colors)
    for idx, word in enumerate(line.split(" ")):
        color = colors[idx % 3 % 7]
        # print(color)
        # print(word)
        print("\b{} ".format(mod.format(color, word)), end = ' ')


def print_all_files():
    for file in all_files:
        if not os.path.isfile(file) or file.strip().split(".")[-1] in ["png", "jpg"]:
            continue
        # print(file)
        with open(file, 'r', encoding="UTF-8") as fr:
            context = fr.readlines()
        for line in context:
            if line.isspace():
                continue
            print_with_auto_color(line)
        break

while 1:
    print_all_files()