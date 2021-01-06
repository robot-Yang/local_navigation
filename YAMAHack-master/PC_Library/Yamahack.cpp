#include "Yamahack.h"
#include <iostream>
#include <bitset>
using namespace std;
YamaHack::YamaHack(QString ip)
{
    buff = new char(8);
   // tcpsock = new QTcpSocket();
    this->ip = ip;
    sync=1;
    speedLeft = 0;
    speedRight = 0;
    setLeft = 0;
    setRight = 0;
    setAcl = 0;
    SBar1=0;
    SBar2=0;
    prev1=0;
    prev=0;
    SBar=0;
    prev2=0;
    for (int i=0;i<8;i++){
        buff[i]=0;
    }
    connected=0;
    line=1;
    status = 1 ;
}


bool YamaHack::connectS(){
    if (!connected){
        tcpsock = new QTcpSocket();
        tcpsock->connectToHost(ip, 12345);
        connect(tcpsock,SIGNAL(readyRead()),this,SLOT(slotReadyRead()));
        connected=1;
        qDebug() << "Connected";
        setspark();
        return 1;
    }
}

bool YamaHack::dis_connect(){
    if (connected){
        tcpsock->disconnectFromHost();
        disconnect(tcpsock,SIGNAL(readyRead()),this,SLOT(slotReadyRead()));
        delete tcpsock;
        connected=0;
        qDebug() << "Disconnected";
        return 1;
    }
}

void YamaHack::slotDisconnected(){

}
void YamaHack::slotConnected(){
}


void YamaHack::slotReadyRead(){
    codeFlag =0;
    status = 1;
    tcpsock->read(buff,8); //8
    char transmission[6];
    sync = buff[0]+1;
   // cout << QString::number(sync).toStdString() <<endl;
    transmission[0] = sync;
    transmission[1] = *((char*)(&setLeft)+0);
    transmission[2] = *((char*)(&setLeft)+1);
    transmission[3] = *((char*)(&setRight)+0);
    transmission[4] = *((char*)(&setRight)+1);
    transmission[5] = setAcl;
    tcpsock->write(transmission,6);
    codeFlag = buff[1];
    if (codeFlag){
        emit errorFlag();
    }
    speedLeft = *((int16_t*)(buff+2));
    speedRight  = *((int16_t*)(buff+4));
    if (buff[6]==0xFF){  //left code
        status = 2;
    }
    if (buff[7]==0xFF){ //right code
        status= 3;
    }
    uint16_t sb = (uint16_t)buff[6]<<8 | buff[7];
    if (prev==0){ // or sb>=0x00FF
        SBar = sb;
    }else{
        uint16_t mask = prev << 1 | prev | prev >> 1;
        SBar = sb & mask;
    }
    prev = SBar;
    int nom= 0;
    int den=0;
    for (int i=0;i<16;i++){
        nom += ((SBar>>i)&0x01) * (i+1);
        den +=  (SBar>>i)&0x01;
    }
    SBar1 = SBar >> 8;
    SBar2 = SBar & 0xFF;
    DIR = (((float)nom/den)-8.5)/7.0; //value between -one and one
    if (den<2){
        line=0;
        status = 0;
    }
}
float YamaHack::getSpeedLeft(){
    return (float)speedLeft/152.4;
}
float YamaHack::getSpeedRight(){
    return (float)speedRight/152.4;
}

int YamaHack::getDirection(float * dir){
    *dir = DIR;
    return status;
}
uint8_t YamaHack::getSensorBar1(){
    return SBar1;
}
uint8_t YamaHack::getSensorBar2(){
    return SBar2;
}

char YamaHack::getError()
{
    return codeFlag;
}

void YamaHack::setspark(){
    char transmission[]={0x01,0,0,0,0,0};
    tcpsock->write(transmission,6);
}


void YamaHack::setControl(int16_t left, int16_t right, uint8_t acl){
    this->setLeft = left;
    this->setRight = right;
    this->setAcl = acl;
}
