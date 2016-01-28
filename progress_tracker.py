from __future__ import division
from datetime import datetime, timedelta
from python_version_backports import total_seconds

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
    def __init__(self, total=None, every_x_percent=None, every_n_records=None, every_n_seconds=None, every_n_seconds_idle=None):
        
        self.total = total
        
        self.start_time = datetime.utcnow()
        
        self.every_x_percent = every_x_percent
        self.next_percent = 0
        
        self.every_n_records = every_n_records
        self.next_record_count = 0
        
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
        elif self.idle_timeout != None and self.idle_timeout.is_overdue():
            should_report = True
        elif self.total != None and self.every_x_percent != None:
            percent_complete = (i / self.total) * 100
            if percent_complete > self.next_percent:
                should_report = True
                self.next_percent = ((int(percent_complete) // self.every_x_percent) + 1) * self.every_x_percent
        elif self.every_n_records != None and i > self.next_record_count:
            should_report = True
            self.next_record_count = ((i // self.every_n_records) + 1) * self.every_n_records
        return should_report
        
    def check(self, i):
        if self.should_report(i):
            time_taken = datetime.utcnow() - self.start_time
            if self.total != None:
                percent_complete = (i / self.total) * 100
                estimated_time_remaining = timedelta(seconds=((100-percent_complete)/percent_complete)*total_seconds(time_taken))
            else:
                percent_complete = None
                estimated_time_remaining = None
            
            items_per_second = i/total_seconds(time_taken) if total_seconds(time_taken) != 0 else None
            
            result = (i, self.total, percent_complete, time_taken, estimated_time_remaining, items_per_second)
        else:
            result = None
            
        if self.idle_timeout != None:
            self.idle_timeout.reset()
            
        return result
            
    def complete(self):
        self.end_time = datetime.utcnow()
        self.total_time = self.end_time - self.start_time