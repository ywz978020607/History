from mytcp import *
ip='127.0.0.1'
port = 8081
server = mytcp_server(ip,port)

client = mytcp_client(ip,port)

#############
client.write(b'\x01\x02')
server.read(0)

server.write(0,b'\x04\x06')
client.read()

client.close()
server.close(0)