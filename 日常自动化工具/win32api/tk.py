from tkinter import *


def main():
    root = Tk()
    b = Button(root, text='退出', command=root.quit)
    b.pack()
    mainloop()


if __name__ == '__main__':
    main()
    print('123')