#coding=utf8
# 手机相关的信息
# 手机的行为
# termux基础api的调用
import os
import sys
import json
import traceback
import subprocess
import shlex
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
fmt = '%(asctime)-15s.%(msecs)03d[%(levelname)s]{%(filename)s,%(lineno)d} %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt, datefmt)
# file_handler = RotatingFileHandler("./logs/update.log", 'w', 100000000, 2)
# file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

"""
"termux-battery-status"     
"termux-download"
"termux-notification-remove"
"termux-sms-send"  
"termux-tts-speak"
"termux-camera-info"           
"termux-fix-shebang"          
"termux-open"          
"termux-storage-get"           
"termux-vibrate"
"termux-camera-photo"          
"termux-info"         
"termux-open-url"              
"termux-telephony-call"        
"termux-wake-lock"
"termux-clipboard-get"         
"termux-infrared-frequencies"  
"termux-reload-settings" 
"termux-telephony-cellinfo"    
"termux-wake-unlock"
"termux-clipboard-set"       
"termux-infrared-transmit"   
"termux-setup-storage"        
"termux-telephony-deviceinfo" 
"termux-wifi-connectioninfo"
"termux-contact-list"          
"termux-location"             
"termux-share"                
"termux-toast"                 
"termux-wifi-scaninfo"
"termux-dialog"                
"termux-notification"          
"termux-sms-inbox"             
"termux-tts-engines" 
"""
termux_temp_str  = """\
termux-battery-status        termux-download              termux-notification-remove   termux-sms-send              termux-tts-speak
termux-camera-info           termux-fix-shebang           termux-open                  termux-storage-get           termux-vibrate
termux-camera-photo          termux-info                  termux-open-url              termux-telephony-call        termux-wake-lock
termux-clipboard-get         termux-infrared-frequencies  termux-reload-settings       termux-telephony-cellinfo    termux-wake-unlock
termux-clipboard-set         termux-infrared-transmit     termux-setup-storage         termux-telephony-deviceinfo  termux-wifi-connectioninfo
termux-contact-list          termux-location              termux-share                 termux-toast                 termux-wifi-scaninfo
termux-dialog                termux-notification          termux-sms-inbox             termux-tts-engines  
"""
# print(termux_temp_str.split())
res = [temp.replace('-','_').replace('termux_','') for temp in termux_temp_str.split()]
print(res)
from collections import namedtuple
TermuxCmd = namedtuple('api',res)
print(namedtuple)
termux_cmd = TermuxCmd(*termux_temp_str.split())
print(termux_cmd.camera_info)
# print(termux.camera_info)
# def action(func):
#     def inner(*args,**kwargs):
#         pass
#     return inner

# def vibrate(duration=1000,force=True):
#     res = {
#         'cmd': 1
#     }
#     return res

class DictObj(object):
    def __init__(self):
        pass
    pass


class _CacheAtrr(object):
    '''
    the class used to chche attr values
    '''
    def __init__(self, termux_cmd, cache = True):
        self.is_cache = cache
        self._cmd = termux_cmd
        self.dict_info = None
        pass
    def __set__(self, ins, val):
        pass
    def __get__(self, ins, owner):
        print(ins)
        print(owner)
        self.exe_cmd()
        return self.dict_info
        pass
    def exe_cmd(self):
        try:
            if not self.is_cache:
                res = os.popen(self._cmd).read()
                self.dict_info = json.loads(res)
                print(self.dict_info)
            else:
                if self.dict_info is None:
                    res = os.popen(self._cmd).read()
                    self.dict_info = json.loads(res)
                    print(self.dict_info)
        except Exception as e:
            print(e)

class Termux(object):
    battery_status = _CacheAtrr(termux_cmd.battery_status, cache=False)
    location = _CacheAtrr(termux_cmd.location, cache=False)
    camera_info = _CacheAtrr(termux_cmd.camera_info)
    contact_list = _CacheAtrr(termux_cmd.contact_list)
    # info = CacheAtrr(termux_cmd.info)
    telephony_cellinfo = _CacheAtrr(termux_cmd.telephony_cellinfo)
    telephony_deviceinfo = _CacheAtrr(termux_cmd.telephony_deviceinfo)
    tts_engines = _CacheAtrr(termux_cmd.tts_engines)
    wifi_connection_info = _CacheAtrr(termux_cmd.wifi_connectioninfo)

    def __exec(self, cmd):
        try:
            args = shlex.split(cmd)
            print(args)
            pro = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = pro.communicate()
            assert pro.returncode == 0, 'the return num for script is not equal 0, bu %s, something wrong' % pro.returncode
            # res = pro.stdout.read()
            
            return out if out else pro.returncode
        except OSError as e:
            logger.error('execute a program that is not exist :%s\n%s' %
                        (cmd, e.child_traceback))
        except ValueError as e:
            logger.error('call Popen() with wrong args %s' % e)
        except subprocess.CalledProcessError as e:
            logger.error('sub program :<%s>, return not 0%s' % (cmd, e))
        except Exception as e:
            logger.error(traceback.format_exc())        

    def camera_photo(self,cid,file_path):
        cmd = "{0} -c {1} {2}".format(termux_cmd.camera_photo,cid,file_path) # TODO       
        return self.__exec(cmd)
    
    def clipboard_get(self):
        return self.__exec(termux_cmd.clipboard_get)
            
    def clipboard_set(self, content):
        cmd = "{cmd} {args}".format(cmd=termux_cmd.clipboard_set, args=content)
        return self.__exec(cmd)
    
    def dialog(self,hint=None,multi=False,pwd=False,title=None):
        '''
        Show a text entry dialog.
            -i hint   the input hint to show when the input is empty
            -m        use a textarea with multiple lines instead of a single
            -p        enter the input as a password
            -t title  the title to show for the input prompt
        '''
        cmd_base = termux_cmd.dialog
        hint = '' if hint is None else '-i {}'.format(hint)
        title = '' if title is None else '-t {}'.format(title)
        multi = '-m' if multi else ''
        pwd = '-p' if pwd else ''
        cmd_all = ' '.join([cmd_base,hint,title,multi,pwd])
        return self.__exec(cmd_all)

    def vibrate(self,duration=1000, force=False):
        '''
        Usage: termux-vibrate [-d duration] [-f]
        Vibrate the device.
        -d duration  the duration to vibrate in ms (default:1000)
        -f           force vibration even in silent mode
        '''
        cmd_base = termux_cmd.vibrate
        duration =  "-d {}".format(duration)
        force = "-f " if force else ""
        cmd_all = ' '.join([cmd_base,duration,force])
        return self.__exec(cmd_all)

    

    

        


def main():
    t = Termux()
    # import time
    # time_before = time.time()
    # print(t.battery_status)
    print(t.camera_info)
    # print(t.contact_list)
    # # print(t.info)
    # print(t.location)
    # print(t.telephony_cellinfo)
    # print(t.telephony_deviceinfo)
    # time_end = time.time()
    # print(time_end-time_before)
    # t.camera_photo(2,'b.jpg')
    # print(t.dialog(hint='123',multi=True,pwd=True,title='hohoho'))
    # print(t.vibrate(force=True))


    # time_before = time.time()
    # print(t.battery_status)
    # print(t.camera_info)
    # print(t.contact_list)
    # # print(t.info)
    # print(t.location)
    # print(t.telephony_cellinfo)
    # print(t.telephony_deviceinfo)
    # time_end = time.time()
    # print(time_end-time_before)




if __name__ == "__main__":
    main()    