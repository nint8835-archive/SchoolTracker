from . import StatusMonitor


class School(object):

    name = ""

    def __init__(self, status_monitor: "StatusMonitor.StatusMonitor", **kwargs):
        self.status_monitor = status_monitor
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.last_status = ""
