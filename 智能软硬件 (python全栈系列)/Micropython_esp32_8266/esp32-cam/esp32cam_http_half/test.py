from microWebSrv import MicroWebSrv 

mws = MicroWebSrv() # TCP port 80 and files in /flash/wwwm

mws.Start()         # Starts server in a new thread

##################
mws = MicroWebSrv(routeHandlers=None, port=80, bindIP='0.0.0.0', webPath="/flash/")

mws.Start(threaded=True)


################
from microWebSrv import MicroWebSrv
mws = MicroWebSrv()      # TCP port 80 and files in /flash/www
mws.Start(threaded=True) # Starts server in a new thread

