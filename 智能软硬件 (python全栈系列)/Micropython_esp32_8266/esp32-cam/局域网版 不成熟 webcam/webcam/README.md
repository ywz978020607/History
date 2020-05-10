
**Latest** script for webcam is mth_webcam.py a multi-threaded web server. Two threads serving port 80, one thread serving port 81, and the main thread serving port 82. The REPL is blocked. You can start one thread for port 82 if you want. In the main.py:

```python
import mth_webcam.py
```
will start the webcam server at hard reset (power cycle). Read [this](https://kopimojo.blogspot.com/2019/11/multi-threading-i-previously-used.html) blog concerning my multi-threaded webcam server.

Simple experimental webcam servers in AP and STA mode built using uasyncio.

The uasyncio package is provided here for your convenience. Please use the latest official version. 

The WiFi is a utility module. Please change the SSID and password for your home network.

Read [my blog](https://kopimojo.blogspot.com/)
