#pragma once
#include<iostream>
using namespace std;
#include<vector>
#include<list>
#include"Inself.h" //启发式深搜inspiredfs + 自遍历优化self
#include<time.h>
#include<Windows.h>         //鼠标点击添加障碍物

#define safe_d 10 //地图边界安全距离，防溢出

//地图大小
#define msizex 55
#define msizey 55
//障碍物边长
#define rlength 5
//起终点
#define start_position (5,5)
#define end_position (45,45)

/*
main

vector<vcector<int>> maze;
maze.resize(50);//first

for(i =0;i<50;i++)
{
    maze[i].resize(100);
    }

*/


//map L
void init_map_L(std::vector<std::vector<int>>& maze)
{
    for (unsigned int i = 0; i < msizex; i++) {
        maze[i].resize(msizey);
    }

    for (int i = 0; i < msizex; ++i) {
        for (int j = 0; j < msizey; ++j) {
            maze[i][j] = 0;
        }
    }

    int rock_num = rand() % 5 + 25;

    for (int i = 0; i < rock_num; ++i) {
        int x = rand() % (msizex - rlength-safe_d*2)+safe_d;
        int y = rand() % (msizey - rlength-safe_d*2)+safe_d;
        for (int j = x; j < x + rlength; ++j) {
            for (int k = y; k < y + rlength; ++k) {
                maze[j][k] = 1;
            }
        }
    }
}



void resetmap(std::vector<std::vector<int>>& maze)
{
    for (int i = 0; i < msizex; ++i)
    {
        for (int j = 0; j < msizey; j++)
        {
            if (maze[i][j] != 0 && maze[i][j] != 1)   //注意，maze[i][j]
                maze[i][j] = 0;
        }
    }
}

int research_num(std::vector<std::vector<int>>& maze)
{
    int num = 0;
    for (int i = 0; i < msizex; ++i)
    {
        for (int j = 0; j < msizey; j++)
        {
            if (maze[i][j] != 0 && maze[i][j] != 1)
                num++;
        }
    }
    return num;
}
