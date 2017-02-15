from typing import List

from .School import School
from .Dispatcher import NotificationDispatcher


class DispatcherManager(object):

    _dispatchers = []  # type: List[NotificationDispatcher]

    def dispatch_notification(self, school: School, new_status: str):
        for dispatcher in self._dispatchers:
            if getattr(school, dispatcher.dispatcher_name + "_ENABLED", False):
                dispatcher.dispatch_notification(school, new_status)

    def register_dispatcher(self, dispatcher: NotificationDispatcher):
        self._dispatchers.append(dispatcher())
