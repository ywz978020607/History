def aa():
    cc = 123
    def bb():
        # global cc
        print("bb")
        print(cc)
    bb()


aa()