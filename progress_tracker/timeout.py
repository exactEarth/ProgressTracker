from datetime import datetime, timedelta
from typing import Optional


class Timeout(object):
    def __init__(self, delta: timedelta, start_time: Optional[datetime] = None) -> None:
        self.delta = delta
        self.start_time = start_time if start_time else datetime.utcnow()
        self.stop_time: Optional[datetime] = None
        self.deadline = self.start_time + self.delta

    def reset(self) -> None:
        self.start_time = datetime.utcnow()
        self.stop_time = None
        self.deadline = self.start_time + self.delta

    def is_overdue(self) -> bool:
        return self.deadline < datetime.utcnow()

    def time_remaining(self) -> timedelta:
        return self.deadline - datetime.utcnow()

    def time_elapsed(self) -> timedelta:
        return datetime.utcnow() - self.start_time if self.stop_time is None else (self.stop_time - self.start_time)

    def stop(self) -> None:
        self.stop_time = datetime.utcnow()
