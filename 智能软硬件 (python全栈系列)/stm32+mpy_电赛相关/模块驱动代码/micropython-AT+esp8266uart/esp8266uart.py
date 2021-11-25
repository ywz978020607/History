from pyb import UART
from pyb import delay
from pyb import micros, elapsed_micros

# This hashmap collects all generic AT commands
CMDS_GENERIC = {
    'TEST_AT': b'AT',
    'RESET': b'AT+RST',
    'VERSION_INFO': b'AT+GMR',
    'DEEP_SLEEP': b'AT+GSLP',
    'ECHO': b'ATE',
    'FACTORY_RESET': b'AT+RESTORE',
    'UART_CONFIG': b'AT+UART'
    }

# All WIFI related AT commands
CMDS_WIFI = {
    'MODE' : b'AT+CWMODE',
    'CONNECT': b'AT+CWJAP',
    'LIST_APS': b'AT+CWLAP',
    'DISCONNECT': b'AT+CWQAP',
    'AP_SET_PARAMS': b'AT+CWSAP',
    'AP_LIST_STATIONS': b'AT+CWLIF',
    'DHCP_CONFIG': b'AT+CWDHCP',
    'SET_AUTOCONNECT': b'AT+CWAUTOCONN',
    'SET_STATION_MAC': b'AT+CIPSTAMAC',
    'SET_AP_MAC': b'AT+CIPAPMAC',
    'SET_STATION_IP': b'AT+CIPSTA',
    'SET_AP_IP': b'AT+CIPAP'
    }

# IP networking related AT commands
CMDS_IP = {
    'STATUS': b'AT+CIPSTATUS',
    'START': b'AT+CIPSTART',
    'SEND': b'AT+CIPSEND',
    'CLOSE': b'AT+CIPCLOSE',
    'GET_LOCAL_IP': b'AT+CIFSR',
    'SET_MUX_MODE': b'AT+CIPMUX',
    'CONFIG_SERVER': b'AT+CIPSERVER',
    'SET_TX_MODE': b'AT+CIPMODE',
    'SET_TCP_SERVER_TIMEOUT': b'AT+CIPSTO',
    'UPGRADE': b'AT+CIUPDATE',
    'PING': b'AT+PING'
    }
    
# WIFI network modes the ESP8266 knows to handle
WIFI_MODES = {
    1: 'Station',
    2: 'Access Point',
    3: 'Access Point + Station',
    }
# Reverse feed lookup table
for key in WIFI_MODES.keys():
    WIFI_MODES[WIFI_MODES[key]] = key
    
# WIFI network security protocols known to the ESP8266 module
WIFI_ENCRYPTION_PROTOCOLS = {
    0: 'OPEN',
    1: 'WEP',
    2: 'WPA_PSK',
    3: 'WPA2_PSK',
    4: 'WPA_WPA2_PSK'
    }
# Reverse feed lookup table
for key in WIFI_ENCRYPTION_PROTOCOLS.keys():
    WIFI_ENCRYPTION_PROTOCOLS[WIFI_ENCRYPTION_PROTOCOLS[key]] = key

class CommandError(Exception):
    pass
    
class CommandFailure(Exception):
    pass
    
class UnknownWIFIModeError(Exception):
    pass

