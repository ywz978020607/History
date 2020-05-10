#include<iostream>
#include<conio.h>
#include"Console.h"
#include<fstream>
using namespace std;


//输出障碍物坐标
void print_rock(vector<vector<int>> &maze)
{
    ofstream OutFileR("Rock.txt");
    for (int ii = 0; ii < msizex; ii++)
    {
        for (int jj = 0; jj < msizey; jj++)
        {
            if (maze[ii][jj] == 1)
                OutFileR << ii << "\t" << jj << endl;
        }
    }
    OutFileR.close();
}
int main()
{
    ofstream OutFile("Path1.txt");
    Console console;
       // init map.
   console.Init_map();
   // init time.
   console.time = 0;
    cout<<"1"<<endl;

    vector<float_Point *>path = console.ins1.float_Self(console.map,Point(18,1),Point(1,18));
    for(auto &p:path)
    {
        cout<<p->x<<","<<p->y<<endl;
        OutFile << p->x << '\t' << p->y << endl;
    }

   /* vector<Point *>path = console.ins1.Self(console.map,Point(4,4),Point(80,80),true);
    for(auto &p:path)
    {
        cout<<p->x<<","<<p->y<<endl;
        OutFile << p->x << '\t' << p->y << endl;
    }
*/

    /*while(true)
    {
        console.time++;
        console.deleteHurricane();

        //风暴
        if(0)

        {
            Point a(25,25);
            int delta_time, radius;
            console.createHurricane(a, delta_time, radius);
            console.refreshAllPath();
        }

        //加入飞机
        if(1)
        {
            Point start(10,10);
            Point end(60,60);
            int speed = 1;
            if(!console.createNewPlane(start,end,speed))
            {
                cout<<"wait for calculate."<<endl;
                continue;
            }
        }

        //检查是否停止的飞机可以移动
        console.StopToMove();

        //显示更新以及飞机到达出队
        console.refreshPlane();

        system("pause");
    }*/

    OutFile.close();            //关闭Path.txt文件
    //输出障碍物坐标 rock.txt
    print_rock(console.map);


    return 0;
}
