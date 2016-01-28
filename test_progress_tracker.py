import time
import unittest

from progress_tracker import ProgressTracker

class BoundedTest(unittest.TestCase):
    def test_every_x_percent(self):
        NUMBER_OF_ITERATIONS = 100
        
        times_reported = 0
        progress = ProgressTracker(total=NUMBER_OF_ITERATIONS, every_x_percent=5)
        with progress:
            for i in range(1, NUMBER_OF_ITERATIONS+1):
                if progress.check(i) != None:
                    times_reported += 1
        self.assertEqual(times_reported, 20)

    def test_every_n_records(self):
        NUMBER_OF_ITERATIONS = 100
        
        times_reported = 0
        progress = ProgressTracker(total=NUMBER_OF_ITERATIONS, every_n_records=5)
        with progress:
            for i in range(1, NUMBER_OF_ITERATIONS+1):
                if progress.check(i) != None:
                    times_reported += 1
        self.assertEqual(times_reported, 20)
            
    def test_every_n_seconds(self):
        NUMBER_OF_ITERATIONS = 2
        SECONDS_BETWEEN_ITERATIONS = 2
        print "Starting a test that will take {0} seconds".format(NUMBER_OF_ITERATIONS * SECONDS_BETWEEN_ITERATIONS)
        times_reported = 0
        progress = ProgressTracker(every_n_seconds=1)
        with progress:
            for i in range(1, NUMBER_OF_ITERATIONS+1):
                time.sleep(SECONDS_BETWEEN_ITERATIONS)
                if progress.check(i) != None:
                    times_reported += 1
        self.assertEqual(times_reported, 2)

    def test_every_n_seconds_idle(self):
        IDLE_SECONDS_TRIGGER = 2
        
        print "Starting a test that will take {0} seconds".format((IDLE_SECONDS_TRIGGER*2) + (IDLE_SECONDS_TRIGGER+2))
        times_reported = 0
        progress = ProgressTracker(every_n_seconds_idle=IDLE_SECONDS_TRIGGER)
        with progress:
            for i in range(IDLE_SECONDS_TRIGGER*2):
                time.sleep(1)
                if progress.check(i) != None:
                    times_reported += 1
            self.assertEqual(times_reported, 0)
            
            time.sleep(IDLE_SECONDS_TRIGGER+2)
            if progress.check(0) != None:
                    times_reported += 1
            self.assertEqual(times_reported, 1)

if __name__ == '__main__':
    unittest.main()