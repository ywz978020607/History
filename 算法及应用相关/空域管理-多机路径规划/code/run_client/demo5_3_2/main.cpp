#include "widget.h"
#include <QApplication>

int main(int argc, char *argv[])
{

    QApplication a(argc, argv);
    Widget w;
    w.resize(QSize(qt_map_x,qt_map_y));
    w.setWindowTitle(QWidget::tr("Plane base station"));

    w.show();

    return a.exec();
}
