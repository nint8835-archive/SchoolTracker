import json
import os

from .StatusMonitor import StatusMonitor
from .DispatcherManager import DispatcherManager


class SchoolTracker(object):

    def __init__(self):
        self.DispatcherManager = DispatcherManager()
        if os.path.isfile(os.path.join(os.getcwd(), "schools.json")):
            with open(os.path.join(os.getcwd(), "schools.json"), "r") as f:
                schools = json.load(f)
        else:
            schools = []
            with open(os.path.join(os.getcwd(), "schools.json"), "w") as f:
                json.dump(schools, f)
        self.StatusMonitor = StatusMonitor(self.DispatcherManager, schools)

    def start(self):
        self.StatusMonitor.start()
