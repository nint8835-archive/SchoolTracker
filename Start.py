import logging
import os

from SchoolTracker import SchoolTracker
from SchoolTracker.Dispatcher.TwitterDispatcher import TwitterDispatcher

if os.getenv("SCHOOLTRACKER_DEBUG", False):
    log_level = logging.DEBUG
else:
    log_level = logging.INFO
schooltracker = SchoolTracker(log_level)
schooltracker.DispatcherManager.register_dispatcher(TwitterDispatcher)
schooltracker.start()
