import time
import unittest

from progress_tracker import track_progress


class BoundedTests(unittest.TestCase):
    def setUp(self):
        self.callback_count = 0

    def increment(self):
        self.callback_count += 1

    def test_every_x_percent(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_x_percent=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_every_x_percent_while_including_first(self):
        # [0,5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_x_percent=5, ignore_first_iteration=False, callback=lambda _: self.increment()))
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

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_n_records=5, ignore_first_iteration=False, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 21)

    def test_every_n_seconds(self):
        NUMBER_OF_ITERATIONS = 2
        SECONDS_BETWEEN_ITERATIONS = 2
        print "Starting a test that will take {0} seconds".format(NUMBER_OF_ITERATIONS * SECONDS_BETWEEN_ITERATIONS)
        for _ in track_progress(range(1, NUMBER_OF_ITERATIONS + 1), every_n_seconds=1, callback=lambda _: self.increment()):
            time.sleep(SECONDS_BETWEEN_ITERATIONS)
        self.assertEqual(self.callback_count, 2)

    def test_every_n_seconds_idle(self):
        IDLE_SECONDS_TRIGGER = 2

        print "Starting a test that will take {0} seconds".format((IDLE_SECONDS_TRIGGER * 2) - 1 + (IDLE_SECONDS_TRIGGER + 2))

        for i in track_progress(range(1, IDLE_SECONDS_TRIGGER * 2), every_n_seconds_idle=IDLE_SECONDS_TRIGGER, callback=lambda _: self.increment()):
            time.sleep(1)
            if i == 1:
                self.assertEqual(self.callback_count, 0)
            elif i == 2:
                time.sleep(IDLE_SECONDS_TRIGGER + 2)
        self.assertEqual(self.callback_count, 1)

    def test_every_x_percent_every_y_records(self):
        NUMBER_OF_ITERATIONS = 100

        results = list(track_progress(range(0, NUMBER_OF_ITERATIONS), every_x_percent=10, every_n_records=11, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 19)

    def test_record_keeping(self):
        NUMBER_OF_ITERATIONS = 100

        pt = track_progress(range(0, NUMBER_OF_ITERATIONS), every_x_percent=10, every_n_records=11, callback=lambda _: self.increment())
        results = list(pt)
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(len(results), pt.items_seen)
        self.assertEqual(self.callback_count, 19)
        self.assertEqual(self.callback_count, pt.times_callback_called)
        self.assertNotEqual(pt.start_time, None)
        self.assertNotEqual(pt.end_time, None)
        self.assertNotEqual(pt.total_time, None)


class UnboundedTests(unittest.TestCase):
    def setUp(self):
        self.callback_count = 0

    def increment(self):
        self.callback_count += 1

    def test_every_x_percent(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        # every_x_percent doesn't make sense when you don't know the size (because it is a generator)
        with self.assertRaises(Exception):
            track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), every_x_percent=5, callback=lambda _: self.increment())

        # But if you happen to know the size a priori, you can pass it in
        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), total=NUMBER_OF_ITERATIONS, every_x_percent=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_every_n_records(self):
        # [5,10...100]
        NUMBER_OF_ITERATIONS = 101

        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), every_n_records=5, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 20)

    def test_every_n_seconds(self):
        NUMBER_OF_ITERATIONS = 2
        SECONDS_BETWEEN_ITERATIONS = 2
        print "Starting a test that will take {0} seconds".format(NUMBER_OF_ITERATIONS * SECONDS_BETWEEN_ITERATIONS)
        for _ in track_progress((i for i in range(1, NUMBER_OF_ITERATIONS + 1)), every_n_seconds=1, callback=lambda _: self.increment()):
            time.sleep(SECONDS_BETWEEN_ITERATIONS)
        self.assertEqual(self.callback_count, 2)

    def test_every_n_seconds_idle(self):
        IDLE_SECONDS_TRIGGER = 2

        print "Starting a test that will take {0} seconds".format((IDLE_SECONDS_TRIGGER * 2) - 1 + (IDLE_SECONDS_TRIGGER + 2))

        for i in track_progress((i for i in range(1, IDLE_SECONDS_TRIGGER * 2)), every_n_seconds_idle=IDLE_SECONDS_TRIGGER, callback=lambda _: self.increment()):
            time.sleep(1)
            if i == 1:
                self.assertEqual(self.callback_count, 0)
            elif i == 2:
                time.sleep(IDLE_SECONDS_TRIGGER + 2)
        self.assertEqual(self.callback_count, 1)

    def test_every_x_percent_every_y_records(self):
        NUMBER_OF_ITERATIONS = 100

        results = list(track_progress((i for i in range(0, NUMBER_OF_ITERATIONS)), total=NUMBER_OF_ITERATIONS, every_x_percent=10, every_n_records=11, callback=lambda _: self.increment()))
        self.assertEqual(len(results), NUMBER_OF_ITERATIONS)
        self.assertEqual(self.callback_count, 19)

    def test_format_strings(self):
        with self.assertRaises(Exception):
            track_progress((i for i in range(0, 100)), format_string="{percent_complete}", every_n_records=11, callback=lambda _: self.increment())

        track_progress((i for i in range(0, 100)), total=100, format_string="{percent_complete}", every_n_records=11, callback=lambda _: self.increment())


if __name__ == '__main__':
    unittest.main()
