import rlg
import memesign
<<<<<<< HEAD
import time
=======
>>>>>>> rework
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "RLGTicker"
    _svc_display_name_ = "RLG Ticker"
<<<<<<< HEAD

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        display = memesign.MemeSign()
        rlg_thread = rlg.RogueLikeGeneral()
        with open('E:\RLGTicker\lastpost.txt', 'r') as f:
            rlg_thread.last_post = int(f.read().rstrip())
            f.close()
        rc = None

        while rc != win32event.WAIT_OBJECT_0:
            post = rlg_thread.get_next_reply()
            while len(post) > 500:
                if len(post) > 500:
                    display.add_meme(post[:500])
                    while display.wait():
                        if win32event.WAIT_OBJECT_0:
                            return
                    display.print_meme()
                    post = post[500:]
            display.add_meme(post)
            while display.wait():
                pass
            display.print_meme()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 2000)

        f = open('E:\RLGTicker\lastpost.txt', 'w')
        f.write(str(rlg_thread.last_post))
        f.close()
=======

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.display = memesign.MemeSign()
        self.rlg_thread = rlg.RogueLikeGeneral()
        self.timeout = 2000
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while True:
            post = self.rlg_thread.get_next_reply()
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                servicemanager.LogInfoMsg("RLGTicker - STOPPED")
                break
            else:
                while len(post) > 500:
                    if len(post) > 500:
                        self.display.add_meme(post[:500])
                        self.display.wait()
                        self.display.print_meme()
                        post = post[500:]
                self.display.add_meme(post)
                self.display.wait()
                self.display.print_meme()
>>>>>>> rework


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
<<<<<<< HEAD



=======
>>>>>>> rework
