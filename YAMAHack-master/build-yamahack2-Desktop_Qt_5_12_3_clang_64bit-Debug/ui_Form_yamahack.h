/********************************************************************************
** Form generated from reading UI file 'Form_yamahack.ui'
**
** Created by: Qt User Interface Compiler version 5.12.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FORM_YAMAHACK_H
#define UI_FORM_YAMAHACK_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLCDNumber>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollBar>
#include <QtWidgets/QSlider>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Form_yamahack
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout_2;
    QVBoxLayout *verticalLayout;
    QLCDNumber *lcdNumber_speedLeft;
    QHBoxLayout *horizontalLayout;
    QSlider *verticalSlider_setLeft;
    QLCDNumber *lcdNumber;
    QLabel *label;
    QVBoxLayout *verticalLayout_2;
    QLCDNumber *lcdNumber_3;
    QLCDNumber *lcdNumber_4;
    QSpacerItem *verticalSpacer;
    QGridLayout *gridLayout;
    QPushButton *pushButton_connect;
    QPushButton *pushButton_disconnect;
    QPushButton *pushButton;
    QPushButton *pushButton_2;
    QVBoxLayout *verticalLayout_4;
    QHBoxLayout *horizontalLayout_3;
    QLabel *label_4;
    QScrollBar *horizontalScrollBar_setAcl;
    QLabel *label_5;
    QLabel *label_2;
    QVBoxLayout *verticalLayout_3;
    QLCDNumber *lcdNumber_speedRight;
    QHBoxLayout *horizontalLayout_2;
    QSlider *verticalSlider_setRight;
    QLCDNumber *lcdNumber_2;
    QLabel *label_3;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *Form_yamahack)
    {
        if (Form_yamahack->objectName().isEmpty())
            Form_yamahack->setObjectName(QString::fromUtf8("Form_yamahack"));
        Form_yamahack->resize(440, 361);
        centralWidget = new QWidget(Form_yamahack);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout_2 = new QGridLayout(centralWidget);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(3);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        lcdNumber_speedLeft = new QLCDNumber(centralWidget);
        lcdNumber_speedLeft->setObjectName(QString::fromUtf8("lcdNumber_speedLeft"));
        lcdNumber_speedLeft->setMinimumSize(QSize(0, 30));
        lcdNumber_speedLeft->setSmallDecimalPoint(false);
        lcdNumber_speedLeft->setDigitCount(5);
        lcdNumber_speedLeft->setSegmentStyle(QLCDNumber::Flat);
        lcdNumber_speedLeft->setProperty("intValue", QVariant(0));

        verticalLayout->addWidget(lcdNumber_speedLeft);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(0);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        verticalSlider_setLeft = new QSlider(centralWidget);
        verticalSlider_setLeft->setObjectName(QString::fromUtf8("verticalSlider_setLeft"));
        verticalSlider_setLeft->setMinimum(-10000);
        verticalSlider_setLeft->setMaximum(10000);
        verticalSlider_setLeft->setPageStep(2);
        verticalSlider_setLeft->setValue(0);
        verticalSlider_setLeft->setSliderPosition(0);
        verticalSlider_setLeft->setTracking(true);
        verticalSlider_setLeft->setOrientation(Qt::Vertical);
        verticalSlider_setLeft->setInvertedAppearance(false);
        verticalSlider_setLeft->setInvertedControls(false);
        verticalSlider_setLeft->setTickPosition(QSlider::TicksBothSides);
        verticalSlider_setLeft->setTickInterval(300);

        horizontalLayout->addWidget(verticalSlider_setLeft);


        verticalLayout->addLayout(horizontalLayout);

        lcdNumber = new QLCDNumber(centralWidget);
        lcdNumber->setObjectName(QString::fromUtf8("lcdNumber"));
        lcdNumber->setMinimumSize(QSize(0, 30));

        verticalLayout->addWidget(lcdNumber);

        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setAlignment(Qt::AlignCenter);

        verticalLayout->addWidget(label);


        gridLayout_2->addLayout(verticalLayout, 0, 0, 1, 1);

        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        lcdNumber_3 = new QLCDNumber(centralWidget);
        lcdNumber_3->setObjectName(QString::fromUtf8("lcdNumber_3"));

        verticalLayout_2->addWidget(lcdNumber_3);

        lcdNumber_4 = new QLCDNumber(centralWidget);
        lcdNumber_4->setObjectName(QString::fromUtf8("lcdNumber_4"));

        verticalLayout_2->addWidget(lcdNumber_4);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_2->addItem(verticalSpacer);

        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        pushButton_connect = new QPushButton(centralWidget);
        pushButton_connect->setObjectName(QString::fromUtf8("pushButton_connect"));

        gridLayout->addWidget(pushButton_connect, 0, 0, 1, 1);

        pushButton_disconnect = new QPushButton(centralWidget);
        pushButton_disconnect->setObjectName(QString::fromUtf8("pushButton_disconnect"));

        gridLayout->addWidget(pushButton_disconnect, 1, 0, 1, 1);

        pushButton = new QPushButton(centralWidget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));

        gridLayout->addWidget(pushButton, 1, 1, 1, 1);

        pushButton_2 = new QPushButton(centralWidget);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));

        gridLayout->addWidget(pushButton_2, 0, 1, 1, 1);


        verticalLayout_2->addLayout(gridLayout);

        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setSpacing(0);
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setSpacing(6);
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setMaximumSize(QSize(25, 16777215));

        horizontalLayout_3->addWidget(label_4);

        horizontalScrollBar_setAcl = new QScrollBar(centralWidget);
        horizontalScrollBar_setAcl->setObjectName(QString::fromUtf8("horizontalScrollBar_setAcl"));
        horizontalScrollBar_setAcl->setMaximum(100);
        horizontalScrollBar_setAcl->setValue(20);
        horizontalScrollBar_setAcl->setOrientation(Qt::Horizontal);

        horizontalLayout_3->addWidget(horizontalScrollBar_setAcl);

        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setMaximumSize(QSize(25, 16777215));

        horizontalLayout_3->addWidget(label_5);


        verticalLayout_4->addLayout(horizontalLayout_3);

        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setAlignment(Qt::AlignCenter);

        verticalLayout_4->addWidget(label_2);


        verticalLayout_2->addLayout(verticalLayout_4);


        gridLayout_2->addLayout(verticalLayout_2, 0, 1, 1, 1);

        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setSpacing(3);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        lcdNumber_speedRight = new QLCDNumber(centralWidget);
        lcdNumber_speedRight->setObjectName(QString::fromUtf8("lcdNumber_speedRight"));
        lcdNumber_speedRight->setMinimumSize(QSize(0, 30));
        QFont font;
        font.setPointSize(15);
        font.setBold(false);
        font.setWeight(50);
        lcdNumber_speedRight->setFont(font);
        lcdNumber_speedRight->setAutoFillBackground(false);
        lcdNumber_speedRight->setStyleSheet(QString::fromUtf8(""));
        lcdNumber_speedRight->setFrameShape(QFrame::Box);
        lcdNumber_speedRight->setFrameShadow(QFrame::Raised);
        lcdNumber_speedRight->setLineWidth(1);
        lcdNumber_speedRight->setMidLineWidth(0);
        lcdNumber_speedRight->setSmallDecimalPoint(false);
        lcdNumber_speedRight->setDigitCount(5);
        lcdNumber_speedRight->setSegmentStyle(QLCDNumber::Flat);

        verticalLayout_3->addWidget(lcdNumber_speedRight);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        verticalSlider_setRight = new QSlider(centralWidget);
        verticalSlider_setRight->setObjectName(QString::fromUtf8("verticalSlider_setRight"));
        verticalSlider_setRight->setMinimum(-10000);
        verticalSlider_setRight->setMaximum(10000);
        verticalSlider_setRight->setPageStep(2);
        verticalSlider_setRight->setOrientation(Qt::Vertical);
        verticalSlider_setRight->setTickInterval(300);

        horizontalLayout_2->addWidget(verticalSlider_setRight);


        verticalLayout_3->addLayout(horizontalLayout_2);

        lcdNumber_2 = new QLCDNumber(centralWidget);
        lcdNumber_2->setObjectName(QString::fromUtf8("lcdNumber_2"));
        lcdNumber_2->setMinimumSize(QSize(0, 30));

        verticalLayout_3->addWidget(lcdNumber_2);

        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setAlignment(Qt::AlignCenter);

        verticalLayout_3->addWidget(label_3);


        gridLayout_2->addLayout(verticalLayout_3, 0, 2, 1, 1);

        Form_yamahack->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(Form_yamahack);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 440, 22));
        Form_yamahack->setMenuBar(menuBar);
        mainToolBar = new QToolBar(Form_yamahack);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        Form_yamahack->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(Form_yamahack);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        Form_yamahack->setStatusBar(statusBar);

        retranslateUi(Form_yamahack);
        QObject::connect(verticalSlider_setRight, SIGNAL(valueChanged(int)), lcdNumber_2, SLOT(display(int)));
        QObject::connect(verticalSlider_setLeft, SIGNAL(valueChanged(int)), lcdNumber, SLOT(display(int)));

        QMetaObject::connectSlotsByName(Form_yamahack);
    } // setupUi

    void retranslateUi(QMainWindow *Form_yamahack)
    {
        Form_yamahack->setWindowTitle(QApplication::translate("Form_yamahack", "MainWindow", nullptr));
        label->setText(QApplication::translate("Form_yamahack", "Left wheel", nullptr));
        pushButton_connect->setText(QApplication::translate("Form_yamahack", "connect", nullptr));
        pushButton_disconnect->setText(QApplication::translate("Form_yamahack", "disconnect", nullptr));
        pushButton->setText(QApplication::translate("Form_yamahack", "Rand Pack", nullptr));
        pushButton_2->setText(QApplication::translate("Form_yamahack", "spark", nullptr));
        label_4->setText(QApplication::translate("Form_yamahack", "min", nullptr));
        label_5->setText(QApplication::translate("Form_yamahack", "max", nullptr));
        label_2->setText(QApplication::translate("Form_yamahack", "Acceleration", nullptr));
        label_3->setText(QApplication::translate("Form_yamahack", "Left wheel", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Form_yamahack: public Ui_Form_yamahack {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FORM_YAMAHACK_H
