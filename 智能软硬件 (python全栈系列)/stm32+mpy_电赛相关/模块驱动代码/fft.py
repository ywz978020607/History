# algorithms.py
# 14th March 2015
# Examples of Discrete Fourier Transform code in Python
# http://forum.micropython.org/viewtopic.php?f=2&t=208&hilit=fft
#
import math, cmath

# Recursive algorithm: simple but slow and stack-hungry
# Enter with an array of complex numbers of length 2**N
def fft_recursive(x):
    n = len(x)
    if n <= 1:
        return x
    even = fft(x[0::2])
    odd =  fft(x[1::2])
    return [even[m] + math.e**(-2j*math.pi*m/n)*odd[m] for m in range(n//2)] + \
           [even[m] - math.e**(-2j*math.pi*m/n)*odd[m] for m in range(n//2)]

# Code used as the basis for the assembler routine. Cooley-Tukey algorithm with
# twiddle factors precomputed.

def fft(nums, roots, forward=True):
    n = len(nums)
    m = int(math.log(n)/math.log(2))
    #n= 2**m 
    #Do the bit reversal
    i2 = n >> 1
    j = 0
    for i in range(n-1):
        if i<j: nums[i], nums[j] =  nums[j], nums[i]
        k = i2
        while (k <= j):
            j -= k
            k >>= 1
        j+=k
    #Compute the FFT
    l2 = 1
    for l in range(m):
        c = roots[l]
        if forward:
            c = c.real -c.imag*1j
        l1 = l2
        l2 <<= 1
        u = 0j+1
        for j in range(l1):
            for i in range(j, n, l2):
                i1 = i+l1
                t1 = u*nums[i1]
                nums[i1] = nums[i] - t1
                nums[i] += t1
            u *= c
    # Scaling for forward transform
    if forward:
        for i in range(n):
            nums[i] /= n
    return nums   

def buildarrays(length):
    bits = int(math.log(length)/math.log(2))
    roots = []
    c = -1+0j
    roots.append(c)    # Complex roots of unity
    for x in range(bits):
        cimag = math.sqrt((1.0 - c.real) / 2.0) # Imaginary part
        creal = math.sqrt((1.0 + c.real) / 2.0) # Real part
        c = creal + cimag*1j
        roots.append(c) 
        
    re = [0+0j]*length
    return re, roots

# Test/demo for above algorithm

def printlist(q):
    s = ""
    for t in q:
        s += "[{:5.2f}{:5.2f}] ".format(t.real, t.imag)
    print(s)

nums, roots = buildarrays(16)
for x in range(len(nums)):
    nums[x] = 0.1+ math.cos(2*math.pi*x/len(nums))
print("Initial")
printlist(nums)
fft(nums, roots, True)
print("fft") 
printlist(nums)
print("Reverse transform")
fft(nums, roots, False)
printlist(nums)

