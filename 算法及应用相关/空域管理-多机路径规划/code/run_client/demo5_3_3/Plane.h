#ifndef PLANE_H
#define PLANE_H

#include<iostream>
#include"Inself.h"
#include<list>

#include<QLabel>

using namespace std;

class Plane
{
public:
    /* Properties */
    int xin,yin,xout,yout; // The (x,y) of the start point and the end point
    int index_now;
    QLabel *label;
    int v; // The v of the plane
    float xnow, ynow; // The (x,y) of present
    int plane_number;
    int direction;
    float direction_f;
    std::vector<float_Point *> final_path; // The certain path of the plane

    /* Functions */
    void initSelf(int x_in, int y_in, int x_out, int y_out, int v_,std::vector<float_Point *> _final_path,int _plane_number)
    {
     /*Init the plane!
     * Args:
     *      x_in,y_in,x_out,y_out: The start (x,y) and the end (x,y) of the plane.
     *      V_: The speed of the plane.
     * Returns:
     *      None.
     *
     * Raises:
     *      IOErrors: None
     */


      //  static int bianhao = 0;
      //  bianhao++;
       // plane_number = bianhao;

        xin = x_in;
        xout = x_out;
        yin = y_in;
        yout = y_out;
        v = v_;
        final_path = _final_path;
        plane_number = _plane_number;
    }



};

#endif
