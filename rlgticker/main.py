import rlg
import memesign
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "RLGTicker"
    _svc_display_name_ = "RLG Ticker"

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
            while len(post) > 500:
                if len(post) > 500:
                    self.display.add_meme(post[:500])
                    self.display.wait()
                    self.display.print_meme()
                    print(post[:500])
                    post = post[500:]
            self.display.add_meme(post)
            self.display.wait()
            self.display.print_meme()
            print(post)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
