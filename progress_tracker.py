from __future__ import division, print_function
from datetime import datetime, timedelta

from ee_libs.timeout import Timeout
from python_version_backports import MonkeyPatch
MonkeyPatch.patch_total_seconds()


class ProgressTracker(object):
    # This is a class that allows you to offload the tracking of progress.
    # It encapsulates a number of common conditions for reporting progress.
    #
    # For example, you often want to print out your processing progress every x percent of completion, but also every y seconds.
    # This class allows you to not have to do all of this tracking in your code. It will call its callback function with a formatted string.
    #
    def __init__(self, iterable,
                 total=None,
                 callback=print,
                 format_string=None,
                 every_x_percent=None,
                 every_n_records=None,
                 every_n_seconds=None,
                 every_n_seconds_idle=None,
                 ignore_first_iteration=True,
                 last_iteration=False):

        self.iterable = iterable

        try:
            self.total = len(self.iterable)
        except TypeError:
            self.total = None

        if self.total is None and total is not None:
            self.total = total

        if self.total is None:
            self.format_string = format_string if format_string is not None else "{i} in {time_taken}"

            length_related_kwargs = ["total", "percent_complete", "estimated_time_remaining"]
            invalid_args = [length_related_kwarg for length_related_kwarg in length_related_kwargs if "{{{0}}}".format(length_related_kwarg) in self.format_string]
            if len(invalid_args) > 0:
                invalid_arg_strings = ["'{{{0}}}'".format(invalid_arg) for invalid_arg in invalid_args]
                proper_grammar = ", ".join(invalid_arg_strings[:-1]) + ', nor {0}'.format(invalid_arg_strings[-1]) if len(invalid_arg_strings) > 1 else invalid_arg_strings[0]
                raise Exception("Format string cannot include {0} if total length is not available.".format(proper_grammar))

            if every_x_percent is not None:
                raise Exception("Cannot ask to report 'every_x_percent' if total length is not available")

        else:
            self.format_string = format_string if format_string is not None else "{i}/{total} ({percent_complete}%) in {time_taken} (ETA:{estimated_time_remaining})"

        self.callback = callback

        self.every_x_percent = every_x_percent
        self.next_percent = every_x_percent if ignore_first_iteration else 0

        self.every_n_records = every_n_records
        self.next_record_count = every_n_records if ignore_first_iteration else 0

        self.timeout = Timeout(timedelta(seconds=every_n_seconds)) if every_n_seconds is not None else None
        self.idle_timeout = Timeout(timedelta(seconds=every_n_seconds_idle)) if every_n_seconds_idle is not None else None

        self.last_iteration = last_iteration

        self.start_time = None
        self.end_time = None
        self.total_time = None

        self.items_seen = 0
        self.times_callback_called = 0

    def __iter__(self):
        with self:
            for index, item in enumerate(self.iterable):
                self.items_seen += 1
                yield item
                check = self.check(index + 1)
                if check is not None:
                    i, total, percent_complete, time_taken, estimated_time_remaining, items_per_second = check
                    self.callback(self.format_string.format(
                        i=i,
                        total=total,
                        percent_complete=percent_complete,
                        time_taken=time_taken,
                        estimated_time_remaining=estimated_time_remaining,
                        items_per_second=items_per_second
                    ))
                    self.times_callback_called += 1

    def __enter__(self):
        self.start_time = datetime.utcnow()

    def __exit__(self, type, value, traceback):
        self.complete()

    def should_report(self, i):
        should_report = False
        if self.timeout is not None and self.timeout.is_overdue():
            should_report = True
            self.timeout.reset()
        if self.idle_timeout is not None and self.idle_timeout.is_overdue():
            should_report = True
        if self.total is not None and self.every_x_percent is not None:
            percent_complete = (i / self.total) * 100
            if percent_complete >= self.next_percent:
                should_report = True
                self.next_percent = ((int(percent_complete) // self.every_x_percent) + 1) * self.every_x_percent
        if self.every_n_records is not None and i >= self.next_record_count:
            should_report = True
            self.next_record_count = ((i // self.every_n_records) + 1) * self.every_n_records
        if self.total is not None and self.last_iteration and i == self.total:
            should_report = True

        return should_report

    # Returns a tuple that contains all of the usual values that you want to print out.
    def check(self, i):
        if self.should_report(i):
            time_taken = datetime.utcnow() - self.start_time
            if self.total is not None:
                percent_complete = (i / self.total) * 100
                estimated_time_remaining = timedelta(seconds=((100 - percent_complete) / percent_complete) * time_taken.total_seconds()) if percent_complete != 0 else None
            else:
                percent_complete = None
                estimated_time_remaining = None

            items_per_second = i / time_taken.total_seconds() if time_taken.total_seconds() != 0 else None

            result = (i, self.total, percent_complete, time_taken, estimated_time_remaining, items_per_second)
        else:
            result = None

        if self.idle_timeout is not None:
            self.idle_timeout.reset()

        return result

    def complete(self):
        self.end_time = datetime.utcnow()
        self.total_time = self.end_time - self.start_time


def track_progress(iterable, **kwargs):
    return ProgressTracker(iterable, **kwargs)
