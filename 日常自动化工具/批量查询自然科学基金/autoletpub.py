import time
import requests
import csv


person_name_list = ['孙玲玲']

details_info = {}

def get_name_list():
    global person_name_list
    person_name_list = """
    魏晓辉
    王屹山
    王国宏
    李玉杰
    黄德双
    晏长岭
    穆志纯
    王均宏
    张艳宁
    梁荣华
    张向东
    王琼华
    郭康贤
    陈恩红
    孙利民
    周志鑫
    黎大兵
    金仲和
    刘明
    朱大奇
    付琨
    沈纲祥
    罗均
    陶建华
    吕建成
    韩家广
    章秀银
    郭松涛
    赵青
    尹怡欣
    冉广照
    杨明红
    宋令阳
    公茂果
    杜军平
    吴超仲
    许伟伟
    杨军
    文继荣
    刘光灿
    鄢社锋
    李朝晖
    张玉清
    谭永红
    郑庆华
    杜文莉
    屈军乐
    李亚丁
    彭文达
    钱卫宁
    李德玉
    徐学珍
    王云才
    郑文明
    张新平
    陈松灿
    田聪
    赵耀
    全智
    王永良
    谷延锋
    杜祖亮
    淄丽
    王美琴
    苏剑波
    胡占义
    廖桂生
    王大轶
    姬荣斌
    郭茂祖
    汪宏
    车文荃
    郜江瑞
    明东
    李小俚
    余荣
    董红召
    艾渤
    高宏
    刘佳琪
    张首刚
    储向峰
    张群飞
    王建浦
    高清维
    马泳
    靳文舟
    杨善林
    曾璇
    张苗苗
    桂卫华
    陈慧岩
    费敏锐
    谢少荣
    吴建鑫
    胡斌
    迟楠
    刘怡光
    乔俊飞
    高阳
    郭太锋
    迟学斌
    吴黎兵
    赵宇海
    杨金生
    潘炜
    吴启晖
    翁健
    段培永
    赵众
    李肯立
    韩银和
    陈少平
    陈增强
    赵维谦
    王新兵
    魏志义
    王吉华
    汪萌
    陈启军
    王丹
    雷建军
    廖晓峰
    邱景辉
    孙艳丰
    王良民
    吕超
    欧勇盛
    牛玉刚
    唐为华
    赵湛
    钱锋
    柴利
    冯全源
    张俊清
    张桂戌
    张利国
    陆品燕
    关柏鸥
    王国胤
    柴毅
    陈根祥
    薛向阳
    薛建儒
    姜育刚
    卓力
    李焱
    王建新
    操晓春
    纪荣嵘
    王士同
    尤著宏
    王熙照
    孙哲南
    蒋亚东
    周维虎
    李树涛
    胡章贵
    张昭
    曾志刚
    梅霆
    张承慧
    华长春
    徐友春
    李向阳
    张新亮
    缪向水
    张健
    林崇
    蒋林
    洪日昌
    黄河燕
    李伟生
    仲盛
    孙玲玲
    王树鹏
    黄维
    陈虹
    刘方爱
    杨健
    张广宇
    郭平
    郑铮
    江波
    董长昆
    薛晨阳
    徐现刚
    章毅
    方勇纯
    王一丁
    胡昌华
    洪文
    徐中伟
    李霞
    张军
    罗军舟
    邓少芝
    鲁耀兵
    周傲英
    吕岩
    朱日宏
    李天瑞
    石光明
    申德振
    李步洪
    苏良碧
    郭雷
    王建国
    王友清
    张勤
    邵建达
    谭小地
    赵建林
    谢胜利
    黄惠
    张伟力
    丁志军
    袁东风
    陶然
    周兴社
    黄庆明
    延凤平
    张群
    黄力
    薛泉
    莫则尧
    陈胜勇
    沈国震
    李克勤
    黄卡玛
    梁华国
    尹宝才
    何瑞春
    陈天石
    陈庆伟
    孙希明
    王世刚
    韩建达
    尚学群
    杨绍普
    夏银水
    陈晔
    赵强
    陈弘
    何军
    邹卫文
    王璞
    曹飞龙
    彭俊彪
    年夫顺
    唐祯然
    张文平
    吴仁彪
    康俊勇
    徐胜元
    史忠科
    李学龙
    刘先省
    继军
    何维兴
    朱艺华
    肖利民
    张软宇
    肖连团
    邱钧
    丁佐华
    张波
    张强
    程建功
    张战军
    荆涛
    赵国忠
    范建平
    顾幸生
    刘志勇
    乔学光
    张杰
    赵君
    段纯钢刚
    赵峰
    曾凡仔
    张宝林
    王典洪
    朱樟明
    王兴伟
    关治洪
    高西奇
    陶滢
    冯志全
    胡磊
    梁吉业
    吴信东
    余思远
    田玉平
    张涛
    吴玉程
    冯志勇
    吴先良
    何勇
    谢长生
陈前斌
张杰
吴仁彪
陶建华
王树鹏
鄢社锋
杨旸
洪文
张勤
孟丽民
虞露
瞿逢重
徐文
陈少平
闫连山
陈景东
张群飞
吴俊
雷建军
刘怡光
江建明
方志军
安平
汪敏
王海燕
袁东风
成秀珍
陶晓明
金欣
方璐
李刚
蒋刚毅
黄平平
朱洪波
周亮
潘成胜
丁大志
柏连发
吴启晖
王国宏
季向阳
王世刚
喻莉
江涛
季飞
张桂戌
李树涛
梁永生
谷延锋
张钦宇
孙大军
欧阳缮
赵峰
迟楠
高西奇
沈连丰
曾兵
朱策
李宏亮
李惠勇
陈山枝
彭木根
马华东 
邱钧
黄华
陶然
刘志文
安建平
艾渤
卓力
尹宝才
贾克斌
胡艳军
    """
    person_name_list = person_name_list.split("\n")

