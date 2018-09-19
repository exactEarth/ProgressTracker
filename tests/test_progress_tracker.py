import time
import unittest

from collections import Counter
from progress_tracker import track_progress


class CustomFormatStrings(unittest.TestCase):
    def custom_callback(self, message):
        int(message)

    def test_custom_bounded(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_percent=5, callback=self.custom_callback, format_callback=lambda report, _reasons: "{records_seen}".format(**report)))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)

    def test_custom_unbounded(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), every_n_records=5, callback=self.custom_callback, format_callback=lambda report, _reasons: "{records_seen}".format(**report)))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)


class CustomFormatFunctions(unittest.TestCase):
    def setUp(self):
        self.callback_results = Counter()

    def custom_print_callback(self, message):
        self.callback_results[message] += 1

    def custom_format_callback(self, report, reasons):
        return "Odd" if report['records_seen'] % 2 == 1 else "Even"

    def test_custom_bounded(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_percent=5, callback=self.custom_print_callback, format_callback=self.custom_format_callback))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_results["Odd"], 10)
        self.assertEqual(self.callback_results["Even"], 10)


class IterateWithDelays(object):
    def __init__(self, iterable, gaps_every_n_records=2, gap_seconds=5):
        self.iterable = iterable
        self.gaps_every_n_records = gaps_every_n_records
        self.gap_seconds = gap_seconds

    def __len__(self):
        return len(self.iterable)

    def __iter__(self):
        for i, _ in enumerate(self.iterable):
            if i % self.gaps_every_n_records == self.gaps_every_n_records - 1:
                time.sleep(self.gap_seconds)
            yield i


def iterate_with_delays(*args, **kwargs):
    return IterateWithDelays(*args, **kwargs)


class BoundedTests(unittest.TestCase):
    def setUp(self):
        self.callback_count = 0

    def increment(self):
        self.callback_count += 1

    def test_every_n_percent(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_percent=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_first_and_last_records(self):
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), report_first_record=True, report_last_record=True, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 2)

    def test_every_n_percent_while_including_first(self):
        # [0,5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_percent=5, report_first_record=True, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 21)

    def test_every_n_records(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_records=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_every_n_records_while_including_first(self):
        # [0,5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_records=5, report_first_record=True, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 21)

    def test_every_n_seconds(self):
        NUMBER_OF_ITERATIONS = 2
        SECONDS_BETWEEN_ITERATIONS = 2
        print("Starting a test that will take {0} seconds".format(NUMBER_OF_ITERATIONS * SECONDS_BETWEEN_ITERATIONS))
        for _ in track_progress(range(1, NUMBER_OF_ITERATIONS + 1), every_n_seconds=1, callback=lambda _: self.increment()):
            time.sleep(SECONDS_BETWEEN_ITERATIONS)
        self.assertEqual(self.callback_count, 2)

    def test_every_n_seconds_idle(self):
        IDLE_SECONDS_TRIGGER = 2

        print("Starting a test that will take {0} seconds".format(IDLE_SECONDS_TRIGGER + 2))
        for _ in track_progress(iterate_with_delays(range(1, 4), gaps_every_n_records=2, gap_seconds=IDLE_SECONDS_TRIGGER + 2),
                                every_n_seconds_idle=IDLE_SECONDS_TRIGGER,
                                callback=lambda _: self.increment()):
            continue
        self.assertEqual(self.callback_count, 1)

    def test_every_n_percent_every_y_records(self):
        NUMBER_OF_ITERATIONS = 100

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_percent=10, every_n_records=11, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 19)

    def test_record_keeping(self):
        NUMBER_OF_ITERATIONS = 100

        pt = track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_percent=10, every_n_records=11, callback=lambda _: self.increment())
        results = list(pt)
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(len(results), pt.records_seen)
        self.assertEqual(self.callback_count, 19)
        self.assertEqual(self.callback_count, pt.reports_raised)
        self.assertNotEqual(pt.start_time, None)
        self.assertNotEqual(pt.end_time, None)
        self.assertNotEqual(pt.total_time, None)


class UnboundedTests(unittest.TestCase):
    def setUp(self):
        self.callback_count = 0

    def increment(self):
        self.callback_count += 1

    def test_every_n_percent(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        # every_n_percent doesn't make sense when you don't know the size (because it is a generator)
        with self.assertRaises(Exception):
            track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), every_n_percent=5, callback=lambda _: self.increment())

        # But if you happen to know the size a priori, you can pass it in
        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), total=NUMBER_OF_ITERATIONS, every_n_percent=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_first_and_last_records(self):
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), report_first_record=True, report_last_record=True, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 2)

    def test_every_n_records(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), every_n_records=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_every_n_seconds(self):
        NUMBER_OF_ITERATIONS = 2
        SECONDS_BETWEEN_ITERATIONS = 2
        print("Starting a test that will take {0} seconds".format(NUMBER_OF_ITERATIONS * SECONDS_BETWEEN_ITERATIONS))
        for _ in track_progress((i for i in range(1, NUMBER_OF_ITERATIONS + 1)), every_n_seconds=1, callback=lambda _: self.increment()):
            time.sleep(SECONDS_BETWEEN_ITERATIONS)
        self.assertEqual(self.callback_count, 2)

    def test_every_n_seconds_idle(self):
        IDLE_SECONDS_TRIGGER = 2

        print("Starting a test that will take {0} seconds".format(IDLE_SECONDS_TRIGGER + 2))
        for _ in track_progress(iterate_with_delays((i for i in range(1, 4)), gaps_every_n_records=2, gap_seconds=IDLE_SECONDS_TRIGGER + 2),
                                every_n_seconds_idle=IDLE_SECONDS_TRIGGER,
                                callback=lambda _: self.increment()):
            continue
        self.assertEqual(self.callback_count, 1)

    def test_every_n_percent_every_y_records(self):
        NUMBER_OF_ITERATIONS = 100

        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), total=NUMBER_OF_ITERATIONS, every_n_percent=10, every_n_records=11, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 19)

    def test_format_strings(self):
        track_progress((i for i in range(0, 100)), total=100, format_callback=lambda report, _reasons: "{percent_complete}".format(**report), every_n_records=11, callback=lambda _: self.increment())


if __name__ == '__main__':
    unittest.main()
