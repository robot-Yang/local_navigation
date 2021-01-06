/*
    bytes
    Send
    0 - sync
    1,2 - left speed
    3,4 - right speed
    5 - acceleration
    6,7,8 -

    Received
    0 - sync
    1,2 - left speed
    3,4 - right speed
    5,6,7,8 - i2c sensors


*/
#ifndef YAMAHACK_H
#define YAMAHACK_H

//#include <QObject>
#include <QTcpSocket>

class YamaHack : public QObject
{
    Q_OBJECT
public:
    YamaHack(QString ip);
    bool connectS();
    bool dis_connect();
    void setControl(int16_t left, int16_t right, uint8_t acl);
    void setspark();
    float getSpeedRight();
    float getSpeedLeft();
    uint8_t getSensorBar1();
    int getDirection(float *dir);
    uint8_t getSensorBar2();
    bool line;
    char getError();
signals:
    void errorFlag();
private:
    bool connected;
    float DIR;
    char codeFlag;
    QTcpSocket *tcpsock;
    QString ip;
    int16_t setLeft,setRight;
    int16_t speedLeft,speedRight;
    uint8_t SBar1;
    uint8_t SBar2;
    uint16_t SBar;
    uint16_t prev;
    uint8_t prev1,prev2;
    uint8_t setAcl;
    uint8_t sync;
    uint8_t status;
    char *buff;
    char *transmission;


public slots:
    void slotReadyRead();
    void slotDisconnected();
    void slotConnected();

};

#endif // YAMAHACK_H