class ESP8266(object):

    def __init__(self, uart=1, baud_rate=115200):
        """Initialize this module. uart may be an integer or an instance 
        of pyb.UART. baud_rate can be used to set the Baud rate for the 
        serial communication."""
        if uart:
            if type(uart) is int:
                self.uart = UART(uart, baud_rate)
            elif type(uart) is UART:
                self.uart = uart
            else:
                raise Exception("Argument 'uart' must be an integer or pyb.UART object!")
        else:
            raise Exception("Argument uart must not be 'None'!")

    def _send_command(self, cmd, timeout=0, debug=False):
        """Send a command to the ESP8266 module over UART and return the 
        output.
        After sending the command there is a 1 second timeout while 
        waiting for an anser on UART. For long running commands (like AP 
        scans) there is an additional 3 seconds grace period to return 
        results over UART.
        Raises an CommandError if an error occurs and an CommandFailure 
        if a command fails to execute."""
        if debug:
            start = micros()
        cmd_output = []
        okay = False
        if cmd == '' or cmd == b'':
            raise CommandError("Unknown command '" + cmd + "'!")
        # AT commands must be finalized with an '\r\n'
        cmd += '\r\n'
        if debug:
            print("%8i - TX: %s" % (elapsed_micros(start), str(cmd)))
        self.uart.write(cmd)
        # wait at maximum one second for a command reaction
        cmd_timeout = 100
        while cmd_timeout > 0:
            if self.uart.any():
                cmd_output.append(self.uart.readline())
                if debug:
                    print("%8i - RX: %s" % (elapsed_micros(start), str(cmd_output[-1])))
                if cmd_output[-1].rstrip() == b'OK':
                    if debug:
                        print("%8i - 'OK' received!" % (elapsed_micros(start)))
                    okay = True
                delay(10)
            cmd_timeout -= 1
        if cmd_timeout == 0 and len(cmd_output) == 0:
            if debug == True:
                print("%8i - RX timeout of answer after sending AT command!" % (elapsed_micros(start)))
            else:
                print("RX timeout of answer after sending AT command!")
        # read output if present
        while self.uart.any():
            cmd_output.append(self.uart.readline())
            if debug:
                print("%8i - RX: %s" % (elapsed_micros(start), str(cmd_output[-1])))
            if cmd_output[-1].rstrip() == b'OK':
                if debug:
                    print("%8i - 'OK' received!" % (elapsed_micros(start)))
                okay = True
        # handle output of AT command 
        if len(cmd_output) > 0:
            if cmd_output[-1].rstrip() == b'ERROR':
                raise CommandError('Command error!')
            elif cmd_output[-1].rstrip() == b'OK':
                okay = True
            elif not okay:
                # some long running commands do not return OK in case of success 
                # and/or take some time to yield all output.
                if timeout == 0:
                    cmd_timeout = 300
                else:
                    if debug:
                        print("%8i - Using RX timeout of %i ms" % (elapsed_micros(start), timeout))
                    cmd_timeout = timeout / 10
                while cmd_timeout > 0:
                    delay(10)
                    if self.uart.any():
                        cmd_output.append(self.uart.readline())
                        if debug:
                            print("%8i - RX: %s" % (elapsed_micros(start), str(cmd_output[-1])))
                        if cmd_output[-1].rstrip() == b'OK':
                            okay = True
                            break
                        elif cmd_output[-1].rstrip() == b'FAIL':
                            raise CommandFailure()
                    cmd_timeout -= 1
            if not okay and cmd_timeout == 0 and debug:
                print("%8i - RX-Timeout occured and no 'OK' received!" % (elapsed_micros(start)))
        return cmd_output
    
    @classmethod
    def _join_args(cls, *args, debug=True):
        """Joins all given arguments as the ESP8266 needs them for the 
        argument string in a 'set' type command.
        Strings must be quoted using '"' and no spaces outside of quoted 
        srrings are allowed."""
        while type(args[0]) is tuple:
            if len(args) == 1:
                args = args[0]
        if debug:
            print(args)
        str_args = []
        for arg in args:
            if type(arg) is str:
                str_args.append('"' + arg + '"')
            elif type(arg) is bytes:
                str_args.append(arg.decode())
            elif type(arg) is bool:
                str_args.append(str(int(arg)))
            else:
                str_args.append(str(arg))
        if debug:
            print(str_args)
        return ','.join(str_args).encode()
        
    @classmethod
    def _parse_accesspoint_str(cls, ap_str):
        """Parse an accesspoint string description into a hashmap 
        containing its parameters. Returns None if string could not be 
        split into 3 or 5 fields."""
        if type(ap_str) is str:
            ap_str = ap_str.encode()
        ap_params = ap_str.split(b',')
        if len(ap_params) == 5:
            (enc_mode, ssid, rssi, mac, channel) = ap_params
            ap = {
                'encryption_protocol': int(enc_mode), 
                'ssid': ssid, 
                'rssi': int(rssi), 
                'mac': mac, 
                'channel': int(channel)
                }
        elif len(ap_params) == 3:
            (enc_mode, ssid, rssi) = ap_params
            ap = {
                'encryption_protocol': int(enc_mode),
                'ssid': ssid,
                'rssi': int(rssi),
                }
        else:
            ap = None
        return ap
        
    def _query_command(self, cmd, timeout=0, debug=False):
        """Sends a 'query' type command and return the relevant output 
        line, containing the queried parameter."""
        return self._send_command(cmd + b'?', timeout=timeout, debug=debug)[1].rstrip()
            
    def _set_command(self, cmd, *args, timeout=0, debug=False):
        """Send a 'set' type command and return all lines of the output 
        which are not command echo and status codes.
        This type of AT command usually does not return output except 
        the echo and 'OK' or 'ERROR'. These are not returned by this 
        method. So usually the result of this methid must be an empty list!"""
        return self._send_command(cmd + b'=' + ESP8266._join_args(args, debug=debug), timeout=timeout, debug=debug)[1:-2]
        
    def _execute_command(self, cmd, timeout=0, debug=False):
        """Send an 'execute' type command and return all lines of the 
        output which are not command echo and status codes."""
        return self._send_command(cmd, timeout=timeout, debug=debug)[1:-2]

    def test(self, debug=False):
        """Test the AT command interface."""
        return self._execute_command(CMDS_GENERIC['TEST_AT'], debug=debug) == []

    def reset(self, debug=False):
        """Reset the module and read the boot message.
        ToDo: Interpret the boot message and do something reasonable with
        it, if possible."""
        boot_log = []
        if debug:
            start = micros()
        self._execute_command(CMDS_GENERIC['RESET'], debug=debug)
        # wait for module to boot and messages appearing on self.uart
        timeout = 300
        while not self.uart.any() and timeout > 0:
            delay(10)
            timeout -= 1
        if debug and timeout == 0:
            print("%8i - RX timeout occured!" % (elapsed_micros(start)))
        # wait for messages to finish
        timeout = 300
        while timeout > 0:
            if self.uart.any():
                boot_log.append(self.uart.readline())
                if debug:
                    print("%8i - RX: %s" % (elapsed_micros(start), str(boot_log[-1])))
            delay(20)
            timeout -= 1
        if debug and timeout == 0:
            print("%8i - RTimeout occured while waiting for module to boot!" % (elapsed_micros(start)))
        return boot_log[-1].rstrip() == b'ready'
        
    def get_mode(self, debug=False):
        """Returns the mode the ESP WIFI is in:
            1: station mode
            2: accesspoint mode
            3: accesspoint and station mode
        Check the hashmap esp8266.WIFI_MODES for a name lookup. 
        Raises an UnknownWIFIModeError if the mode was not a valid or 
        unknown.
        """
        mode = int(self._query_command(CMDS_WIFI['MODE']).split(b':')[1], debug=debug)
        if mode in WIFI_MODES.keys():
            return mode
        else:
            raise UnknownWIFIModeError("Mode '%s' not known!" % mode)
            
    def set_mode(self, mode, debug=False):
        """Set the given WIFI mode.
        Raises UnknownWIFIModeError in case of unknown mode."""
        if mode not in WIFI_MODES.keys():
            raise UnknownWIFIModeError("Mode '%s' not known!" % mode)
        return self._set_command(CMDS_WIFI['MODE'], mode, debug=debug)

    def get_accesspoint(self, debug=False):
        """Read the SSID of the currently joined access point.
        The SSID 'No AP' tells us that we are not connected to an access 
        point!"""
        answer = self._query_command(CMDS_WIFI["CONNECT"], debug=debug)
        #print("Answer: " + str(answer))
        if answer == b'No AP':
            result = None
        else:
            result = answer.split(b'+' + CMDS_WIFI['CONNECT'][3:] + b':')[1][1:-1]
        return result
        
    def connect(self, ssid, psk, debug=False):
        """Tries to connect to a WIFI network using the given SSID and 
        pre shared key (PSK). Uses a 20 second timeout for the connect 
        command.
        Bugs: AT firmware v0.21 has a bug to only join a WIFI which SSID 
        is 10 characters long."""
        self._set_command(CMDS_WIFI['CONNECT'], ssid, psk, debug=debug, timeout=20000)

    def disconnect(self, debug=False):
        """Tries to connect to a WIFI network using the given SSID and 
        pre shared key (PSK)."""
        return self._execute_command(CMDS_WIFI['DISCONNECT'], debug=debug) == []
        
    @classmethod
    def _parse_list_ap_results(cls, ap_scan_results):
        aps = []
        for ap in ap_scan_results:
            try:
                ap_str = ap.rstrip().split(CMDS_WIFI['LIST_APS'][-4:] + b':')[1].decode()[1:-1]
            except IndexError:
                # Catching this exception means the line in scan result 
                # was probably rubbish
                continue
            # parsing the ap_str may not work because of rubbish strings 
            # returned from the AT command. None is returned in this case.
            ap = ESP8266._parse_accesspoint_str(ap_str)
            if ap:
                aps.append(ap)
        return aps
        
    def list_all_accesspoints(self, debug=False):
        """List all available access points.
        TODO: The IoT AT firmware 0.9.5 seems to sporadically yield 
        rubbish or mangled AP-strings. Check needed!"""
        return ESP8266._parse_list_ap_results(self._execute_command(CMDS_WIFI['LIST_APS'], debug=debug))
        
    def list_accesspoints(self, *args):
        """List accesspoint matching the parameters given by the 
        argument list.
        The arguments may be of the types string or integer. Strings can 
        describe MAC adddresses or SSIDs while the integers refer to 
        channel names."""
        return ESP8266._parse_list_ap_results(self._set_command(CMDS_WIFI['LIST_APS'], args))
        
    def set_accesspoint_config(self, ssid, password, channel, encrypt_proto, debug=False):
        """Configure the parameters for the accesspoint mode. The module 
        must be in access point mode for this to work.
        After setting the parameters the module is reset to 
        activate them.
        The password must be at least 8 characters long up to a maximum of 
        64 characters.
        WEP is not allowed to be an encryption protocol. 
        Raises CommandFailure in case the WIFI mode is not set to mode 2 
        (access point) or 3 (access point and station) or the WIFI 
        parameters are not valid."""
        if self.get_mode() not in (2, 3):
            raise CommandFailure('WIFI not set to an access point mode!')
        if type(ssid) is not str:
            raise CommandFailure('SSID must be of type str!')
        if type(password) is not str:
            raise CommandFailure('Password must be of type str!')
        if len(password) > 64 or len(password) < 8:
            raise CommandFailure('Wrong password length (8..64)!')
        if channel not in range(1, 15) and type(channel) is not int:
            raise CommandFailure('Invalid WIFI channel!')
        if encrypt_proto not in (0, 2, 3, 4) or type(encrypt_proto) is not int:
            raise CommandFailure('Invalid encryption protocol!')
        self._set_command(CMDS_WIFI['AP_SET_PARAMS'], ssid, password, channel, encrypt_proto, debug=debug)
        self.reset()
        
    def get_accesspoint_config(self):
        """Reads the current access point configuration. The module must 
        be in an acces point mode to work.
        Returns a hashmap containing the access point parameters.
        Raises CommandFailure in case of wrong WIFI mode set."""
        if self.get_mode() not in (2, 3):
            raise CommandFailure('WIFI not set to an access point mode!')
        (ssid, password, channel, encryption_protocol) = self._query_command(CMDS_WIFI['AP_SET_PARAMS'], debug=False).split(b':')[1].split(b',')
        return {
            'ssid': ssid,
            'password': password,
            'channel': int(channel),
            'encryption_protocol': int(encryption_protocol)
            }
            
    def list_stations(self):
        """List IPs of stations which are connected to the access point.
        ToDo: Parse result and return python list of IPs (as str)."""
        return self._execute_command(CMDS_WIFI['AP_LIST_STATIONS'], debug=False)
    
    def set_dhcp_config(self, mode, status, debug=False):
        """Set the DHCP configuration for a specific mode.
        
        Oddities:
        The mode seems not to be the WIFI mode known from the methods 
        set_mode() and get_mode(). The mode are as follows according to 
        the Esspressif documentation:
          0: access point (softAP)
          1: station
          2: access point and station
        The second argument (status) is strange as well:
          0: enable
          1: disable
        """
        # Invert status to make the call to this methid reasonable.
        if type(status) is int:
            status = bool(status)
        if type(status) is bool:
            status = not status
        return self._set_command(CMDS_WIFI['DHCP_CONFIG'], mode, status, debug=debug)
        
    def set_autoconnect(self, autoconnect, debug=False):
        """Set if the module should connnect to an access point on 
        startup."""
        return self._set_command(CMDS_WIFI['SET_AUTOCONNECT'], autoconnect, debug=debug)
    
    def get_station_ip(self, debug=False):
        """get the IP address of the module in station mode.
        The IP address must be given as a string. No check on the 
        correctness of the IP address is made."""
        return self._query_command(CMDS_WIFI['SET_STATION_IP'], debug=debug)
        
    def set_station_ip(self, ip_str, debug=False):
        """Set the IP address of the module in station mode.
        The IP address must be given as a string. No check on the 
        correctness of the IP address is made."""
        return self._set_command(CMDS_WIFI['SET_STATION_IP'], ip_str, debug=debug)
    
    def get_accesspoint_ip(self, debug=False):
        """get the IP address of the module in access point mode.
        The IP address must be given as a string. No check on the 
        correctness of the IP address is made."""
        return self._query_command(CMDS_WIFI['SET_AP_IP'], debug=debug)
        
    def set_accesspoint_ip(self, ip_str, debug=False):
        """Set the IP address of the module in access point mode.
        The IP address must be given as a string. No check on the 
        correctness of the IP address is made."""
        return self._set_command(CMDS_WIFI['SET_AP_IP'], ip_str, debug=debug)
    
    def get_connection_status(self):
        """Get connection information.
        ToDo: Parse returned data and return python data structure."""
        return self._execute_command(CMDS_IP['STATUS'])
        
    def start_connection(self, protocol, dest_ip, dest_port, debug=False):
        """Start a TCP or UDP connection. 
        ToDo: Implement MUX mode. Currently only single connection mode is
        supported!"""
        self._set_command(CMDS_IP['START'], protocol, dest_ip, dest_port, debug=debug)
        
    def send(self, data, debug=False):
        """Send data over the current connection."""
        self._set_command(CMDS_IP['SEND'], len(data), debug=debug)
        print(b'>' + data)
        self.uart.write(data)
        
    def ping(self, destination, debug=False):
        """Ping the destination address or hostname."""
        return self._set_command(CMDS_IP['PING'], destination, debug=debug)
