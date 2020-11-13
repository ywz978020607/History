#include "widget.h"


using namespace std;

const int qt_x = int(qt_map_y/msizex);
const int qt_y = int(qt_map_y/msizey);

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    init();
}

Widget::~Widget()
{

}

/////////////////////////////
// private function
//Event_paint
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    QRect rec_bg(QPoint(0,0),QPoint(this->height(),this->height()));
   // qDebug()<<this->width()<<","<<this->height();


    for(int ii =0;ii<msizex;ii++)
    {
        for(int jj =0;jj<msizey;jj++)
        {
            if(console.map[ii][jj] == 1)
                 painter.drawPixmap(xiangsu_xy(ii),xiangsu_xy(jj),qt_x,qt_y,pix_Stones);
            else if(console.map[ii][jj] == 3||console.map[ii][jj] == 4)
                painter.drawPixmap(xiangsu_xy(ii),xiangsu_xy(jj),qt_x,qt_y,pix_wind);

        }
    }
}
void Widget::mouseMoveEvent(QMouseEvent *event)
{
    int x = dexiangsu_xy(event->pos().x());
    int y = dexiangsu_xy(event->pos().y());
    QString str ="坐标：("+QString::number(x)+","+QString::number(y)+")";
    qt_poslabel->setText(str);
}


void Widget::init()
{
    qDebug()<<qt_x;
    input_hurricane = 0;
    input_plane = 0;

    //QPixmap pix("");
    pix_Stones = QPixmap("../block.png");
    pix_wind = QPixmap("../storm.png");
    pix_plane = QPixmap("../plane_1.png");//图片路径
    pix_plane2 = QPixmap("../plane_2.png");


    gridlayout -> setColumnStretch(0,4);
    gridlayout -> setColumnStretch(1,4);
    gridlayout -> setColumnStretch(2,4);
    gridlayout -> setColumnStretch(3,4);
    gridlayout -> setColumnStretch(4,4);
    gridlayout -> addWidget(qt_title_1,0,14);
    gridlayout -> addWidget(qt_Editx_start,1,14);
    gridlayout -> addWidget(qt_title_x_s,1,13);
    gridlayout -> addWidget(qt_title_y_s,2,13);
    gridlayout -> addWidget(qt_Edity_start,2,14);
    gridlayout -> addWidget(qt_title_2,3,14);
    gridlayout -> addWidget(qt_Editx_end,4,14);
    gridlayout -> addWidget(qt_Edity_end,5,14);
    gridlayout -> addWidget(qt_title_x_e,4,13);
    gridlayout -> addWidget(qt_title_y_e,5,13);
    gridlayout -> addWidget(qt_title_3,6,14);
    gridlayout -> addWidget(qt_Edit_speed,7,14);
    gridlayout -> addWidget(qt_button1,8,14);
    gridlayout -> addWidget(qt_title_4,9,14);
    gridlayout -> addWidget(qt_Editx_storm,10,14);
    gridlayout -> addWidget(qt_Edity_storm,11,14);
    gridlayout -> addWidget(qt_title_x_storm,10,13);
    gridlayout -> addWidget(qt_title_y_storm,11,13);
    gridlayout -> addWidget(qt_title_5,12,14);
    gridlayout -> addWidget(qt_Editt_storm,13,14);
    gridlayout -> addWidget(qt_title_6,14,14);
    gridlayout -> addWidget(qt_Editr_storm,15,14);
    gridlayout -> addWidget(qt_button2,16,14);
   // gridlayout -> addWidget(qt_pos_label_ex,17,13);
    gridlayout -> addWidget(qt_poslabel,17,14);
    qt_poslabel -> resize(10,30);
    this -> setLayout(gridlayout);

   // QLabel * show_start = new QLabel(this);

    for(int jj =0;jj<8;jj++)
    {
        leftmatrix[jj].rotate(45*jj);
    }
    //风暴持续时间
    myTimer = new QTimer(this);
    myTimer->start(100);
    connect(myTimer,SIGNAL(timeout()),this,SLOT(FlashTimerout()));//连接Timer的槽
    ///////////
    connect(qt_button1,SIGNAL(clicked(bool)),this,SLOT(plane_input()));
    connect(qt_button2,SIGNAL(clicked(bool)),this,SLOT(hurricane_input()));
///////////////////////////////////////////////////////////////////////////////////////////////////
    console.Init_map();
    console.initsql();
    // init time.
    console.time = 0;

    time_count = 0;
    time_count_max = 5 ;//分几步走，也是最大速度

    setMouseTracking(true);//实时跟踪鼠标
    update();
}
///////////////////////
void Widget::plane_input()
{
    input_plane = 1;
    editx_s = qt_Editx_start -> text().toInt();   // QPushButton *QPushButton2
    edity_s = qt_Edity_start -> text().toInt();
    editx_e = qt_Editx_end -> text().toInt();
    edity_e = qt_Edity_end -> text().toInt();
    edit_v = qt_Edit_speed->text().toInt();
}
void Widget::hurricane_input()
{
    input_hurricane = 1;
    editx_storm = qt_Editx_storm->text().toInt();
    edity_storm = qt_Edity_storm->text().toInt();
    edit_time = qt_Editt_storm->text().toInt();
    editr_storm = qt_Editr_storm->text().toInt();
}
//鼠标时间
void Widget::mousePressEvent(QMouseEvent * event)
{
    static int flag_plane = 0;
    static int flag_hurricane = 0;

    static int start_x;
    static int start_y;

    if(event->button()==Qt::LeftButton)
    {
        //加入飞机
    if(flag_plane == 0)
    {
        start_x = dexiangsu_xy(event->pos().x());
        start_y = dexiangsu_xy(event->pos().y());
        //show_start->setPixmap(pix_plane);
        //show_start->setGeometry(xiangsu_xy(start_x),xiangsu_xy(start_y),40,40);
        //show_start->show();
        flag_plane++;
    }
    else
    {

        flag_plane = 0;
        input_plane = 1;
        editx_s = start_x;
        edity_s = start_y;
        editx_e = dexiangsu_xy(event->pos().x());
        edity_e = dexiangsu_xy(event->pos().y());
        edit_v = 1;
    }


    }
    else if(event->button()==Qt::RightButton)
    {
    if(flag_hurricane == 0)
    {

    }
        //加入飓风
        input_hurricane = 1;
        editx_storm = dexiangsu_xy(event->pos().x());
        edity_storm = dexiangsu_xy(event->pos().y());
        edit_time = qt_Editt_storm->text().toInt();
        editr_storm = qt_Editr_storm->text().toInt();
    }
}

