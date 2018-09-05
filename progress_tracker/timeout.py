from datetime import datetime, timedelta
from typing import Optional


class Timeout(object):
    def __init__(self, delta: timedelta, start_time: Optional[datetime] = None) -> None:
        self.delta = delta
        self.deadline = start_time + self.delta if start_time else datetime.utcnow() + self.delta

    def reset(self) -> None:
        self.deadline = datetime.utcnow() + self.delta

    def is_overdue(self) -> bool:
        return self.deadline < datetime.utcnow()

    def time_remaining(self) -> timedelta:
        return self.deadline - datetime.utcnow()
