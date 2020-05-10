from django.shortcuts import render
import MySQLdb

from django.http import HttpResponse
def test_hanshu(request):
   # print(request.GET.get('a1'))
#    print(request.json(username = request.GET.get('username',default='xxx')))
    print(request)
    
    flag = 0
    flag = str(request.GET.get('a0'))
    a1 = str(request.GET.get('a1'))
    a2 = str(request.GET.get('a2'))
    a3 = str(request.GET.get('a3'))
    a4 = str(request.GET.get('a4'))
    a5 = str(request.GET.get('a5'))
    
    if flag =='1':
        sql_jiaoben = """INSERT INTO user_add (Startx,Starty,Endx,Endy,v) SELECT """+a1+","+a2+","+a3+","+a4+","+a5+""" FROM dual WHERE not exists (select *from user_add where Startx="""+a1+" AND Starty="+a2+" AND Endx="+a3+" And Endy="+a4+" AND v="+a5+");"
    
    elif flag=='2':
        sql_jiaoben = """truncate table user_add;"""
    else:
        sql_jiaoben=""
    
    
    try:
        con = MySQLdb.connect(host='39.105.218.125',port=3306,user='root',passwd='Ywz19980316',db='test1')
        cursor = con.cursor()
        
        try:
            if flag == 3:
                cursor.execute("""truncate table user_add;""")
                con.commit()
                cursor.execute("""truncate table delete_table;""")
                con.commit()
                cursor.execute("""truncate table add_to_area;""")
                con.commit()
            else:
                cursor.execute(sql_jiaoben)
                con.commit()
        except:
            con.rollback()
        
        con.close()
    except:
        return HttpResponse("0")


    return HttpResponse("Hello World!")



# Create your views here.
