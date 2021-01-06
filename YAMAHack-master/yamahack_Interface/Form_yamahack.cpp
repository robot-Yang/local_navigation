#include "Form_yamahack.h"
#include "ui_Form_yamahack.h"
#include <QTcpSocket>
#include <iostream>

using namespace std;
Form_yamahack::Form_yamahack(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::Form_yamahack)
{
    ui->setupUi(this);
    yam = new YamaHack("192.168.11.240");
    timer_update = new QTimer(this);
    connect(timer_update, SIGNAL(timeout()),this,SLOT(slot_update()));
    timer_update->start(100);



}

Form_yamahack::~Form_yamahack()
{
    delete ui;
}




void Form_yamahack::slot_update(){
    ui->lcdNumber_speedLeft->display(yam->getSpeedLeft());
    ui->lcdNumber_speedRight->display(yam->getSpeedRight());

    ui->lcdNumber_3->display(yam->getSensorBar1());
    ui->lcdNumber_4->display(yam->getSensorBar2());

}
void Form_yamahack::on_pushButton_clicked()
{

}

void Form_yamahack::on_pushButton_connect_clicked()
{
    yam->connectS();
}

void Form_yamahack::on_pushButton_disconnect_clicked()
{
    yam->dis_connect();
}


void Form_yamahack::on_verticalSlider_setLeft_valueChanged(int value)
{
   yam->setControl(value,ui->verticalSlider_setRight->value(),ui->horizontalScrollBar_setAcl->value());
}

void Form_yamahack::on_verticalSlider_setRight_valueChanged(int value)
{
    yam->setControl(ui->verticalSlider_setLeft->value(),value,ui->horizontalScrollBar_setAcl->value());
}

void Form_yamahack::on_verticalSlider_setLeft_sliderMoved(int position)
{

}

void Form_yamahack::on_horizontalScrollBar_setAcl_valueChanged(int value)
{
    yam->setControl(ui->verticalSlider_setLeft->value(),ui->verticalSlider_setRight->value(),value);
}



void Form_yamahack::on_pushButton_2_clicked()
{
    yam->setspark();
}
