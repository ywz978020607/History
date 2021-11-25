def b2i(a):
    num=0
    for ii in range(len(a)):
        num = num*256 + a[ii]
    
    return num 
    