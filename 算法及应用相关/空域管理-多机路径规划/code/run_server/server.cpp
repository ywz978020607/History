#include "server.h"

Server::Server(QWidget *parent)
    : QWidget(parent)
{
    init();
}

Server::~Server()
{
    init();
}

/////////////////////////////


///////////////////
void Server::init()
{
    label1->setText("123456");
    label1->setGeometry(20,20,300,200);
    label1->show();
    button->setText("按钮");
    button->show();
    tcpServer = new QTcpServer;
    tcpSocket = new QTcpSocket;
    newListen();
    connect(tcpServer,SIGNAL(newConnection()),SLOT(acceptConnection()));
    connect(tcpSocket, SIGNAL(error(QAbstractSocket::SocketError)),SLOT(showError(QAbstractSocket::SocketError)));
    connect(button,SIGNAL(clicked(bool)),SLOT(sendMessage()));
}


void Server::sendMessage()  //发送数据
{
    QString textEdit = "111111";
    QString strData = QString::fromLocal8Bit("message");
    QByteArray sendMessage = strData.toLocal8Bit();
    mChat += ("Send " + sendMessage);
    tcpSocket->write(sendMessage);
}

void Server::onReciveData()  //读取数据
{
    QString data = tcpSocket->readAll();
    qDebug()<<data;
    mChat +=("Recv " + data + "\n");
    label1->setText(mChat);
}

void Server::newListen()
{
    if(!tcpServer->listen(QHostAddress::Any,6666))
    {
        qDebug()<<tcpServer->errorString();

        tcpServer->close();
    }
}

void Server::acceptConnection()
{
    tcpSocket = tcpServer->nextPendingConnection();
    connect(tcpSocket,SIGNAL(readyRead()),SLOT(onReciveData()));
}

void Server::showError(QAbstractSocket::SocketError)
{
    qDebug()<<tcpSocket->errorString();
    tcpSocket->close();
}
