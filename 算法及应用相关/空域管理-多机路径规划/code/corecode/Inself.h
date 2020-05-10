#pragma once
#include<iostream>
using namespace std;
#include<vector>
#include<math.h>
#include<list>
const int kCost1 = 10;//邻格
const int kCost2 = 14;//斜格消耗
const int safe_distance = 0; //安全距离

struct Point {
    int x, y;
    float t;
    int F, G, H;
    Point *parent;
    //初始化坐标
    Point(int _x, int _y) :x(_x), y(_y), F(0), G(0), H(0), t(0),parent(NULL)
    {
    }

};

struct float_Point
{
    float x,y,t;
    float_Point(float _x, float _y):x(_x),y(_y),t(0){}
    float_Point(float _x, float _y,float _t):x(_x),y(_y),t(_t){}
};


class Inself {
public:
    void InitInself(std::vector<std::vector<int>>&_maze);
    std::list<Point *> GetfPath(Point &startPoint, Point &endPoint, bool isIgnoreCorner);
    std::vector<Point *> Self(std::vector<std::vector<int>>&_maze,Point  startPoint, Point  endPoint, bool isIgnoreCorner); //自遍历优化
    //std::list<Point *> GetPath(Point &startPoint, Point &endPoint, bool isIgnoreCorner); //起终点，是否能斜着走

    std::vector<float_Point *>float_Self(std::vector<std::vector<int>>&_maze,Point  startPoint, Point  endPoint);



    //释放内存
    void clearRAM(vector<Point *> aa);
    void clearRAM_except(vector<Point *> aa,Point * except_one = NULL);

    std::vector<std::vector<int>> maze;
private:
    Point *findPath(Point &startPoint, Point &endPoint, bool isIgnoreCorner);
    //Point *refindPath(Point &startPoint, Point &endPoint, bool isIgnoreCorner);
    std::vector<Point *>getSurroundPoints(const Point *point, bool isIgnoreCorner);
    bool isCanreach(const Point *point, const Point *target, bool isIgnoreCorner, int safe_d) const;//judge if there is a solution
    Point *isInList(Point * curPoint, const Point *point)const;
    //Point *getLeastFpoint(Point * point, bool isIgnoreCorner);   //return Fmin point from openlist,F=G+H
    bool isoneline(const Point *p1, const Point *p2, bool isIgnoreCorner);
    bool islineok(const Point *point, const Point *target);
    int calcG(Point *temp_start, Point *point);
    int calcH(Point *point, Point *end);
    int calcF(Point *point);
    float calDegree(Point *p1, Point *p2);

    void extend(Point *p1,Point *p2);


    vector<Point *> all_temp_Point;
public://公有成员：
    int inspire_num;
    int final_num;

};
