#ifndef FORM_YAMAHACK_H
#define FORM_YAMAHACK_H

#include <QMainWindow>
#include "YamaHack.h"
#include <QTimer>
namespace Ui {
    class Form_yamahack;
}

class Form_yamahack : public QMainWindow
{
    Q_OBJECT

public:
    explicit Form_yamahack(QWidget *parent = nullptr);
    ~Form_yamahack();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_connect_clicked();

    void on_pushButton_disconnect_clicked();


    void on_verticalSlider_setLeft_valueChanged(int value);

    void on_verticalSlider_setRight_valueChanged(int value);

    void on_verticalSlider_setLeft_sliderMoved(int position);

    void on_horizontalScrollBar_setAcl_valueChanged(int value);

    void slot_update();

    void on_pushButton_2_clicked();

private:
    Ui::Form_yamahack *ui;
    YamaHack *yam;
    QTimer *timer_update;
};

#endif // MAINWINDOW_H
