#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include<QPainter>
#include<Qt>
#include<QResizeEvent>
#include<qDebug>
#include<vector>
#include<QLabel>
#include<QPushButton>

//=====================
#include<QtNetwork>
#include <QTcpServer>
#include <QTcpSocket>


class Server : public QWidget
{
    Q_OBJECT

public:
    Server(QWidget *parent = 0);
    ~Server();


private:

    QLabel *label1 = new QLabel(this);
    QPushButton *button = new QPushButton(this);
    void init();

private slots:
    void sendMessage(); //发送消息
    void onReciveData();  //接收数据
    void newListen(); //建立tcp监听事件
    void acceptConnection(); //接收客户端连接
    void showError(QAbstractSocket::SocketError); //错误输出

private:
    QTcpSocket *tcpSocket;
    QTcpServer *tcpServer;
    QByteArray mChat;


};

#endif // WIDGET_H