int Widget::xiangsu_xy(float x)
{
    return (int)(x*qt_x);
}

int Widget::dexiangsu_xy(float x)
{
    return (int)(x/qt_x);
}

void Widget::FlashTimerout() //主函数loop_main
{
    myTimer->stop();
    time_count++;
    if(time_count >= time_count_max)
    {
        console.time++;
        console.deleteHurricane();

        //Hurricane
        if(input_hurricane)
        {
            input_hurricane = 0;
            Point a(editx_storm,edity_storm);

            console.createHurricane(a,edit_time,editr_storm);
            console.refreshAllPath();
        }

        //create new plane
        else if(input_plane)
        {
            input_plane = 0;
            Point start(editx_s,edity_s);
            Point end(editx_e,edity_e);
            if(console.map[start.x][start.y] != 0 || console.map[end.x][end.y] != 0)
            {
                qDebug()<<"can't be stone start/end.";
            }
            else if(!console.createNewPlane(start,end,edit_v,-1))//-1为小区域飞机
            {
                qDebug()<<editx_s<<","<<editx_e<<"Wait for creat the new plane.";
            }
            else
            {
                console.planes_status[console.planes_status.size()-1]->label = new QLabel(this);
            }
        }
        else if(console.sql_add()){
            Point start(console.plane_next.xin,console.plane_next.yin);
            Point end(console.plane_next.xout,console.plane_next.yout);
            if(console.map[start.x][start.y] != 0 || console.map[end.x][end.y] != 0)
            {
                qDebug()<<"can't be stone start/end.";
            }
            else if(!console.createNewPlane(start,end,console.plane_next.v,console.plane_next.plane_number))
            {
                qDebug()<<editx_s<<","<<editx_e<<"Wait for creat the new plane.";
            }
            else
            {
                console.planes_status[console.planes_status.size()-1]->label = new QLabel(this);
            }
        }
        //检查是否停止的飞机可以移动
        console.StopToMove();

        //显示更新以及飞机到达出队
        console.refreshPlane();

        //更新map
        update();

        time_count = 0;//重新计数
    }
    else
    {
        console.movePlane(time_count,time_count_max);
    }


   // qDebug()<<console.planes_status.size();


    //更新飞机
    for(int ii =0;ii<console.planes_status.size();ii++)
    {
        //选择正向图片
        bool qt_judge_1 = abs(console.planes_status[ii] -> direction_f) <= 22.5;//-22.5度到22.5度
        bool qt_judge_2 = abs(abs(console.planes_status[ii] -> direction_f) - 90) <= 22.5;//90-22.5度到90+22.5度
        bool qt_judge_3 = abs(abs(console.planes_status[ii] -> direction_f) -180) <= 22.5;//180-22.5度到180度

        if(qt_judge_1 || qt_judge_2 || qt_judge_3)//-22.5度到22.5度
        {
            //cw_matrix
            cw_matrix.rotate(console.planes_status[ii] -> direction_f);
            //qDebug()<<"旋转角度为"<<console.planes_status[ii] -> direction_f;
           // pix_plane = pix_plane.transformed(cw_matrix,Qt::SmoothTransformation).scaled(qt_x,qt_y, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            console.planes_status[ii] -> label -> setPixmap(pix_plane.transformed(cw_matrix,Qt::SmoothTransformation).scaled(qt_x,qt_y, Qt::IgnoreAspectRatio, Qt::SmoothTransformation));
            cw_matrix.rotate(-(console.planes_status[ii] -> direction_f));
        }
        //
        else //if(console.planes_status[ii] -> direction_f >=(-180+45));


        {
            cw_matrix.rotate((console.planes_status[ii] -> direction_f)-45);
            //qDebug()<<"旋转角度"<<console.planes_status[ii] -> direction_f-45;
            //pix_plane2 = pix_plane2.transformed(cw_matrix, Qt::Transformation).scaled(qt_x,qt_y, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            console.planes_status[ii] -> label -> setPixmap(pix_plane2.transformed(cw_matrix, Qt::SmoothTransformation).scaled(qt_x,qt_y, Qt::IgnoreAspectRatio, Qt::SmoothTransformation));
            cw_matrix.rotate(-((console.planes_status[ii] -> direction_f)-45));
        }


//        if( console.planes_status[ii]->direction % 2 == 0)//90度
//            console.planes_status[ii]->label->setPixmap(pix_plane.transformed(leftmatrix[console.planes_status[ii]->direction],Qt::SmoothTransformation).scaled(qt_x,qt_y, Qt::IgnoreAspectRatio, Qt::SmoothTransformation));
//        else
//            console.planes_status[ii]->label->setPixmap(pix_plane2.transformed(leftmatrix[console.planes_status[ii]->direction - 1],Qt::SmoothTransformation).scaled(qt_x,qt_y, Qt::IgnoreAspectRatio, Qt::SmoothTransformation));


        console.planes_status[ii]->label->setGeometry(xiangsu_xy(console.planes_status[ii]->xnow),xiangsu_xy(console.planes_status[ii]->ynow),qt_x,qt_y);
        console.planes_status[ii]->label->show();

        //旋转浮点数角度；
        //qDebug()<<console.planes_status[ii]->xnow<<","<<console.planes_status[ii]->ynow;
    }




    myTimer->start(100);
}

