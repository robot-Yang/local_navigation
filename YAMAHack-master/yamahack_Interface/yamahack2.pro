#-------------------------------------------------
#
# Project created by QtCreator 2019-06-07T23:12:10
#
#-------------------------------------------------

QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = yamahack2
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        Form_yamahack.cpp \
        main.cpp

HEADERS += \
        Form_yamahack.h \
        Yamahack.h

FORMS += \
        Form_yamahack.ui




macx: LIBS += -L$$PWD/./ -lYamaHack

INCLUDEPATH += $$PWD/.
DEPENDPATH += $$PWD/.

macx: PRE_TARGETDEPS += $$PWD/./libYamaHack.a
