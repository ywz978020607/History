#include<iostream>

using namespace std;

class Hurricane
{
public:
    /* Properties */
    int x, y; // The center (x,y)
    int radius; // The hurricane range: [x-radius,x+radius]*[y-radius,y+radius]
    int end_time;

    /* Functions */
    void initHurricane(int _x,int  _y,int _radius,int _end_time)
    {
        x = _x;
        y = _y;
        radius = _radius;
        end_time = _end_time;
    }

};

