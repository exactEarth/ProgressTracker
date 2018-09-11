================
progress_tracker
================

``progress_tracker`` is an easy and flexible way to print custom progress messages while processing streams of events on the CLI.

It was originally developed at `exactEarth Ltd`_ . See `this presentation`_ to `DevHouse Waterloo`_ for the original motivation.

.. _exactEarth Ltd: https://exactearth.com/

Tested with Python 3.4, 3.5, 3.6, 3.7.

.. contents:: Contents

Quick Start
-----------

.. code:: bash

  % pip install progress_tracker

.. code:: python

    >>> from progress_tracker import track_progress
    >>> for _ in track_progress(list(range(1000)), every_n_records=100):
    ...     continue
    ...
    100/1000 (10.0%) in 0:00:00.000114 (Time left: 0:00:00.001026)
    200/1000 (20.0%) in 0:00:00.000274 (Time left: 0:00:00.001096)
    300/1000 (30.0%) in 0:00:00.000374 (Time left: 0:00:00.000873)
    400/1000 (40.0%) in 0:00:00.000473 (Time left: 0:00:00.000710)
    500/1000 (50.0%) in 0:00:00.000572 (Time left: 0:00:00.000572)
    600/1000 (60.0%) in 0:00:00.000671 (Time left: 0:00:00.000447)
    700/1000 (70.0%) in 0:00:00.000770 (Time left: 0:00:00.000330)
    800/1000 (80.0%) in 0:00:00.000868 (Time left: 0:00:00.000217)
    900/1000 (90.0%) in 0:00:00.000979 (Time left: 0:00:00.000109)
    1000 in 0:00:00.001086

Usage
-----

``progress_tracker`` is very customizable to fit your desires, but tries to have sensible defaults.

The core of ``progress_tracker`` is a class called ``ProgressTracker``. By changing the parameters passed into its constructor, you can customize how frequently (and with what messages) the tracker will report.

.. code:: python

    def __init__(self, 
        iterable: Iterable[T], # The iterable to iterate over
        total: Optional[int] = None, # Override for the total message count, defaults to len(iterable)
        callback: Callable[[str], Any] = print, # A function (f(str) -> None) that gets called each time a condition matches
        format_callback: Callable[..., str] = default_format_callback, # A function (f(str) -> str) that formats the progress values into a string.
        format_string: Optional[str] = None, # An override for the default format strings.
        every_x_percent: Optional[float] = None, # Reports after every x percent
        every_n_records: Optional[int] = None, # Reports every n records
        every_n_seconds: Optional[float] = None, # Reports every n seconds
        every_n_seconds_idle: Optional[float] = None, # Report every n seconds, but only if there hasn’t been any progress. Useful for infinite streams
        ignore_first_iteration: bool = True, # Don’t report on the first iteration
        last_iteration: bool = False # Report after the last iteration
        ) -> None

Other Resources
---------------

- `This presentation`_ to `DevHouse Waterloo`_

.. _This presentation: https://www.slideshare.net/MichaelOvermeyer/progress-tracker-a-handy-progress-printout-pattern
.. _DevHouse Waterloo: https://www.meetup.com/DevHouse-Waterloo/events/247071801/