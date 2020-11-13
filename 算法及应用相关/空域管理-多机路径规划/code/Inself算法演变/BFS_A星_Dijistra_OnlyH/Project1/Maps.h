#pragma once
#include<iostream>
using namespace std;
#include<vector>
#include<list>
#include"Astar.h"
#include<time.h>
#include<Windows.h>         //鼠标点击添加障碍物
#define msize 200
#define barrier_num 30     //障碍物数量
#define safe_distance 1    //安全距离
#define safe_value 9     //等待转换为1的安全值
char out = '>';
 unsigned long _time=100;


 //map L
 void init_map_L(std::vector<std::vector<int>>& maze)
 {
	 for (int i = 0; i < msize; i++) {
		 maze[i].resize(msize);
	 }
	 //边界障碍物
	 for (int i = 0; i < msize; i++)
	 {
		 if (i == 0 || i == msize - 1)
		 {
			 for (int j = 0; j < msize - 1; j++)
			 {
				 maze[i][j] = 1;
				 //	gotoxy(i, j);
					 //cout << maze[i][j];
			 }
		 }
		 else {
			 maze[i][0] = 1;
			 //gotoxy(i, 0);
			 //cout << maze[i][0];
			 maze[i][msize - 1] = 1;
			 //gotoxy(i, msize - 1);
			 //cout << maze[i][msize - 1];
			 for (int j = 1; j < msize - 2; j++)
				 maze[i][j] = 0;
		 }
	 }

	 //镜像"L"障碍
	 for (int i = 50; i < 151; i++)
	 {
		 maze[i][150] = 1;
		 maze[150][i] = 1;
	 }
 }



 void resetmap(std::vector<std::vector<int>>& maze)
 {
	 for (int i = 0; i < msize; i++)
	 {
		 for (int j = 0; j < msize; j++)
		 {
			 if (maze[j][i] != 0 && maze[j][i] != 1)   //注意，\n是换y，所以遍历一个y对应的x，然后\n
				 maze[j][i] = 0;
		 }
	 }
 }

 int research_num(std::vector<std::vector<int>>& maze)
 {
	 int num = 0;
	 for (int i = 0; i < msize; i++)
	 {
		 for (int j = 0; j < msize; j++)
		 {
			 if (maze[j][i] != 0 && maze[j][i] != 1)
				 num++;
		 }
	 }
	 return num;
 }