================
progress_tracker
================

``progress_tracker`` is an easy and flexible way to print custom progress messages while processing streams of events on the CLI.

It was originally developed at `exactEarth Ltd`_ . See `this presentation`_ to `DevHouse Waterloo`_ for the original motivation.

.. _exactEarth Ltd: https://exactearth.com/

Built and tested with Python 3.6+

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

The core of ``progress_tracker`` is a method called ``track_progress``.
By changing the parameters passed to ``track_progress``, you can customize how frequently (and with what messages) the tracker will report.

.. code:: python

    def track_progress( 
        iterable: Iterable[T], # The iterable to iterate over
        total: Optional[int] = None, # Override for the total message count, defaults to len(iterable)
        callback: Callable[[str], Any] = print, # A function (f(str) -> None) that gets called each time a condition matches
        format_callback: Callable[[Dict[str, Any], Set[str]], str] = default_format_callback, # A function (f(str) -> str) that formats the progress values into a string.
        every_n_percent: Optional[float] = None, # Reports after every n percent
        every_n_records: Optional[int] = None, # Reports every n records
        every_n_seconds: Optional[float] = None, # Reports every n seconds
        every_n_seconds_idle: Optional[float] = None, # Report if there has not been a record processed in the past n seconds. Useful for infinite streams.
        every_n_seconds_since_report: Optional[float] = None, # Report if there hasn’t been any report in the past n seconds.
        report_first_record: bool = False, # Report after the first record
        report_last_record: bool = False # Report after the last record
        ) -> None

Examples
^^^^^^^^

Print after every n records are processed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``every_n_records`` parameter will trigger a report after every nth record is processed. 

.. code:: python

    >>> from progress_tracker import track_progress
    >>>
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

Print after every x percent of records are processed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``every_n_percent`` parameter will trigger a report after every nth percent of records are processed. 

.. code:: python

    >>> from progress_tracker import track_progress
    >>> for _ in track_progress(list(range(1000)), every_n_percent=10):
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

``every_n_percent`` only works for bounded iterables. For unbounded iterables (ex. streams), using ``every_n_percent`` will report a ``RuntimeWarning``.

At most a single report is generated per processed record. Even if processing of a single record would meet the conditions multiple times 
(ex. if ``every_n_percent=10``, but there are only 2 records, then processing each record causes 50%, or 5 * 10%, progress), only a single report is created (containing the latest values).

Print every n records OR every n seconds during processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is especially useful when you have highly variable processing times (ex. most records take 2 seconds to process, but some take 20 seconds to process).
You can use the ``every_n_seconds`` parameter to get reports between the expensive records.

.. code:: python

    import time
    from progress_tracker import track_progress

    def simulated_processing(item):
        if item == 'hard':
            time.sleep(10)

    variable_stream_simulation = (['easy'] * 15) + (['hard'] * 5) + (['easy'] * 15)

    for item in track_progress(variable_stream_simulation, every_n_records=5, every_n_seconds=10):
        simulated_processing(item)

    ...
    5/35 (14.285714285714285%) in 0:00:00.000014 (Time left: 0:00:00.000084)
    10/35 (28.57142857142857%) in 0:00:00.000095 (Time left: 0:00:00.000238)
    15/35 (42.857142857142854%) in 0:00:00.000120 (Time left: 0:00:00.000160)
    16/35 (45.714285714285715%) in 0:00:10.011364 (Time left: 0:00:11.888495)
    17/35 (48.57142857142857%) in 0:00:20.022107 (Time left: 0:00:21.199878)
    18/35 (51.42857142857142%) in 0:00:30.031801 (Time left: 0:00:28.363368)
    19/35 (54.285714285714285%) in 0:00:40.041754 (Time left: 0:00:33.719372)
    20/35 (57.14285714285714%) in 0:00:50.073991 (Time left: 0:00:37.555493)
    25/35 (71.42857142857143%) in 0:00:50.074246 (Time left: 0:00:20.029698)
    30/35 (85.71428571428571%) in 0:00:50.074286 (Time left: 0:00:08.345714)
    35 in 0:00:50.074319

During the processing of the slow records, ``track_progress`` reported after every record.

Note: Because the default "Time left" calculation is just a simple linear extrapolation, it is not as useful in the face of such variability in processing times.

Combining trigger conditions
----------------------------

As seen in the previous example, you can combine multiple conditions together to dictate when a report is created.

Each of the conditions are combined using an OR operator, meaning that if any condition is met, a report is created.

Even if multiple conditions are met simultaneously, only a single report will be created.

Report Creation Invariants
--------------------------

Report creation observes two invariants:

1. At most a single report is created per processed record.
2. Reports are only created in response to a record being processed.

Customizing the report formatting / Internationalization
--------------------------------------------------------

By default, ``progress_tracker`` formats the report into an English language string.
This can be overriden by supplying a different function as the ``format_callback`` parameter to ``track_progress``.

This can be used to perform advanced formatting, or to add internationalization/localization.

