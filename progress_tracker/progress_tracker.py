import warnings
from datetime import datetime, timedelta

from progress_tracker.timeout import Timeout
from typing import Any, Callable, Dict, Generic, Iterable, Optional, Set, Sized, Type, TypeVar, cast
from types import TracebackType

T = TypeVar("T")

EVERY_N_PERCENT = "every_n_percent"
EVERY_N_RECORDS = "every_n_records"
EVERY_N_SECONDS = "every_n_seconds"
EVERY_N_SECONDS_IDLE = "every_n_seconds_idle"
EVERY_N_SECONDS_SINCE_REPORT = "every_n_seconds_since_report"
REPORT_FIRST_RECORD = "report_first_record"
REPORT_LAST_RECORD = "report_last_record"


def default_format_callback(report: Dict[str, Any], reasons: Set[str]) -> str:
    total = report["total"]
    idle_message = " (After being idle for {idle_time})" if "every_n_seconds_idle" in reasons else ""
    if total is None or REPORT_LAST_RECORD in reasons:
        format_string = "{records_seen} in {time_taken}" + idle_message
    else:
        format_string = "{records_seen}/{total} ({percent_complete}%) in {time_taken} (Time left: {estimated_time_remaining})" + idle_message

    return format_string.format(**report)


class ProgressTracker(Generic[T]):
    # This is a class that allows you to offload the tracking of progress.
    # It encapsulates a number of common conditions for reporting progress.
    #
    # For example, you often want to print out your processing progress every x percent of completion, but also every y seconds.
    # This class allows you to not have to do all of this tracking in your code. It will call its callback function with a formatted string.
    #
    def __init__(self, iterable: Iterable[T],
                 total: Optional[int] = None,
                 callback: Callable[[str], Any] = print,
                 format_callback: Callable[[Dict[str, Any], Set[str]], str] = default_format_callback,
                 every_n_percent: Optional[float] = None,
                 every_n_records: Optional[int] = None,
                 every_n_seconds: Optional[float] = None,
                 every_n_seconds_idle: Optional[float] = None,
                 every_n_seconds_since_report: Optional[float] = None,
                 report_first_record: bool = False,
                 report_last_record: bool = False) -> None:

        self.iterable = iterable

        self.used_as_context_manager = False

        self.total: Optional[int]
        try:
            self.total = len(cast(Sized, self.iterable))
        except TypeError:
            self.total = None

        if self.total is None and total is not None:
            self.total = total

        if self.total is None and every_n_percent is not None:
            warnings.warn("Asked to report 'every_n_percent', but total length is not available.", RuntimeWarning)

        self.callback = callback
        self.format_callback = format_callback

        self.every_n_percent = every_n_percent
        self.next_percent = every_n_percent

        self.every_n_records = every_n_records
        self.next_record_count = every_n_records

        self.timeout = Timeout(timedelta(seconds=every_n_seconds)) if every_n_seconds is not None else None
        self.idle_timeout = Timeout(timedelta(seconds=every_n_seconds_idle)) if every_n_seconds_idle is not None else None
        self.last_report_timeout = Timeout(timedelta(seconds=every_n_seconds_since_report)) if every_n_seconds_since_report is not None else None

        self.report_first_record = report_first_record
        self.report_last_record = report_last_record

        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_time: Optional[timedelta] = None

        self.records_seen = 0
        self.reports_raised = 0
        self.report_raised_this_record = False

    def __iter__(self) -> Iterable[T]:
        def iter_helper() -> Iterable[T]:
            if self.timeout is not None:
                self.timeout.reset()
            if self.idle_timeout is not None:
                self.idle_timeout.reset()

            for record in self.iterable:
                if self.idle_timeout is not None and self.idle_timeout.is_overdue():
                    # Pause elapsed time here. Report will want this value.
                    self.idle_timeout.stop()

                self.records_seen += 1
                self.report_raised_this_record = False
                yield record  # Process record

                reasons_to_report = self.should_report()
                if reasons_to_report:
                    self.raise_report(reasons_to_report)

                if self.idle_timeout is not None:
                    self.idle_timeout.reset()

            if self.report_last_record and self.records_seen > 0 and not self.report_raised_this_record:  # Ensure that we don't break the "Report Creation Invariants".
                self.raise_report(set([REPORT_LAST_RECORD]))

        if self.used_as_context_manager:
            yield from iter_helper()
        else:
            with self:
                yield from iter_helper()

    def __enter__(self) -> 'ProgressTracker':  # https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel
        self.start_time = datetime.utcnow()
        self.used_as_context_manager = True
        return self

    def __exit__(self, exc_type: Optional[Type[Exception]], value: Optional[Exception], traceback: Optional[TracebackType]) -> None:
        self.complete()

    def raise_report(self, reasons_to_report: Set[str]) -> None:
        assert not self.report_raised_this_record, "`raise_report` called multiple times for a single record."
        self.callback(self.format_callback(self.create_report(), reasons_to_report))
        self.reports_raised += 1
        self.report_raised_this_record = True
        if self.last_report_timeout is not None:
            self.last_report_timeout.reset()

    def should_report(self) -> Set[str]:
        reasons_to_report: Set[str] = set()

        if self.report_first_record and self.records_seen == 1:
            reasons_to_report.add(REPORT_FIRST_RECORD)

        if self.idle_timeout is not None and self.idle_timeout.is_overdue():
            reasons_to_report.add(EVERY_N_SECONDS_IDLE)

        if self.last_report_timeout is not None and self.last_report_timeout.is_overdue():
            reasons_to_report.add(EVERY_N_SECONDS_SINCE_REPORT)

        if self.timeout is not None and self.timeout.is_overdue():
            reasons_to_report.add(EVERY_N_SECONDS)
            self.timeout.reset()

        if self.total is not None and self.every_n_percent is not None and self.next_percent is not None:
            percent_complete: float = (self.records_seen / self.total) * 100
            if percent_complete >= self.next_percent:
                reasons_to_report.add(EVERY_N_PERCENT)
                self.next_percent = ((int(percent_complete) // self.every_n_percent) + 1) * self.every_n_percent

        if self.every_n_records is not None and self.next_record_count is not None and self.records_seen >= self.next_record_count:
            reasons_to_report.add(EVERY_N_RECORDS)
            self.next_record_count = ((self.records_seen // self.every_n_records) + 1) * self.every_n_records

        return reasons_to_report

    def create_report(self) -> Dict[str, Any]:
        assert self.start_time is not None
        time_taken = datetime.utcnow() - self.start_time
        percent_complete: Optional[float]
        estimated_time_remaining: Optional[timedelta]
        if self.total is not None:
            percent_complete = (self.records_seen / self.total) * 100
            estimated_time_remaining = timedelta(seconds=((100 - percent_complete) / percent_complete) * time_taken.total_seconds()) if percent_complete != 0 else None
        else:
            percent_complete = None
            estimated_time_remaining = None

        items_per_second = self.records_seen / time_taken.total_seconds() if time_taken.total_seconds() != 0 else None

        return {
            'records_seen': self.records_seen,
            'total': self.total,
            'percent_complete': percent_complete,
            'time_taken': time_taken,
            'estimated_time_remaining': estimated_time_remaining,
            'items_per_second': items_per_second,
            'idle_time': self.idle_timeout.time_elapsed() if self.idle_timeout is not None else None
        }

    def complete(self) -> None:
        assert self.start_time is not None
        self.end_time = datetime.utcnow()
        self.total_time = self.end_time - self.start_time


def track_progress(iterable: Iterable[T], **kwargs: Any) -> ProgressTracker[T]:
    return ProgressTracker(iterable, **kwargs)
