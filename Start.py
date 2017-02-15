import logging
import os

from SchoolTracker import SchoolTracker
from SchoolTracker.Dispatcher.TwitterDispatcher import TwitterDispatcher
from SchoolTracker.Dispatcher.PushoverDispatcher import PushoverDispatcher

if os.getenv("SCHOOLTRACKER_DEBUG", False):
    log_level = logging.DEBUG
else:
    log_level = logging.INFO
schooltracker = SchoolTracker(log_level)
schooltracker.DispatcherManager.register_dispatcher(TwitterDispatcher)
schooltracker.DispatcherManager.register_dispatcher(PushoverDispatcher)
schooltracker.start()