def get_info(person_name, details_info, idx = 0):
    person_name = person_name.strip()

    cookies = {
        'PHPSESSID': '7ahuoicna8l4fnqukqg8t3tfi5',
        'Hm_lvt_a94e857ae4207c3ac8fcfd63f6604f22': '1657872520',
        '_ga': 'GA1.3.1067340432.1657872520',
        '_gid': 'GA1.3.638212722.1657872520',
        '__utmc': '189275190',
        '__utmz': '189275190.1657872520.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'Hm_lpvt_a94e857ae4207c3ac8fcfd63f6604f22': '1657876568',
        '__utma': '189275190.1067340432.1657872520.1657872520.1657876568.2',
        '__utmt': '1',
        '__utmb': '189275190.2.10.1657876568',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'PHPSESSID=7ahuoicna8l4fnqukqg8t3tfi5; Hm_lvt_a94e857ae4207c3ac8fcfd63f6604f22=1657872520; _ga=GA1.3.1067340432.1657872520; _gid=GA1.3.638212722.1657872520; __utmc=189275190; __utmz=189275190.1657872520.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lpvt_a94e857ae4207c3ac8fcfd63f6604f22=1657876568; __utma=189275190.1067340432.1657872520.1657872520.1657876568.2; __utmt=1; __utmb=189275190.2.10.1657876568',
        'Origin': 'https://www.letpub.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://www.letpub.com.cn/index.php?page=grant',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'x-proxy-origin': 'http://10.226.42.75:5001',
}


    params = {
        'mode': 'advanced',
        'datakind': 'list',
        'currentpage': '1',
    }

    data = {
        'page': '',
        'name': '',
        'person': person_name,
        'no': '',
        'company': '',
        'addcomment_s1': '',
        'addcomment_s2': '',
        'addcomment_s3': '',
        'addcomment_s4': '',
        'money1': '',
        'money2': '',
        'startTime': '1997',
        'endTime': '2021',
        'province_main': '',
        'subcategory': '',
        'searchsubmit': 'true',
    }

    response = requests.post('https://www.letpub.com.cn/nsfcfund_search.php', params=params, cookies=cookies, headers=headers, data=data)
    # print(response.text)
    res_data = response.content.decode()
    # print(len(res_data))
    if len(res_data) < 300:
        print("have not data res, id:{},name:{}".format(idx, person_name))
        return False
    brief_data = res_data.split("script type=")[0]
    # print(brief_data)
    data_list = brief_data.split("""<td style="border:1px #DDD solid; border-collapse:collapse; text-align:left; padding:8px 8px 8px 8px; color:#3b5998; font-weight:bold;">""")[1:]
    # each_data = data_list[0]
    #
    for each_data in data_list:
        school = each_data.split("""<td style="border:1px #DDD solid; border-collapse:collapse; text-align:left; padding:8px 8px 8px 8px;">""")[1].split("</td")[0]
        second_code = each_data.split("学科代码</td")[-1].split("</td")[0].split("二级：")[-1].split("，")[0] # 二级解析
        third_code = each_data.split("学科代码</td")[-1].split("</td")[0].split("三级：")[-1].split("</td")[0]
        if second_code.startswith("F"):
            details_info[person_name] = [school, second_code, third_code]
            print(details_info[person_name])
            break
    return True

def write_csv(details_info):
    # diff
    already_info = {}
    reader1 = csv.reader(open("save.csv"))
    reader1_list = list(reader1)
    for item in reader1_list:
        already_info[item[0]] = item[1:]
    
    # csvfile = open("save.csv", 'w', newline='')
    csvfile = open("save.csv", 'a', newline='')
    writer = csv.writer(csvfile)
    # writer.writerow(['name', 'school', 'second_kind', 'third_kind'])
    for key in details_info.keys():
        if key not in already_info.keys():
            writer.writerow([key, details_info[key][0], details_info[key][1], details_info[key][2]])
    csvfile.close()



if __name__=="__main__":
    get_name_list()
    print("start")
    last_idx = 346
    while 1:
        try:
            for idx, person_name in enumerate(person_name_list):
                if idx < last_idx:
                    continue
                print("{}:{}".format(idx, person_name))
                res_flag = get_info(person_name, details_info, idx = idx)
                if not res_flag:
                    last_idx = idx
                    break
                time.sleep(5)
        except Exception as e:
            print("error:{}".format(e))

        print(details_info)
        write_csv(details_info)
        print(idx)
        print("done")
        time.sleep(20)
        # print(set(person_name_list) - set(details_info.keys()))



