import os
import threading
from typing import List

import time

import logging
import requests

from .School import School
from .DispatcherManager import DispatcherManager


class StatusMonitor(threading.Thread):

    def __init__(self, dispatcher_manager: DispatcherManager, schools: List[dict]):
        super(StatusMonitor, self).__init__()
        self.logger = logging.getLogger("StatusMonitor")
        self.dispatcher_manager = dispatcher_manager
        self.schools = []  # type: List[School]

        for school in schools:
            self.schools.append(School(self, **school))

        self.running = False
        self.first_check = not os.getenv("SCHOOLTRACKER_DEBUG", False)

    def run(self):
        self.running = True

        while self.running:
            for school in self.schools:
                self.check_status(school)
            if self.first_check:
                self.first_check = False
            time.sleep(60)

    def check_status(self, school: School):
        page_response = requests.get("https://www.nlesd.ca/schools/statusreport/")
        resp_text = page_response.text.replace("\r", "").replace("\n", "")
        if resp_text.count(school.name) != 0:
            # Brace for bootleg text parsing
            after_school = resp_text.split(school.name + "</a>")[1]
            span = after_school.split("<br/>")[3]
            status_list = span.split(";\">")[1].split("<span style=\"color: grey;\"></span>")[0].split(
                "</span><br>")
            status = ". ".join(
                [i.replace("<br/>", "").replace("<br>", "").split("<span")[0].strip().rstrip(".").capitalize() for i in
                 status_list])
        else:
            status = "School open"

        if status != school.last_status:
            self.logger.info("Status for {} updated. New status: {}".format(school.name, status))
            self.dispatch_notification(school, status)
            school.last_status = status

    def dispatch_notification(self, school: School, new_status: str):
        if self.first_check:
            return
        else:
            self.dispatcher_manager.dispatch_notification(school, new_status)