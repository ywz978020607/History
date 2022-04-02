https://blog.csdn.net/qq_36398005/article/details/108543089


sudo apt install -y iperf3

A机器：
```
iperf3 -s -p 5206
```

B机器：
```
#UDP
iperf3 -u -c 10.134.126.158 -p 5206 -b 1000M

#TCP
iperf3 -c 10.134.126.158 -p 5206 -b 1000M
```

