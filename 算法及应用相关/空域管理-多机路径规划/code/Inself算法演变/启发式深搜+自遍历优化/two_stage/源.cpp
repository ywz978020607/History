
#include<iostream>
#include<conio.h>
#include"Inself.h"
#include"Maps.h"

#define start_position (10,10)
#define end_position (190,190)
using namespace std;


int main()
{
	//HideCursor(); //隐藏控制台的光标 
	DWORD start_time = GetTickCount();
	vector<vector<int>>maze(msize);
	init_map_L(maze);//初始化地图及边界。

	Inself ins1;
	ins1.InitInself(maze);
	Point start start_position;
	Point end end_position;
	//list<Point *> path = astar.GetfPath(start, end, true);
	list<Point *> path = ins1.Self(start, end, true);
	maze = ins1.maze;


	DWORD end_time = GetTickCount();
	
	cout << "方案：" << "启发式深搜+自遍历优化路径" << endl;
	cout << endl << "The run time is:" << (end_time - start_time) << "ms!"<<endl;//输出运行时间
	cout << endl << "开拓点数" << research_num(maze) << endl;
	cout << endl << "启发式深搜路径长度" << ins1.inspire_num << endl;
	cout << endl << "最终路径长度" << ins1.final_num << endl;

	for (auto &p : path)
		cout << '(' << p->x << ',' << p->y << ')' << endl;
	/*
	for (int i = 0; i < msize; i++)
	{
		for (int j = 0; j < msize; j++)
		{
			cout << maze[i][j];
		}
		cout << endl;
	}
	*/
	while (1);
	return 0;
}
