#ifndef WIDGET_H
#define WIDGET_H

#include"console.h"
#include <QWidget>
#include<QPainter>
#include<Qt>
#include<QResizeEvent>
#include<QDebug>
#include<QGridLayout>
#include<QPushButton>
#include<QLineEdit>
#include<QTimer>
#include<QMouseEvent>
#include <QApplication>
#include <QLayout>
#include <QLabel>
#include <QPainter>
#include <QLineEdit>
#include <iostream>
#define GridCount 10
#define qt_map_x 1300
#define qt_map_y 1000

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = 0);
    ~Widget();

protected:
   void paintEvent(QPaintEvent *);
   void mouseMoveEvent(QMouseEvent *);
   void mousePressEvent(QMouseEvent *);
public slots:
   void plane_input();
   void hurricane_input();
   void FlashTimerout();
private:
    void init();
    void show_map();
    void show_planes();
    int xiangsu_xy(float x);
    int dexiangsu_xy(float x);

    QTimer *myTimer;

   // QLabel *label = new QLabel(this);

    int time_count;
    int time_count_max;

    int input_plane;
    int input_hurricane;

    Console console;


    int editx_s,edity_s,editx_e,edity_e,edit_v;
    int editx_storm,edity_storm,editr_storm,edit_time;

    QPixmap pix_bg;
    QPixmap pix_Stones;
    QPixmap pix_wind;
    QPixmap pix_plane;
    QPixmap pix_plane2;

    //QLabel *show_start;

    QMatrix leftmatrix[8];
    QMatrix cw_matrix;
    QMatrix acw_matrix;
    QGridLayout *gridlayout = new QGridLayout(this);
    QLineEdit *qt_Editx_start = new QLineEdit(this);
    QLineEdit *qt_Edity_start = new QLineEdit(this);
    QPushButton *qt_button1 = new QPushButton("加入飞机");
    QLabel *qt_title_1 = new QLabel(QWidget::tr("起点坐标"));
    QLabel *qt_title_2 = new QLabel(QWidget::tr("终点坐标"));
    QLabel *qt_title_x_s = new QLabel(QWidget::tr("x"));
    QLabel *qt_title_y_s = new QLabel(QWidget::tr("y"));
    QLineEdit *qt_Editx_end = new QLineEdit(this);
    QLineEdit *qt_Edity_end = new QLineEdit(this);
    QLabel *qt_title_x_e = new QLabel(QWidget::tr("x"));
    QLabel *qt_title_y_e = new QLabel(QWidget::tr("y"));
    QLabel *qt_title_3 = new QLabel(QWidget::tr("飞行速度"));
    QLineEdit *qt_Edit_speed = new QLineEdit(this);
    QLabel *qt_title_4 = new QLabel(QWidget::tr("飓风中心"));
    QLineEdit *qt_Editx_storm = new QLineEdit(this);
    QLineEdit *qt_Edity_storm = new QLineEdit(this);
    QLabel *qt_title_x_storm = new QLabel(QWidget::tr("x"));
    QLabel *qt_title_y_storm = new QLabel(QWidget::tr("y"));
    QLabel *qt_title_5 = new QLabel(QWidget::tr("飓风时间"));
    QLineEdit *qt_Editt_storm = new QLineEdit(this);
    QLabel *qt_title_6 = new QLabel(QWidget::tr("飓风半径"));
    QLineEdit *qt_Editr_storm = new QLineEdit(this);
    QPushButton *qt_button2 = new QPushButton("加入飓风");
    QLabel *qt_poslabel = new QLabel;

};

#endif // WIDGET_H
