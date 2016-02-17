from __future__ import division
from datetime import datetime, timedelta

from python_version_backports import MonkeyPatch
MonkeyPatch.patch_total_seconds()

class Timeout(object):
    def __init__(self, delta, start_time=None):
        self.delta = delta
        self.deadline = start_time + self.delta if start_time else datetime.utcnow() + self.delta
        
    def reset(self):
        self.deadline = datetime.utcnow() + self.delta
        
    def is_overdue(self):
        return self.deadline < datetime.utcnow()
        
    def time_remaining(self):
        return self.deadline - datetime.utcnow()

class ProgressTracker(object):
    #This is a class that allows you to offload the tracking of progress.
    #It encapsulates a number of common conditions for reporting progress.
    #
    #For example, you often want to print out your processing progress every x percent of completion, but also every y seconds.
    #This class allows you to not have to do all of this tracking in your code. Periodically, just call the 'check' function with the iteration (1-based, not 0-based) you are on, and format the results.
    #
    def __init__(self, total=None, every_x_percent=None, every_n_records=None, every_n_seconds=None, every_n_seconds_idle=None, ignore_first_iteration=True):

        self.total = total
        
        self.start_time = datetime.utcnow()

        self.every_x_percent = every_x_percent
        self.next_percent = every_x_percent if ignore_first_iteration else 0

        self.every_n_records = every_n_records
        self.next_record_count = every_n_records if ignore_first_iteration else 0
        
        self.timeout = Timeout(timedelta(seconds=every_n_seconds)) if every_n_seconds != None else None
        self.idle_timeout = Timeout(timedelta(seconds=every_n_seconds_idle)) if every_n_seconds_idle != None else None

    def __enter__(self):
        self.start_time = datetime.utcnow()
    
    def __exit__(self, type, value, traceback):
        self.complete()
    
    def should_report(self, i):
        should_report = False
        if self.timeout != None and self.timeout.is_overdue():
            should_report = True
            self.timeout.reset()
        if self.idle_timeout != None and self.idle_timeout.is_overdue():
            should_report = True
        if self.total != None and self.every_x_percent != None:
            percent_complete = (i / self.total) * 100
            if percent_complete >= self.next_percent:
                should_report = True
                self.next_percent = ((int(percent_complete) // self.every_x_percent) + 1) * self.every_x_percent
        if self.every_n_records != None and i >= self.next_record_count:
            should_report = True
            self.next_record_count = ((i // self.every_n_records) + 1) * self.every_n_records
            
        return should_report
        
    #Returns a tuple that contains all of the usual values that you want to print out.
    def check(self, i):
        if self.should_report(i):
            time_taken = datetime.utcnow() - self.start_time
            if self.total != None:
                percent_complete = (i / self.total) * 100
                estimated_time_remaining = timedelta(seconds=((100-percent_complete)/percent_complete)*time_taken.total_seconds()) if percent_complete != 0 else None
            else:
                percent_complete = None
                estimated_time_remaining = None
            
            items_per_second = i/time_taken.total_seconds() if time_taken.total_seconds() != 0 else None
            
            result = (i, self.total, percent_complete, time_taken, estimated_time_remaining, items_per_second)
        else:
            result = None
            
        if self.idle_timeout != None:
            self.idle_timeout.reset()
            
        return result
            
    def complete(self):
        self.end_time = datetime.utcnow()
        self.total_time = self.end_time - self.start_time