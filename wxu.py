"""This module contains my common ultilities functions
    1 create win32 mouse cursor event
    2 config for progressbar, logging
    3 Class: MyTimer
"""
__author__ = 'Weichao Xu'
__version__ = "0.0.1"
__status__ = "Dev"
# ########## imports ##########
import sys, os, re, string, time, logging
import math, numpy, random
import win32api, win32con, win32gui
import progressbar as pb
from ftplib import FTP
import pprint
import psutil
import subprocess

mypbwidgets = ['GLobal: ', pb.Percentage(), pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
loggingfmt = '%(name)-10s|%(asctime)s|%(levelname)8s|  %(message)s'
logging.basicConfig(level=logging.NOTSET, stream=sys.stdout, \
                    format=loggingfmt,
                    datefmt='%m%d-%M%M%S')
l = logging.getLogger(__name__)





# # WIN32API Mouse Click
def click(x, y):
    """ click(x, y): click at (x,y) """
    xx, yy = win32api.GetCursorPos()
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    l.info("(%4d, %4d) --> (%4d, %4d) clicked" % (xx, yy, x, y))


def get_cursor_xy():
    xx, yy = win32api.GetCursorPos()
    l.info("(%5d, %4d)" % (xx, yy))
    return xx, yy


def clickandreturn(x, y):
    """ clickandreturn(x, y)
    move the mouse, click and return to previous position"""
    xx, yy = win32api.GetCursorPos()
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.SetCursorPos((xx, yy))


# ########## file operation ##########
def get_num_line_in_file(thefilepath):
    """Count number of lines in a file by number of \n"""
    count, thefile = 0, open(thefilepath, 'rb')
    while 1:
        mybuffer = thefile.read(512 * 1024)
        if not mybuffer: break
        count += mybuffer.count('\n')
    thefile.close()
    return count


def download_files_ftp(IPaddr='131.101.199.181', username="vsa",
                       password="service", remotedir='./userdir',
                       DeleteAfterTransfer=False):
    """ Download all files in a FTP directory
    """
    myftp = FTP(IPaddr)  # connect to host, default port
    myftp.login(user=username, passwd=password)  # user anonymous, passwd anonymous@
    myftp.cwd(remotedir)  # Change to
    print "Remote work dir: ", myftp.pwd()
    TransferFileDir = r"FTP_Transfer"  # dir name
    if not os.path.exists(TransferFileDir):
        os.makedirs(TransferFileDir)
        print TransferFileDir, " created"
    namelist = myftp.nlst()
    print namelist
    for idx, fname in enumerate(namelist):
        fnlocal = r'%s\z%s_' % (TransferFileDir, time.strftime("%m%d%H%M%S")) + fname  # add timestamp
        print idx, "Local file location:", os.path.join(os.getcwdu(), fnlocal)
        try:
            myftp.retrbinary("RETR " + fname, open(fnlocal, 'wb').write)
        except Exception, e:
            print "ERROR %s" % e
        if DeleteAfterTransfer: myftp.delete(fname)
    print idx + 1, "files transferred to\n%s" % (os.path.dirname(os.path.abspath(fnlocal)))
    myftp.close()


# ########## file generation ##########

def generate_random_int_array(numrow=100, numcol=100, minval=0, maxval=2 ** 32 - 1):
    fnout = 'randintarr%dx%d.txt' % (numrow, numcol)
    fhout = open(fnout, 'w')
    for ct in xrange(numrow):
        d = [str(random.randint(minval, maxval)) for _ in xrange(numcol)]
        fhout.write(' '.join(d))
        fhout.write('\n')
    fhout.close()


def existDir(dirpath):
    """Check whether a directory exists. Create a new if not"""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        return False
    else:
        return True


# ########## importinfo ##########
def importinfo():
    print [key for key in locals().keys() if isinstance(locals()[key], type(sys)) and not key.startswith('__')]
    print sys.modules.keys()


# ########## Process Management ##########
def repeatexecute(consolecmd,waittimesec=60):
    l.debug(consolecmd)
    while True:
        tloop0=time.time()
        try:
            subprocess.Popen(consolecmd)
        except:
            pass
        texe=time.time()-tloop0
        timetowait=max(waittimesec-texe,0)
        pbar=pb.ProgressBar(widgets=mypbwidgets,maxval=int(math.floor(timetowait)))
        pbar.start()
        for ct in xrange(int(math.floor(timetowait))):
            pbar.update(ct)
            time.sleep(1)
        pbar.finish()

class MyTimer:
    'My time to get '

    def __init__(self):
        self.time0 = time.time()
        self.timelast, self.timenow = self.time0, self.time0

    def updatenow(self):
        self.timelast = self.timenow
        self.timenow = time.time()
        return self.timenow

    def updatelast(self):
        return self.timelast

    def getlast(self):
        return self.timelast

    def getnow(self):
        return self.timenow

    def diff_last_now(self):
        return self.timenow - self.timelast

    def diff_now(self):
        return self.timenow - self.time0

    def get_all(self):
        return self.time0, self.timelast, self.timenow

    def __del__(self):
        return self.time0, self.timelast, self.timenow

    def __repr__(self, t=None):
        if t is None:
            return time.localtime(self.time0)
        else:
            return time.localtime(t)

    def __str__(self):
        return time.strftime("%m%d-%H%M%S", self.timenow)


def main():
    repeatexecute(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",3)


if __name__ == "__main__":
    main()
else:
    print "%10s:      %s" % ("CWD", os.getcwdu())
    print "%10s:      %s" % ("Imported", __file__)
    print "\n"