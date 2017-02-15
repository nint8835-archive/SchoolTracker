from typing import List

from .School import School
from .Dispatcher import NotificationDispatcher


class DispatcherManager(object):

    _dispatchers = []  # type: List[NotificationDispatcher]

    def dispatch_notification(self, school: School, new_status: str):
        for dispatcher in self._dispatchers:
            dispatcher.dispatch_notification(school, new_status)
