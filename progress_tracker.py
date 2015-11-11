from __future__ import division
from datetime import datetime, timedelta
from ee_libs.python_version_backports import total_seconds

class Timeout(object):
    def __init__(self, delta, start_time=None):
        self.delta = delta
        self.deadline = start_time + self.delta if start_time else datetime.utcnow() + self.delta
        
    def reset(self):
        self.deadline = datetime.utcnow() + self.delta
        
    def is_overdue(self):
        return self.deadline < datetime.utcnow()

class ProgressTracker(object):
    def __init__(self, total, every_x_percent=None, every_n_records=None, every_n_seconds=None, every_n_seconds_idle=None):
        self.total = total
        
        self.start_time = datetime.utcnow()
        
        self.every_x_percent = every_x_percent
        self.next_percent = 0
        
        self.every_n_records = every_n_records
        self.next_record_count = 0
        
        self.timeout = Timeout(timedelta(every_n_seconds)) if every_n_seconds != None else None
        self.idle_timeout = Timeout(timedelta(every_n_seconds_idle)) if every_n_seconds_idle != None else None

    def __enter__(self):
        self.start_time = datetime.utcnow()
    
    def __exit__(self, type, value, traceback):
        self.complete()
    
    def check(self, i):
        percent_complete = (i / self.total) * 100
        
        should_report = False
        if self.timeout != None and self.timeout.is_overdue():
            self.timeout.reset()
        elif self.idle_timeout != None and self.idle_timeout.is_overdue():
            should_report = True
        elif self.every_x_percent != None and percent_complete > self.next_percent:
            should_report = True
            self.next_percent = ((int(percent_complete) // self.every_x_percent) + 1) * self.every_x_percent
        elif self.every_n_records != None and i > self.next_record_count:
            should_report = True
            self.next_record_count = ((i // self.every_n_records) + 1) * self.every_n_records

        if should_report:
            time_taken = datetime.utcnow() - self.start_time
            estimated_time_remaining = timedelta(seconds=((100-percent_complete)/percent_complete)*total_seconds(time_taken))
            items_per_second = i/total_seconds(time_taken)
            self.idle_timeout.reset()
            return (i, self.total, percent_complete, time_taken, estimated_time_remaining, items_per_second)
        else:
            return None
            
    def complete(self):
        self.end_time = datetime.utcnow()
        self.total_time = self.end_time - self.start_time