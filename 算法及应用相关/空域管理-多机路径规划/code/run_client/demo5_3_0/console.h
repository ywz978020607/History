#ifndef CONSOLE_H
#define CONSOLE_H

#include<iostream>
#include<vector>

#include"Hurricane.h"
#include"Plane.h"
#include"Inself.h"
#include<math.h>
#include<QDebug>
#include<time.h>

//#include<Windows.h>         //鼠标点击添加障碍物
/////////////////
///

#include <QtSql/QSqlDatabase>
#include <QStringList>
#include <QSqlQuery>
#include <QCoreApplication>
///
using namespace std;

//地图大小
#define msizex 27
#define msizey 27
const int safe_d = 1;//安全距离
const int this_jizhan_number = 0; // 左上角0，右上角1，右下角2，左下角3

class Console
{
public:
    /* Properties */
    int time;
    Inself ins1;
    vector<Plane*> planes_status; // About all the planes status.
    vector<Plane*> stop_planes_status; // About all the stop planes.
    vector<vector<int>> map; //0：pass; 1:origin_stone ; 2：encounterPoint;3:hurricanPoint;4:encounter&hurricane
    vector<vector<int>> temp_map;
    vector<Hurricane*> hurricane_status; // About all the hurricane status

    //sql
    QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL");
    char cmd[256]; // To control the sql
    Plane plane_next;
    /* Functions */

    bool createNewPlane(Point start , Point end,int speed,int plane_number);
    bool createNewPlane(Plane *pp);
    bool createHurricane(Point a, int delta_t, int radius);
    void deleteHurricane();
    void StopToMove();
    void refreshPlane();
    void movePlane(int t,int pieces_num);

    bool judgeEncounter(Plane *new_plane);
    void addMapPoint(int x,int y, int val);
    bool refreshAllPath();

    bool Init_map();
    void fresh_map_air_stones();
    void deleteMapPoint(int x, int y, int val);
    void refresh_temp_map();
    bool refresh_path_time(vector<float_Point *> &path,int t_start,int v);
    void removeEncounterMap();

    //sql
    void initsql();
    bool sql_add();
    void sql_delete(int plane_number);


};


#endif
