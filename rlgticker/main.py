import rlg
import memesign
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import textwrap


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
            splits = textwrap.wrap(post, 500)
            for i in range(len(splits)):
                self.display.add_meme(splits[i])
                while self.display.wait():
                    pass
                self.display.print_meme()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
