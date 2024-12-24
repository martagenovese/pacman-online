import threading
import time

class GhostSupervisor(threading.Thread):
    def __init__(self, r, c, p, o):
        super().__init__()
        self.r = r
        self.c = c
        self.p = p
        self.o = o

    def set_all_status(self, n):
        self.r.set_status(n)
        self.c.set_status(n)
        self.p.set_status(n)
        self.o.set_status(n)

    def get_a_status(self):
        return self.r.get_status()

    def run(self):
        while True:
            if self.get_a_status() == 1:
                try:
                    time.sleep(7)
                except Exception:
                    pass
                self.set_all_status(0)
            elif self.get_a_status() == 0:
                try:
                    time.sleep(20)
                except Exception:
                    pass
                self.set_all_status(1)