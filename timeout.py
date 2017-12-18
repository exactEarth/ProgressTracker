from builtins import object
from datetime import datetime


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
