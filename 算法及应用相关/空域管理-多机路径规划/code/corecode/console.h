#include<iostream>
#include<vector>

#include"Hurricane.h"
#include"Plane.h"
#include"Inself.h"
#include<math.h>

#include<time.h>
#include<Windows.h>         //鼠标点击添加障碍物

using namespace std;

//地图大小
#define msizex 25
#define msizey 25

class Console
{
public:
    /* Properties */
    int time;
    Inself ins1;
    vector<Plane> planes_status; // About all the planes status.
    vector<Plane> stop_planes_status; // About all the stop planes.
    vector<vector<int>> map; //0：pass; 1:origin_stone ; 2：encounterPoint;3:hurricanPoint;4:encounter&hurricane
    vector<vector<int>> temp_map;
    vector<Hurricane> hurricane_status; // About all the hurricane status

    /* Functions */

    bool createNewPlane(Point start , Point end,int speed);
    bool createNewPlane(Plane &pp);
    bool createHurricane(Point a, int delta_t, int radius);
    void deleteHurricane();
    void StopToMove();
    void refreshPlane();

    bool judgeEncounter(Plane new_plane);
    void addMapPoint(int x,int y, int val);
    bool refreshAllPath();

    bool Init_map();
    void deleteMapPoint(int x, int y, int val);
    void refresh_temp_map();
    bool refresh_path_time(vector<Point *> &path,int t_start,int v);
    void removeEncounterMap();
};


