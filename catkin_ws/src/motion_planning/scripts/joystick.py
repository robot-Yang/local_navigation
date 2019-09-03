import HighPrecision_ADDA as converter
import time
import heapq
import logging
from logging import handlers


conv = converter.AD_DA()


level_relations = {
        # 'debug':logging.DEBUG,
        'info':logging.INFO,
        # 'warning':logging.WARNING,
        # 'error':logging.ERROR,
        # 'crit':logging.CRITICAL
    }

def log(Command_DAC0, Command_DAC1, filename,level,fmt='%(created).6f %(message)s'):
    logger = logging.getLogger(filename)
    format_str = logging.Formatter(fmt)
    logger.setLevel(level_relations.get(level))
    sh = logging.StreamHandler()
    sh.setFormatter(format_str)
    th = logging.handlers.TimedRotatingFileHandler(filename=filename,encoding='utf-8')
    th.setFormatter(format_str)
    logger.addHandler(sh)
    logger.addHandler(th)
    logger.info("%s %s",Command_DAC0, Command_DAC1)
    logger.removeHandler(sh)
    logger.removeHandler(th)


while True:
     a = conv.ReadChannel(0, conv.data_format.voltage) #forward up/backward down
     b = conv.ReadChannel(1, conv.data_format.voltage) #left up/right down
    # c = conv.ReadChannel(7, conv.data_format.voltage)
    # print u"1: qrcode create"
    # print u"2: qrcode identify"
    # print u"3: exit"
    # select=int(raw_input(u"please choose: "))
    # if select == 1:
        # qrcode.erzeugen()
    # elif select == 2:
        # result=qrcode.lesen().strip()
       # result1= result.encode("utf-8")
        # print result
        # result1=result.split()
    # elif select == 3:
        # print u"programme completed..."
        # break

    # conv.SET_DAC0(int(result1[0]), conv.data_format.voltage)
    # conv.SET_DAC1(int(result1[1]), conv.data_format.voltage)
     conv.SET_DAC0(a, conv.data_format.voltage)
     conv.SET_DAC1(b, conv.data_format.voltage)

     Command_DAC0, Command_DAC1 = str(a), str(b)
     Command_DAC0, Command_DAC1 = Command_DAC0.ljust(8), Command_DAC1.ljust(8)
     log(Command_DAC0, Command_DAC1, 'info_luis2.log', level='info')

     print (a,b)
     time.sleep(0.1)



