from srun4k import *
import sys

gatewayUrl = "https://gw.buaa.edu.cn"

def usageHelper():
    print("Usage: \n login username password\n logout username\n logout_all username password\n check_online")

def main():
    if len(sys.argv) < 2:
        usageHelper()
        return
    
    option = sys.argv[1]
    if option == "login":
        if len(sys.argv) < 4:
            usageHelper()
            return
        username = sys.argv[2]
        password = sys.argv[3]
        ret = do_login(gatewayUrl, username, password)
        if ret['success']:
            print('成功！')
        else:
            print('失败！\n' + ret['reason'])
    elif option == "logout":
        if len(sys.argv) < 3:
            usageHelper()
            return
        username = sys.argv[2]
        ret = do_logout(gatewayUrl, username)
        if ret['success']:
            print('成功！')
        else:
            print('失败！\n' + ret['reason'])
    elif option == "check_online":
        print(check_online(gatewayUrl))
    elif option == "logout_all":
        if len(sys.argv) < 4:
            usageHelper()
            return
        username = sys.argv[2]
        password = sys.argv[3]
        ret = force_logout(gatewayUrl, username, password)
        if ret['success']:
            print('成功！')
        else:
            print('失败！\n' + ret['reason'])
    else:
        usageHelper()


if __name__ == "__main__":
    main()