.. code:: python

    def format_en_francais(report: Dict[str, Any], reasons: Set[str]):
        i = report["i"]
        total = report["total"]
        if total is None or i == total:
            format_string = "{i} messages traités en {time_taken}"
        else:
            format_string = "{i}/{total} messages traités en {time_taken} (temps restant: {estimated_time_remaining})"
        return format_string.format(**report)

    for poste in track_progress(postes, every_n_records=100, format_callback=format_en_francais):
        traité(poste)

(Veuillez excuser toute erreur en français. C'est le résultat de Google Translate.)

Simple cases can also be done using a lambda:

.. code:: python

    >>> from progress_tracker import track_progress
    >>>
    >>> for _ in track_progress(list(range(5)), every_n_records=1, format_callback=lambda **kwargs: "Got one!"):
    ...     continue
    ...
    Got one!
    Got one!
    Got one!
    Got one!
    Got one!

Report values available
^^^^^^^^^^^^^^^^^^^^^^^

The following values are available in every report for use in the ``format_callback``:

.. table::
   :widths: auto

   ============================== =================== =======================================================================================================================================
   Value                          Type                Meaning
   ============================== =================== =======================================================================================================================================
   ``{records_seen}``             int                 The number of records processed so far.
   ``{total}``                    Optional[int]       The total of records in the iterable, if known. Else ``None``
   ``{percent_complete}``         Optional[float]     The percentage of records processed so far. ``None`` if ``{total}`` is ``None`` or ``records_seen`` = 0
   ``{time_taken}``               timedelta           The amount of time that processing has taken thus far.
   ``{estimated_time_remaining}`` Optional[timedelta] The estimated amount of time needed in order to process the rest of the records (simple linear estimate). ``None`` if total is ``None``
   ``{items_per_second}``         Optional[float]     The number of records processed so far / the number of seconds elapsed. ``None`` if no time have elapsed.
   ``{idle_time}``                timedelta           The amount of idle time between the previous record's processing and this record's arrival.
   ============================== =================== =======================================================================================================================================

Customizing the print behaviour
-------------------------------

By default, ``progress_tracker`` calls Python's `print`_ function with the formatted report.
This can be overriden by supplying a different function as the ``callback`` parameter to ``track_progress``.

.. _`print`: https://docs.python.org/3/library/functions.html#print

``every_n_seconds_idle``
------------------------

``every_n_seconds_idle`` allows you to trigger a report if there is ever more than ``n`` seconds when no records were processed.

Note: If processing of a single record takes longer than ``every_n_seconds_idle``, then it will be triggered after every record.

Difference between ``every_n_seconds`` and ``every_n_seconds_idle``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``every_n_seconds`` triggers a report anytime it has been more than n seconds since ``every_n_seconds`` last triggered a report.
* ``every_n_seconds_idle`` triggers a report anytime there has not been a record processed in the past n seconds (ie. the processing has been idle).

For example:

.. table::
   :widths: auto

   ========== ================================== ============================= ================================================================ ======================
   After      # of records processed in interval Cummulative records processed every_n_seconds=3                                                every_n_seconds_idle=3
   ========== ================================== ============================= ================================================================ ======================
   0 seconds  0                                  0                                                                     
   1 second   1                                  1                                                                     
   2 seconds  1                                  2                                                                     
   3 seconds  1                                  3                             Triggered, since it is the first record T >= 3s (T >= 0s + 3s)
   4 seconds  1                                  4                                                                     
   5 seconds  1                                  5                                                                     
   6 seconds  1                                  6                             Triggered, since it is the first record T >= 6s (T >= 3s + 3s)                                         
   7 seconds  1                                  6                                                                     
   8 seconds  0                                  6                                                                     
   9 seconds  0                                  6                                                                     
   10 seconds 0                                  6                                                                     
   11 seconds 1                                  7                             Triggered, since it is the first record T >= 9s (T >= 6s + 3s)   Triggered, since it is the first record processed in the past 3 seconds (T >= 6s + 3s)                                      
   12 seconds 1                                  8                                                                     
   13 seconds 1                                  9                                                                     
   14 seconds 1                                  10                            Triggered, since it is the first record T >= 14s (T >= 11s + 3s)                                        
   15 seconds 1                                  11                                                                    
   ========== ================================== ============================= ================================================================ ======================

Note that ``every_n_seconds`` reports at 3 seconds and 6 seconds, as one would expect. Then it reports at 11 seconds, since that is the first time a record was processed after the 9 seconds mark.
Then note that instead of next reporting at 12 seconds (9s + 3s), it reports next at 14 seconds (11s + 3s).

``every_n_seconds_idle`` only reported at 11 seconds, since that was the only time that a record was processed without other records being processed during the previous 3 seconds.

Other Resources
---------------

- `This presentation`_ to `DevHouse Waterloo`_.

.. _This presentation: https://www.slideshare.net/MichaelOvermeyer/progress-tracker-a-handy-progress-printout-pattern
.. _DevHouse Waterloo: https://www.meetup.com/DevHouse-Waterloo/events/247071801/