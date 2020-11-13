#include<iostream>
#include<conio.h>
#include"Astar.h"
#include"Maps.h"
#define start_position (10,10)
#define end_position (190,190)
using namespace std;


/*
void HideCursor()//隐藏控制台的光标 
{
	CONSOLE_CURSOR_INFO cursor_info = { 1, 0 };
	SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);
}*/

int main()
{
	//HideCursor(); //隐藏控制台的光标 
	DWORD start_time = GetTickCount();
	vector<vector<int>>maze(msize);
	init_map_L(maze);//初始化地图及边界。

	Astar astar;
	astar.InitAstar(maze);
	Point start start_position;
	Point end end_position;
	list<Point *> path = astar.GetPath(start, end, true);

	DWORD end_time = GetTickCount();
	cout << endl << "方案：";
	switch (mode)
	{
	case 1:cout << "广搜" << endl; break;
	case 2:cout << "A*" << endl; break;
	case 3:cout << "Dijistra" << endl; break;
	case 4:cout << "启发项只有当前点与终点距离的A*变型" << endl; break;
	}
	cout <<endl<< "The run time is:" << (end_time - start_time) << "ms!" ;//输出运行时间
	cout << endl << "开拓点数" << astar.check_num << endl;
	cout << endl << "最终路径长度" << astar.final_num << endl;

	cout << endl << "队列/最小优先队列的元素数量最大值" << max_num << endl;
	for (auto &p : path)
		cout << '(' << p->x << ',' << p->y << ')' << endl;
	

	while (1);
	return 0;
}