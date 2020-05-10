#include "Console.h"
#include<iostream>
using namespace std;


 bool Console::createNewPlane(Point start , Point end,int speed,int plane_number)
 {
    refresh_temp_map();
    vector<float_Point *> path = ins1.float_Self(temp_map,start, end);
    refresh_path_time(path,time,speed);
   //////////////////////////////////////
    Plane *new_plane = new Plane();
    new_plane->initSelf(start.x,start.y,end.x,end.y,speed,path,plane_number);

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
        path = ins1.float_Self(temp_map,start,end);

        //先释放原final_path的内存：
        ins1.fclearRAM(new_plane->final_path);

        refresh_path_time(path,time,speed);
        new_plane->final_path = path;

        if(new_plane->final_path.empty())
        {
            delete(new_plane);
            return false; //无路径
        }
    }
    //成功得到路径

    //清空冲撞点Encounter
    removeEncounterMap();

    planes_status.push_back(new_plane);
    return true;
 }

 bool Console::createNewPlane(Plane *pp)
 {
    refresh_temp_map();
    pp->xin = (int)(pp->xnow);
    pp->yin = (int)(pp->ynow);

    vector<float_Point *> path = ins1.float_Self(temp_map,Point(pp->xin,pp->yin), Point(pp->xout,pp->yout));
    refresh_path_time(path,time,pp->v);
    ///////////////////////////////
    pp->final_path = path;
    //////////////////////////////
    if(path.empty()) //如果无路径
        return false;
    while(judgeEncounter(pp))
    {
        //如果有冲突点，在judgeEncounter中已更新map
        refresh_temp_map();

        //先释放原final_path的内存：
        ins1.fclearRAM(pp->final_path);

        pp->final_path = ins1.float_Self(temp_map,Point(pp->xin,pp->yin),Point(pp->xout,pp->yout));
        refresh_path_time(pp->final_path,time,pp->v);
        if(pp->final_path.empty())
            return false; //无路径
    }
    //成功得到路径

    //清空冲撞点Encounter
    removeEncounterMap();

    planes_status.push_back(pp);
    return true;
 }


 bool Console::refreshAllPath()
 {
    vector<Plane *> temp_planes;
    temp_planes = planes_status;
    planes_status.clear();

    for(int ii = 0 ;ii<temp_planes.size();ii++)
    {
        //首先判断原路径是否可以继续飞行
        int flag = 0;
        for(auto &p:temp_planes[ii]->final_path)
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

 bool Console::judgeEncounter(Plane *new_plane)
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
         for(auto &p:new_plane->final_path)
         {
             for(auto &q:planes_status[i]->final_path)
             {
                 if(fabs(p->x - q->x) < 1 &&fabs(p->y - q->y) < 1 && (fabs(p->t-q->t)<1.5))
                 {
                     addMapPoint(int(p->x), int(p->y), 2);//飞机自己的路径上某个设为障碍
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

             7:air stones.
 */
 {
     if(x<0||x>=msizex||y<0||y>=msizey)
         return;

     if(val == 1)
     {
         map[x][y] = 1;
         return;
     }
     if(map[x][y] == 0 ||map[x][y] == 7)
     {
         map[x][y] = val;
         return;
     }
     else if(map[x][y]==2)
     {
         if(val == 3)
             map[x][y] = 4;
         else if(val == 2)
             ;
     }
     else if(map[x][y]==3)
     {
         if(val == 2)
             map[x][y] = 4;
         else if(val == 3)
             ;
     }

     fresh_map_air_stones();
 }


 void Console::fresh_map_air_stones()
 {
     int flag_air;
     for(int ii =0;ii<msizex;ii++)
     {
         for(int jj =0;jj<msizey;jj++)
         {
             flag_air = 0;
             for(int mm = -safe_d;mm<=safe_d;mm++)
             {
                 for(int nn = -safe_d;nn<=safe_d;nn++)
                 {
                     //边界没有安全距离！
                     if(((ii+mm)<=0)||((ii+mm)>= msizex-1)||((jj+nn)<=0)||((jj+nn)>= msizey-1))
                         continue;
                     else
                     {
                         if((map[ii+mm][jj+nn] == 3||map[ii+mm][jj+nn] == 4) && (map[ii][jj]!=3 && map[ii][jj]!=4))
                         {
                             flag_air = 1;
                             map[ii][jj] = 7;
                             break;
                         }
                        if(map[ii+mm][jj+nn] == 1 && map[ii][jj]!=1)
                        {
                            flag_air = 1;
                            map[ii][jj] = 7;
                            break;
                        }
                     }
                 }
                 if(flag_air)
                     break;
             }
             if(!flag_air)//没有障碍
             {
                 if(map[ii][jj] == 7)
                     map[ii][jj] = 0;
             }
         }
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
                temp_map[i][j] = 1;//包括空气墙
         }
     }
 }

 void Console::deleteMapPoint(int x, int y, int val)
 {
     if(x<0||x>=msizex||y<0||y>=msizey)
         return;
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

    fresh_map_air_stones();
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

 void Console::initsql()
 {
     db.setHostName("39.105.218.125");
     db.setDatabaseName("test1");
     db.setUserName("root");
     db.setPassword("Ywz19980316");

     if(db.open())
     {
         qDebug()<<"connect successfully!";
     }
     else {
         qDebug()<<"sql open false!!!!!!!!!";
     }
 }

 bool Console::sql_add()
 {
     QSqlQuery query(db);
     sprintf(cmd,"SELECT *FROM add_to_area WHERE Area_number = %d LIMIT 1 ",this_jizhan_number);
     query.exec(cmd);
     memset(cmd,'\0',sizeof(cmd));
     if(query.first())
     {
         qDebug()<<"find one in sql";
          plane_next.xin = query.value(1).toInt();
          plane_next.yin = query.value(2).toInt();
          plane_next.xout = query.value(3).toInt();
          plane_next.yout = query.value(4).toInt();
          plane_next.v = query.value(5).toInt();
          plane_next.plane_number = query.value(6).toInt();
          //删除此条
          sprintf(cmd,"DELETE FROM add_to_area WHERE Plane_number = %d ",plane_next.plane_number);
          query.exec(cmd);
          memset(cmd,'\0',sizeof(cmd));
          return true;
     }

     return false;
 }

 void Console::sql_delete(int plane_number)
 {
     if(plane_number>=0)
     {
         QSqlQuery query(db);
         sprintf(cmd,"INSERT INTO delete_table (DeleteID) VALUES(%d);",plane_number);
         qDebug()<<cmd<<endl;
         query.exec(cmd);
         memset(cmd,'\0',sizeof(cmd));
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
  /*  //L型障碍
    for(unsigned int i =0 ;i<msizex;i++)
    {
        for(unsigned int j = 0;j < msizey;j++)
        {
            if(i >5 && i<15 && j ==10)
                map[i][j] = 1;
        }
    }

    map[9][3]=3;//常年风暴
*/
    //5-stones
    for(int ii =0 ;ii<msizex;ii++)
    {
        for(int jj =0;jj<msizey;jj++)
        {
            //
            if((ii>3&&ii<7&&jj>3&&jj<7)||(ii>11&&ii<13&&jj>11&&jj<13)||(ii>17&&ii<21&&jj>17&&jj<21)||(ii>17&&ii<21&&jj>3&&jj<7)||(ii>3&&ii<7&&jj>17&&jj<21))
                map[ii][jj] = 1;
        }
    }


    fresh_map_air_stones();
 }


 bool Console::refresh_path_time(vector<float_Point *> &path, int t_start, int v)
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
            // p->t = t_start + 0.5 + jishu/v;
             p->t = t_start + (float)((int)(jishu%v))/v + jishu/v;
        }
        jishu ++;
    }

    return true;
 }



 bool Console::createHurricane(Point a, int delta_t, int radius)
 {
     // Get into hurricane_status
     Hurricane *new_hurricane = new Hurricane();
     new_hurricane->initHurricane(a.x, a.y, radius, time+delta_t);
     hurricane_status.push_back(new_hurricane);

     qDebug()<<"Coming is hurricane!!!!";
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
         if(hurricane_status[i]->end_time>time)
         {
             continue;
         }
         // end_time == time
         // save the index whose hurricane need to be delete
         delete_list.push_back(i);
         for(m=0;m<(2*hurricane_status[i]->radius+2);m++)
         {
             for(n=0;n<(2*hurricane_status[i]->radius+2);n++)
             {
                 deleteMapPoint(hurricane_status[i]->x-hurricane_status[i]->radius+m, hurricane_status[i]->y-hurricane_status[i]->radius+n, 3);
             }
         }
     }

     // remove from the hurricane status.
     int delete_num;
     delete_num = delete_list.size();
     for(i=0;i<delete_num;i++)
     {
         delete(hurricane_status[delete_num-1-i]);
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
          planes_status[ii]->index_now += planes_status[ii]->v;
          if(planes_status[ii]->index_now<planes_status[ii]->final_path.size())
          {
              planes_status[ii]->xnow = planes_status[ii]->final_path[planes_status[ii]->index_now]->x;
              planes_status[ii]->ynow = planes_status[ii]->final_path[planes_status[ii]->index_now]->y;
          }
          else//飞机飞出区域,则删除
          {
              delete_plane_list.push_back(ii);
              //把删除的飞机加入sql
              sql_delete(planes_status[ii]->plane_number);

          }
     }

     for(int ii=0;ii<delete_plane_list.size();ii++)
     {

         ////////////////////////
         //先删飞机内部的指针数组：
           ins1.fclearRAM(planes_status[delete_plane_list[delete_plane_list.size()-1-ii]]->final_path);
           delete(planes_status[delete_plane_list[delete_plane_list.size()-1-ii]]->label);
         //再删飞机指针内存
         delete(planes_status[delete_plane_list[delete_plane_list.size()-1-ii]]);

         planes_status.erase(planes_status.begin()+delete_plane_list[delete_plane_list.size()-1-ii]);
     }
 }

 void Console::movePlane(int t,int pieces_num)
 {
     int move_distance;
     float delta_x =0 ;
     float delta_y =0;
     float temp_x =0;
     float temp_y =0;
     float angle_float = 0;
    for(int ii = 0;ii<planes_status.size();ii++)
    {
        move_distance = t * planes_status[ii]->v;
        //if can move
        if(1 + planes_status[ii]->index_now + move_distance/pieces_num < planes_status[ii]->final_path.size())
        {
            temp_x = planes_status[ii]->xnow;
            temp_y = planes_status[ii]->ynow;

            planes_status[ii]->xnow = planes_status[ii]->final_path[planes_status[ii]->index_now + move_distance/pieces_num]->x + (float)(planes_status[ii]->final_path[1 + planes_status[ii]->index_now + move_distance/pieces_num]->x - planes_status[ii]->final_path[planes_status[ii]->index_now + move_distance/pieces_num]->x)*(move_distance%pieces_num)/pieces_num;
            planes_status[ii]->ynow = planes_status[ii]->final_path[planes_status[ii]->index_now + move_distance/pieces_num]->y + (float)(planes_status[ii]->final_path[1 + planes_status[ii]->index_now + move_distance/pieces_num]->y - planes_status[ii]->final_path[planes_status[ii]->index_now + move_distance/pieces_num]->y)*(move_distance%pieces_num)/pieces_num;

           // delta_x = planes_status[ii]->final_path[1+planes_status[ii]->index_now + move_distance/pieces_num]->x - planes_status[ii]->final_path[planes_status[ii]->index_now + move_distance/pieces_num]->x;
            //delta_y = planes_status[ii]->final_path[1+planes_status[ii]->index_now + move_distance/pieces_num]->y - planes_status[ii]->final_path[planes_status[ii]->index_now + move_distance/pieces_num]->y;
            delta_x =   planes_status[ii]->xnow - temp_x;//横坐标变化量
            delta_y =   planes_status[ii]->ynow - temp_y;//纵坐标变化量

            angle_float = atan2(delta_y,delta_x);//计算前进方向角度
            planes_status[ii] -> direction_f = (angle_float)*180/3.1415926;//赋给浮点方向,-180度到+180度

//            if(delta_x == 0)
//            {
//                if(delta_y>0)
//                    planes_status[ii]->direction = 4;//y轴正方向
//                else
//                    planes_status[ii]->direction = 0;//y轴负方向
//            }
//            else if(delta_y == 0)
//            {
//                if(delta_x>0)
//                    planes_status[ii]->direction = 2;//x轴正方向
//                else
//                    planes_status[ii]->direction = 6;//x轴负方向

//            }
//            else if((delta_x>0 && delta_y >0)||(delta_x<0 && delta_y <0))
//            {
//                if(delta_y>0)
//                    planes_status[ii]->direction = 3;//45度
//                else
//                    planes_status[ii]->direction = 7;//225度

//            }
//            else
//            {
//                if(delta_y>0)
//                    planes_status[ii]->direction = 5;//135度
//                else
//                    planes_status[ii]->direction = 1;//315度

//            }

        }

    }
 }

