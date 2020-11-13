#include "Console.h"

 bool Console::createNewPlane(Point start , Point end,int speed)
 {
    refresh_temp_map();
    vector<Point *> path = ins1.Self(temp_map,start, end, true);
   //////////////////////////////////////
    Plane new_plane;
    new_plane.initSelf(start.x,start.y,end.x,end.y,speed,path);
    /////////////////////////////////////
    if(path.empty()) //如果无路径
    {
        cout<<"no path calculated."<<endl;
         return false;
    }
    while(judgeEncounter(new_plane))
    {
        //如果有冲突点，在judgeEncounter中已更新map
        refresh_temp_map();
        new_plane.final_path = ins1.Self(temp_map,start,end,true);
        if(new_plane.final_path.empty())
            return false; //无路径
    }
    //成功得到路径

    //清空冲撞点Encounter
    removeEncounterMap();

    //时间戳更新
    if(!(refresh_path_time(new_plane.final_path,time,speed)))
    {
        cout<<"time_refresh_error!";
        return false;
    }
    planes_status.push_back(new_plane);
    return true;
 }

 bool Console::createNewPlane(Plane &pp)
 {
    refresh_temp_map();
    vector<Point *> path = ins1.Self(temp_map,Point(pp.xnow,pp.ynow), Point(pp.xout,pp.yout), true);
    ///////////////////////////////
    pp.final_path = path;
    //////////////////////////////
    if(path.empty()) //如果无路径
        return false;
    while(judgeEncounter(pp))
    {
        //如果有冲突点，在judgeEncounter中已更新map
        refresh_temp_map();
        pp.final_path = ins1.Self(temp_map,Point(pp.xnow,pp.ynow),Point(pp.xout,pp.yout),true);
        if(pp.final_path.empty())
            return false; //无路径
    }
    //成功得到路径

    //清空冲撞点Encounter
    removeEncounterMap();

    //时间戳更新
    if(!(refresh_path_time(pp.final_path,time,pp.v)))
    {
        cout<<"time_refresh_error!";
        return false;
    }
    planes_status.push_back(pp);
    return true;
 }


 bool Console::refreshAllPath()
 {
    vector<Plane> temp_planes;
    temp_planes = planes_status;
    planes_status.clear();

    for(int ii = 0 ;ii<temp_planes.size();ii++)
    {
        //首先判断原路径是否可以继续飞行
        int flag = 0;
        for(auto &p:temp_planes[ii].final_path)
        {
            if(map[p->x][p->y] != 0)//说明有飓风
            {
                flag = 1;
                break;
            }
        }

        if(flag == 0)//正常
            planes_status.push_back(temp_planes[ii]);
        else //有飓风
        {
            if(createNewPlane(temp_planes[ii]))
               continue;//下一个飞机
            else
                stop_planes_status.push_back(temp_planes[ii]);
        }
    }
    temp_planes.clear();
 }

 void Console::StopToMove()
 {
   vector<int> delete_num_list;
   delete_num_list.clear();

   for(int ii=0;ii<stop_planes_status.size();ii++)
   {
       if(createNewPlane(stop_planes_status[ii]))
           delete_num_list.push_back(ii);
   }

   for(int ii=0;ii<delete_num_list.size();ii++)
   {
       stop_planes_status.erase(stop_planes_status.begin()+delete_num_list[delete_num_list.size()-1-ii]);
   }

 }

 bool Console::judgeEncounter(Plane new_plane)
 /*Judge if planes encounter!
  *
  * Judge if planes encounter.
  * If yes: return True and refresh the fault status(count
  * the new fault point into it.).
  * if no: return False.
  *
  * Args:
  *      new_plane: new plane with all the information.
  *
  * Returns:
  *      bool: True or False.
  */
 {
     if(planes_status.empty())
     {
         return false;
     };

     int plane_num = planes_status.size();
     for(int i=0;i<plane_num;i++)
     {
         for(auto &p:new_plane.final_path)
         {
             for(auto &q:planes_status[i].final_path)
             {
                 if(p->x==q->x && p->y==q->y && (fabs(p->t-q->t)<1))
                 {
                     addMapPoint(p->x, p->y, 2);
                     return true;
                 }
             }
         }
     }
     return false;
 }

 void Console::addMapPoint(int x, int y, int val)
 /*Add to fault status!

     Add the encounter point and harricane to the fault status.

     Args:
         x,y :
         value:
             1: origin stone
             2: indicate encouter point.
             3: indicate harricane point.
             4: both of them.
 */
 {
     if(val == 1)
     {
         map[x][y] = 1;
         return;
     }
     if(map[x][y] == 0)
     {
         map[x][y] = val;
         return;
     }
     else
     {
         if(map[x][y] != val)
             map[x][y] = 4;
         else
             map[x][y] = val;//不变
     }
 }

 void Console::refresh_temp_map()
 /*
    copy map to temp_map,which is 0-1 map.
*/
 {
     for(unsigned int i =0 ;i<msizex;i++)
     {
         for(unsigned int j = 0;j < msizey;j++)
         {
            if(map[i][j] == 0)
                temp_map[i][j] = 0;
            else
                temp_map[i][j] = 1;
         }
     }
 }

 void Console::deleteMapPoint(int x, int y, int val)
 {
    if(map[x][y] == val)
    {
         map[x][y] = 0;
         return;
    }
    if(map[x][y] == 4)
    {
        if(val == 2)
        {
            map[x][y] = 3;
            return;
        }
        else if(val ==3)
        {
            map[x][y] = 2;
            return;
        }
    }
 }


 void Console::removeEncounterMap()
 {
     for(unsigned int i =0 ;i<msizex;i++)
     {
         for(unsigned int j = 0;j < msizey;j++)
         {
             deleteMapPoint(i,j,2);
         }
     }
 }

 bool Console::Init_map()
 {
    map.resize(msizex);
    for (unsigned int i = 0; i < msizex; i++) {
       map[i].resize(msizey);
    }

    temp_map.resize(msizex);
    for (unsigned int i = 0; i < msizex; i++) {
       temp_map[i].resize(msizey);
    }

    for(unsigned int i =0 ;i<msizex;i++)
    {
        for(unsigned int j = 0;j < msizey;j++)
        {
            temp_map[i][j] = 0;

            //边界boarder
            if(i == 0||i == msizex - 1||j == 0||j == msizey - 1)
                map[i][j] = 1;
            else
                map[i][j] = 0;
        }
    }

    //////////////
    //L型障碍
    for(unsigned int i =0 ;i<msizex;i++)
    {
        for(unsigned int j = 0;j < msizey;j++)
        {
            if(i >5 && i<15 && j ==10)
                map[i][j] = 1;
        }
    }

    map[9][3]=3;//常年风暴
 }

 bool Console::refresh_path_time(vector<Point *> &path, int t_start, int v)
 {
    int jishu = 0;
    for(auto &p:path)
    {
        if(jishu%v == 0)//整除v
        {
            p->t = t_start + jishu/v;
        }
        else
        {
            p->t = t_start + 0.5 + jishu/v;
        }
        jishu ++;
    }

    return true;
 }



 bool Console::createHurricane(Point a, int delta_t, int radius)
 {
     // Get into hurricane_status
     Hurricane new_hurricane;
     new_hurricane.initHurricane(a.x, a.y, radius, time+delta_t);
     hurricane_status.push_back(new_hurricane);

     // Get into map
     int i,j;
     for(i=0;i<(2*radius+2);i++)
     {
         for(j=0;j<(2*radius+2);j++)
         {
             addMapPoint(a.x-radius+i, a.y-radius+j, 3);
         }
     }
     return true;
 }

 void Console::deleteHurricane()
 {
     // If need to delete
     if(hurricane_status.empty())
     {
         return;
     }
     int hurricane_num;
     hurricane_num = hurricane_status.size();
     int i;
     int m,n;
     // remove from map.
     vector<int> delete_list; // Contain the index of hurricane
     // which need to be delete from the status.

     for(i=0;i<hurricane_num;i++)
     {
         if(hurricane_status[i].end_time>time)
         {
             continue;
         }
         // end_time == time
         // save the index whose hurricane need to be delete
         delete_list.push_back(i);
         for(m=0;m<(2*hurricane_status[i].radius+2);m++)
         {
             for(n=0;n<(2*hurricane_status[i].radius+2);n++)
             {
                 deleteMapPoint(hurricane_status[i].x-hurricane_status[i].radius+m, hurricane_status[i].y-hurricane_status[i].radius+n, 3);
             }
         }
     }

     // remove from the hurricane status.
     int delete_num;
     delete_num = delete_list.size();
     for(i=0;i<delete_num;i++)
     {
         hurricane_status.erase(hurricane_status.begin()+delete_num-1-i);
         // delete big index first will not affect the small index.
     }
 }

 void Console::refreshPlane()
 {//refresh xnow and ynow
     ///////////////////////

      vector<int> delete_plane_list;
      delete_plane_list.clear();

     for(int ii=0;ii<planes_status.size();ii++)
     {
          planes_status[ii].index_now += planes_status[ii].v;
          if(planes_status[ii].index_now<planes_status[ii].final_path.size())
          {
              planes_status[ii].xnow = planes_status[ii].final_path[planes_status[ii].index_now]->x;
              planes_status[ii].ynow = planes_status[ii].final_path[planes_status[ii].index_now]->y;
          }
          else//飞机飞出区域,则删除
          {
              delete_plane_list.push_back(ii);
          }
     }

     for(int ii=0;ii<delete_plane_list.size();ii++)
     {
         planes_status.erase(planes_status.begin()+delete_plane_list[delete_plane_list.size()-1-ii]);
     }
 }
